from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


# Step 1: Load the original model in float32
base_path = Path("/home/tmittra/models")
model_name = "Qwen2-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(str(base_path/model_name), torch_dtype=torch.float32)
tokenizer = AutoTokenizer.from_pretrained(str(base_path/model_name))

# Step 2: Convert model to float16
model = model.half()  # This converts model parameters to float16

# Step 3: Save the float16 model
output_dir = base_path / "Qwen2-1.5B-Instruct-fp16"
model.save_pretrained(output_dir, safe_serialization=True)
tokenizer.save_pretrained(output_dir)

print(f"Float16 model saved to {output_dir}")
