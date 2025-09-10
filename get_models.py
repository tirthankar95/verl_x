import os
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import hf_hub_download, list_repo_files

my_token = os.getenv('HF_TOKEN', '')
home = os.path.expanduser('~')

def get_model(repo_id, local_dir):
    filenames = list_repo_files(repo_id)
    for filename in filenames:
        print(hf_hub_download(repo_id = repo_id, \
                              local_dir = local_dir, \
                              token = my_token,
                              filename=f"{filename}"))

if __name__ == '__main__':
    config = {
        "repo_id": "Qwen/Qwen2-1.5B-Instruct",
        "local_dir" : f"{home}/models/Qwen2-1.5B-Instruct"
    }
    '''
    config = {
        "repo_id": "Qwen/Qwen3-4B",
        "local_dir" : f"{home}/models/Qwen3-4B"
    }
    config = {
        "repo_id": "openai-community/gpt2",
        "local_dir": f"{home}/models/gpt2"
    }
    '''
    get_model(repo_id = config['repo_id'], \
              local_dir = config['local_dir'])
