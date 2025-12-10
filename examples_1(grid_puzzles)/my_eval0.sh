#!/usr/bin/env bash
set -xeuo pipefail

# Paths
RAY_DATA_HOME=${RAY_DATA_HOME:-"${HOME}/rlf-small-lm-grid-puzzles"}
MODEL_PATH=${MODEL_PATH:-"${HOME}/models/Qwen2-1.5B-Instruct"}
TRAIN_FILE=${TRAIN_FILE:-"${RAY_DATA_HOME}/data/grid_train.parquet"}
TEST_FILE=${TEST_FILE:-"${RAY_DATA_HOME}/data/grid_test_resp.parquet"}

# Hardware 
NUM_CPUS=8

python3 -m tm_tutorials.main_eval0 \
    data.path=$TEST_FILE \
    data.response_key=responses \
    data.data_source_key=prompt \
    data.reward_model_key=reward_model \
    reward_model.reward_manager=grid_puzzle \ 
    ray_init.num_cpus=$NUM_CPUS