#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv ai --python=python3.12.3 
mv ai ../
source ~/ai/bin/activate
uv pip install -r requirements.txt
uv pip install flash-attn==2.8.0.post2 --no-build-isolation
./recipe/dapo/prepare_dapo_data.sh & 
python3 get_models.py 
mv models ../
