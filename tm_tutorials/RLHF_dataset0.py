import sys 
HOME = "/home/tmittra/verl_x"
sys.path.append(f"{HOME}")
from verl.trainer.main_ppo import create_rl_dataset
from verl.utils import hf_tokenizer
from pathlib import Path
from omegaconf import OmegaConf
from torchdata.stateful_dataloader import StatefulDataLoader

TRAIN_FILE = Path(HOME) / "data/grid_train.parquet"
TEST_FILE = Path(HOME) / "data/grid_test.parquet"
MODEL_PATH = "/home/tmittra/models/Qwen2-1.5B-Instruct"

data = OmegaConf.create({
    "train_files": str(TRAIN_FILE),
    "val_files": str(TEST_FILE),
    "train_batch_size": 32,
    "max_prompt_length": 1024,
    "max_response_length": 256,
    "prompt_key": "prompt"
})

if __name__ == "__main__":
    tokenizer = hf_tokenizer(MODEL_PATH)
    train_dataset = create_rl_dataset(str(TRAIN_FILE), data, tokenizer, None)
    train_loader = StatefulDataLoader(
        dataset=train_dataset,
        batch_size=data.train_batch_size,
        num_workers=data.get("dataloader_num_workers", 8),
        shuffle=True
    )
    for batch in train_loader:
        print(batch)
        break