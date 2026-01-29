import os
from pathlib import Path

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

print("Saving merged model...")
MODEL_DIR = Path(f"{os.path.expanduser('~')}") / "models"
MODEL_NAME = "Qwen2.5-1.5B-Instruct"
ADAPTER_NAME = "adapter"

model_dir = MODEL_DIR / MODEL_NAME
merged_dir = MODEL_DIR / (MODEL_NAME + "_merged")
adapter_dir = MODEL_DIR / ADAPTER_NAME

tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir)
model = PeftModel.from_pretrained(model, adapter_dir)
model = model.merge_and_unload()
model.save_pretrained(merged_dir)
tokenizer.save_pretrained(merged_dir)
