import os 
import pandas as pd 
from pathlib import Path


HOME = Path.cwd()
file_id = "1w59yMfEU02j3oeY-5R7NZBge37HyBtNE"
RANDOM_STATE, TR_SPLIT = 1111, 0.8

os.makedirs("data", exist_ok=True)
url = f"https://drive.google.com/uc?id={file_id}"
os.system(f"gdown '{url}' -O {HOME/ 'data/GridPuzzle.csv'}")

df = pd.read_csv(HOME / "data/GridPuzzle.csv")
df_new = df[['question', 'answer']]
df_new = df_new.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
tr_index = int(df_new.shape[0] * TR_SPLIT) + 1
df_train, df_test = df_new[:tr_index], df_new[tr_index:]
df_train.to_parquet(HOME / "data/grid_train.parquet")
df_test.to_parquet(HOME / "data/grid_test.parquet")