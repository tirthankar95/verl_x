import sys 
import os 
HOME = os.getcwd()
print(HOME)
sys.path.append(f"{HOME}")
from verl.trainer.main_ppo import create_rl_dataset
from verl.utils import hf_tokenizer
from pathlib import Path
from omegaconf import OmegaConf
from torchdata.stateful_dataloader import StatefulDataLoader
import torch 
from collections import defaultdict
import numpy as np 

TRAIN_FILE = Path(HOME) / "data/grid_train.parquet"
TEST_FILE = Path(HOME) / "data/grid_test.parquet"
MODEL_PATH = "/home/tmittra/models/Qwen2-1.5B-Instruct"

data = OmegaConf.create({
    "train_files": str(TRAIN_FILE),
    "val_files": str(TEST_FILE),
    "train_batch_size": 16,
    "max_prompt_length": 1024,
    "max_response_length": 256,
    "prompt_key": "prompt"
})

def collate_fn(data_list: list[dict]) -> dict:
    """
    Collate a batch of sample dicts into batched tensors and arrays.

    Args:
        data_list: List of dicts mapping feature names to torch.Tensor or other values.

    Returns:
        Dict where tensor entries are stacked into a torch.Tensor of shape
        (batch_size, *dims) and non-tensor entries are converted to
        np.ndarray of dtype object with shape (batch_size,).
    """
    tensors = defaultdict(list)
    non_tensors = defaultdict(list)
    '''
    data_list's length will be the batch size. 
    data_list's keys will be 'reward_model', 'input_ids', 'attention_mask', 'position_ids', 'raw_prompt_ids'
    1. input_ids: sentence tokens. 
    2. attention_mask: left padding 0, 0...1 
    3. position_ids: 0, 0 ... 341, 342, 343. 
    4. reward_model: array(['sol1', 'sol2', ...]) of strings [...], where each element is a solution.
    5. raw_prompt_ids: input_ids without the padding.
    6. index: [0, 0, 0, ...]
    7. tools_kwargs: [{}, {}, ...] no tools.
    '''
    for data in data_list:
        for key, val in data.items():
            if isinstance(val, torch.Tensor):
                tensors[key].append(val)
            else:
                non_tensors[key].append(val)

    for key, val in tensors.items():
        tensors[key] = torch.stack(val, dim=0)

    for key, val in non_tensors.items():
        non_tensors[key] = np.array(val, dtype=object)

    return {**tensors, **non_tensors}

if __name__ == "__main__":
    tokenizer = hf_tokenizer(MODEL_PATH)
    train_dataset = create_rl_dataset(str(TRAIN_FILE), data, tokenizer, None)
    '''
    As a referesher, here is roughly how dataloading works in torch.utils.data.DataLoader: DataLoader begins by generating indices from a sampler and creates batches of batch_size indices. 
    If no sampler is provided, then a RandomSampler or SequentialSampler is created by default. 
    The indices are passed to Dataset.__getitem__(), and then a collate_fn is applied to the batch of samples. 
    If num_workers > 0, it will use multi-processing to create subprocesses, and pass the batches of indices to the worker processes, who will then call Dataset.__getitem__() and apply collate_fn before returning the batches to the main process. 
    At that point, pin_memory may be applied to the tensors in the batch.    
    '''
    train_loader = StatefulDataLoader(
        dataset=train_dataset,
        batch_size=data.train_batch_size,
        num_workers=data.get("dataloader_num_workers", 8),
        collate_fn=collate_fn
    )
    for batch in train_loader:
        print(batch)
        break