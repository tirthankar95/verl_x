import argparse
import os
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser(description="Provide configs to prepare your data.")
parser.add_argument(
    "--style",
    default="strict",
    help="Strategy to calculate reward.\n1. strict\n2. relax",
)
args = parser.parse_args()

HOME = Path.cwd()
# Original Grid Puzzle
file_id = "1w59yMfEU02j3oeY-5R7NZBge37HyBtNE"
# My Grid Puzzle
file_id = "1gSccd4b_1Oe5K66tLA8Ofs81CBGcLEAU"
RANDOM_STATE, TR_SPLIT = 1111, 0.8

os.makedirs("data", exist_ok=True)
url = f"https://drive.google.com/uc?id={file_id}"
if not os.path.exists(HOME / "data/grid_puzzle_easy.csv"):
    os.system(f"gdown '{url}' -O {HOME / 'data/grid_puzzle_easy.csv'}")
else:
    print("File exists.")

df = pd.read_csv(HOME / "data/grid_puzzle_easy.csv")
df_new = df[["question", "answer"]].copy()
df_new.rename(columns={"question": "prompt", "answer": "reward_model"}, inplace=True)
df_new["data_source"] = "grid_puzzle"
df_new["extra_info"] = [{"index": idx, "strategy": args.style} for idx in range(df.shape[0])]
df_new["prompt"] = df_new["prompt"].apply(lambda x: [{"role": "user", "content": x}])
df_new["reward_model"] = df_new["reward_model"].apply(lambda x: {"ground_truth": x})
# SHUFFLE
df_new = df_new.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
tr_index = int(df_new.shape[0] * TR_SPLIT) + 1
df_train, df_test = df_new[:tr_index], df_new[tr_index:]
df_train.to_parquet(HOME / "data/grid_train_easy.parquet", index=False)
df_test.to_parquet(HOME / "data/grid_test_easy.parquet", index=False)

# Verifying content.
df_test.to_csv(HOME / "data/verify.csv", index=False)
