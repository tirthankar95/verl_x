import multiprocessing

try:
    multiprocessing.set_start_method("spawn", force=True)
except RuntimeError:
    pass
from collections import namedtuple
from pathlib import Path

import hydra
import pandas as pd
from omegaconf import DictConfig
from vllm import LLM, SamplingParams

from verl.utils.reward_score.grid_puzzle import compute_score

strategy = ["strict", "relax"]


def generate_with_vllm(prompt, llm, temperature=0.7, max_tokens=1024):
    if llm is None:
        raise RuntimeError("LLM instance is not provided.")
    sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
    outputs = llm.generate(prompt, sampling_params=sampling_params)
    for out in outputs:
        return out.outputs[0].text


def get_question(data) -> str:
    fin_prompt = ""
    roles = {"user", "assistant", "system", "ai"}
    for d in data:
        if d["role"].lower() in roles:
            fin_prompt += f"{d['role'].lower()}: {d['content']}\n"
    return fin_prompt


def get_ground_truth(x) -> str:
    return x["ground_truth"]


def generate(train_set: str, val_set: str, model_path: str):
    llm = LLM(
        model=model_path,
        max_model_len=16384,  # how many tokens the model can see at once (input + output)
        max_num_batched_tokens=8192,
        gpu_memory_utilization=0.8,
        dtype="float16",
    )
    DatasetBundle = namedtuple("DatasetBundle", ["data_name", "data_path"])
    datasets = [DatasetBundle(data_name="val", data_path=val_set), DatasetBundle(data_name="train", data_path=train_set)]
    for ds in datasets:
        df = pd.read_parquet(f"{ds.data_path}")
        df_res = pd.DataFrame()
        df_res["question"] = df["prompt"].apply(lambda x: get_question(x))
        df_res["ground_truth"] = df["reward_model"].apply(lambda x: get_ground_truth(x))
        df_res["response"] = df_res["question"].apply(lambda x: generate_with_vllm(x, llm)).astype(str)
        data_path = Path(ds.data_path)
        df_res.to_csv(str(data_path.parent / f"grid_{ds.data_name}.csv"))
        for s in strategy:
            df_res[f"reward_{s}"] = df_res.apply(lambda x, s=s: compute_score(x["response"], x["ground_truth"], extra_info={"strategy": s}), axis=1)
        df_res.to_csv(str(data_path.parent / f"grid_{ds.data_name}.csv"))


@hydra.main(version_base=None, config_path="config", config_name="dapo_trainer")
def main(cfg: DictConfig):
    generate(train_set=cfg["data"]["train_files"], val_set=cfg["data"]["val_files"], model_path=cfg["actor_rollout_ref"]["model"]["path"])


if __name__ == "__main__":
    main()
