# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,177
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Note that we don't combine the main with ray_trainer as ray_trainer is used by other main.
"""

import os
import socket
import sys 
HOME_DIR = os.getcwd() # When running from ~/verl_x 
sys.path.append(HOME_DIR)
print(f"[TM] HOME_DIR: {HOME_DIR}")
import hydra
import ray
from omegaconf import OmegaConf
from verl import DataProto
from verl.single_controller.ray.base import RayClassWithInitArgs
from verl.trainer.ppo.reward import get_custom_reward_fn
from recipe.grid_dapo.dapo_ray_trainer import RayDAPOTrainer


@hydra.main(config_path="../recipe/grid_dapo/config", config_name="dapo_trainer", version_base=None)
def main(config):
    run_ppo(config)


def run_ppo(config) -> None:
    if not ray.is_initialized():
        # this is for local ray cluster
        ray.init(
            runtime_env={"env_vars": {"RAY_DEBUG": "0", "TOKENIZERS_PARALLELISM": "true", "NCCL_DEBUG": "WARN", "VLLM_LOGGING_LEVEL": "WARN"}},
            num_cpus=config.ray_init.num_cpus,
        )
    if OmegaConf.select(config.trainer, "profile_steps") is not None and len(OmegaConf.select(config.trainer, "profile_steps")) > 0:
        nsight_options = OmegaConf.to_container(config.trainer.controller_nsight_options)
        runner = TaskRunner.options(runtime_env={"nsight": nsight_options}).remote()
    else:
        runner = TaskRunner.remote()
    ray.get(runner.run.remote(config))


@ray.remote(num_cpus=1)  # please make sure main_task is not scheduled on head
class TaskRunner:
    def run(self, config):
        # print initial config
        from pprint import pprint
        from omegaconf import OmegaConf
        from verl.trainer.main_ppo import create_rl_dataset
        from verl.utils.fs import copy_to_local
        from verl.utils import hf_tokenizer
        from pathlib import Path 
        from tm_tutorials.RLHF_dataset0 import collate_fn
        from torchdata.stateful_dataloader import StatefulDataLoader

        print(f"TaskRunner hostname: {socket.gethostname()}, PID: {os.getpid()}")
        pprint(OmegaConf.to_container(config, resolve=True))  # resolve=True will eval symbol values
        OmegaConf.resolve(config)

        # download the checkpoint from hdfs
        '''
        To ensure that the model checkpoint is available locally on the worker node where the Ray actor will use it 
        — especially during model.load() or similar operations.
        '''
        local_path = copy_to_local(config.actor_rollout_ref.model.path)
        tokenizer = hf_tokenizer(local_path)
        train_dataset = create_rl_dataset(config.data.train_files, config.data, tokenizer, None)
        train_loader = StatefulDataLoader(
            dataset=train_dataset,
            batch_size=config.data.train_batch_size,
            num_workers=config.data.get("dataloader_num_workers", 0),
            collate_fn=collate_fn
        )
        # define worker classes
        if config.actor_rollout_ref.actor.strategy == "fsdp":
            assert config.actor_rollout_ref.actor.strategy == config.critic.strategy
            from verl.single_controller.ray import RayWorkerGroup
            from verl.workers.fsdp_workers import ActorRolloutRefWorker, CriticWorker
            ray_worker_group_cls = RayWorkerGroup
        elif config.actor_rollout_ref.actor.strategy == "megatron":
            assert config.actor_rollout_ref.actor.strategy == config.critic.strategy
            from verl.single_controller.ray.megatron import NVMegatronRayWorkerGroup
            from verl.workers.megatron_workers import ActorRolloutRefWorker, CriticWorker
            ray_worker_group_cls = NVMegatronRayWorkerGroup
        else:
            raise NotImplementedError

        from verl.trainer.ppo.ray_trainer import ResourcePoolManager, Role

        role_worker_mapping = {
            Role.ActorRollout: ray.remote(ActorRolloutRefWorker),
            Role.Critic: ray.remote(CriticWorker),
        }
        global_pool_id = "global_pool"
        resource_pool_spec = {
            global_pool_id: [config.trainer.n_gpus_per_node] * config.trainer.nnodes,
        }
        mapping = {
            Role.ActorRollout: global_pool_id,
            Role.Critic: global_pool_id,
        }
        from verl.workers.reward_manager import get_reward_manager_cls
        # Note: please make sure custom reward managers are imported and
        # registered via `verl.workers.reward_manager.register`
        reward_manager_name = config.reward_model.get("reward_manager", "naive")
        reward_manager_cls = get_reward_manager_cls(reward_manager_name)

        compute_score = get_custom_reward_fn(config)
        print(f'[TM] {config.data.reward_fn_key=}')
        reward_fn = reward_manager_cls(
            tokenizer=tokenizer,
            num_examine=1, 
            compute_score=compute_score,
            reward_fn_key=config.data.reward_fn_key,
            max_resp_len=config.data.max_response_length,
            overlong_buffer_cfg=config.reward_model.overlong_buffer,
        )
        # Note that we always use function-based RM for validation
        val_reward_fn = reward_manager_cls(
            tokenizer=tokenizer,
            num_examine=1,
            compute_score=compute_score,
            reward_fn_key=config.data.reward_fn_key, # This value is data_source
            max_resp_len=config.data.max_response_length,
            overlong_buffer_cfg=config.reward_model.overlong_buffer,
        )
        resource_pool_manager = ResourcePoolManager(resource_pool_spec=resource_pool_spec, mapping=mapping)
        resource_pool_manager.create_resource_pool()
        print(f'{resource_pool_manager=}')
        resource_pool_to_cls = {pool: {} for pool in self.resource_pool_manager.resource_pool_dict.values()}
        print(f'{resource_pool_to_cls=}')
        for batch in train_loader:
            break
        extract_one = {
                'input_ids': batch['input_ids'][0],
                'attention_mask': batch['attention_mask'][0],
                'position_ids': batch['position_ids'][0],
                'reward_model': batch['reward_model'][0]
            }
        pprint(extract_one)
        ### JUST USE THE LAST BATCH, for code understanding ###
        new_batch: DataProto = DataProto.from_single_dict(batch)
        # pop those keys for generation
        gen_batch = new_batch.pop(
            batch_keys=["input_ids", "attention_mask", "position_ids"],
            non_tensor_batch_keys=["raw_prompt_ids"], # raw_prompt_ids: input_ids with padding.
        )
        actor_rollout_wg = role_worker_mapping[Role.ActorRollout]
        actor_rollout_wg_cls = RayClassWithInitArgs(actor_rollout_wg, config=config.actor_rollout_ref, role="ref")
        '''
        # worker_dict_cls = create_colocated_worker_cls(class_dict=class_dict)
        # wg_dict = self.ray_worker_group_cls(resource_pool=resource_pool, ray_cls_with_init=worker_dict_cls, device_name=self.device_name, **wg_kwargs)
        # spawn_wg = wg_dict.spawn(prefix_set=class_dict.keys())
        # all_wg.update(spawn_wg)
        
        # actor_rollout_wg_cls.init_model()
        # gen_batch_output = actor_rollout_wg_cls.generate_sequences(gen_batch)
        # print(gen_batch_output)
        # create actor and rollout
        if self.hybrid_engine:
            resource_pool = self.resource_pool_manager.get_resource_pool(Role.ActorRollout)
            print(f'{resource_pool=}')
            actor_rollout_cls = RayClassWithInitArgs(
                cls=self.role_worker_mapping[Role.ActorRollout],
                config=self.config.actor_rollout_ref,
                role="actor_rollout",
            )
            self.resource_pool_to_cls[resource_pool]["actor_rollout"] = actor_rollout_cls
        else:
            raise NotImplementedError

        # create critic
        if self.use_critic:
            resource_pool = self.resource_pool_manager.get_resource_pool(Role.Critic)
            critic_cls = RayClassWithInitArgs(cls=self.role_worker_mapping[Role.Critic], config=self.config.critic)
            self.resource_pool_to_cls[resource_pool]["critic"] = critic_cls

        # create reference policy if needed
        if self.use_reference_policy:
            resource_pool = self.resource_pool_manager.get_resource_pool(Role.RefPolicy)
            ref_policy_cls = RayClassWithInitArgs(self.role_worker_mapping[Role.RefPolicy], config=self.config.actor_rollout_ref, role="ref")
            self.resource_pool_to_cls[resource_pool]["ref"] = ref_policy_cls
        '''

if __name__ == '__main__':
    main()