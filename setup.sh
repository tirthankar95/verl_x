#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv venv ../ai --python=python3.12.3 
source ~/ai/bin/activate
uv pip install -r requirements.txt
uv pip install flash-attn==2.8.0.post2 --no-build-isolation
python3 recipe/grid_dapo/prepare_data.py --style relax
python3 get_models.py
