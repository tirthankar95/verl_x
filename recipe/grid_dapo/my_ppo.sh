#!/usr/bin/env bash
set -xeuo pipefail

project_name='DAPO'
exp_name='DAPO-Early-AnyLLM'

# Paths
RAY_DATA_HOME=${RAY_DATA_HOME:-"${HOME}/verl_x"}
MODEL_PATH=${MODEL_PATH:-"${HOME}/models/Qwen2-1.5B-Instruct"}
TRAIN_FILE=${TRAIN_FILE:-"${RAY_DATA_HOME}/data/aime-2024.parquet"}
TEST_FILE=${TEST_FILE:-"${RAY_DATA_HOME}/data/aime-2024.parquet"}

# Algorithm
PYTHONUNBUFFERED=1 python3 -m verl.trainer.main_ppo \
    data.train_files=$TRAIN_FILE \
    data.val_files=$TEST_FILE \
    data.train_batch_size=128 \
    data.max_prompt_length=512 \
    data.max_response_length=256 \
    actor_rollout_ref.model.lora_rank=8 \
    actor_rollout_ref.model.lora_alpha=16 \
    actor_rollout_ref.rollout.load_format=safetensors \
    actor_rollout_ref.model.path=$MODEL_PATH \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.actor.ppo_mini_batch_size=1 \
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=1 \
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=1 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.7 \
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=1 \
    critic.optim.lr=1e-5 \
    critic.model.path=$MODEL_PATH \
    critic.ppo_micro_batch_size_per_gpu=1 \
    algorithm.kl_ctrl.kl_coef=0.001 \
    trainer.logger=['console'] \
    trainer.val_before_train=False \
    trainer.default_hdfs_dir=null \
    trainer.n_gpus_per_node=1 \
    trainer.nnodes=1 \
    trainer.save_freq=10 \
    trainer.test_freq=10 \
    trainer.total_epochs=15 2>&1 | tee verl_demo.log