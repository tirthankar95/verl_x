# rlf-small-lm-grid-puzzles

A research repository built on the [VERL framework](https://github.com/volcengine/verl) to explore fine-tuning small language models on grid-puzzle tasks. The project experiments with memory-efficient fine-tuning (LoRA), prompt engineering, and reward shaping to improve performance on grid puzzles.

## Key ideas
- **Template-based grid puzzles:** Small, reproducible puzzle datasets created to probe model reasoning.
- **Memory-efficient fine-tuning:** Use LoRA to reduce GPU memory requirements during training.
- **Reward shaping:** Design reward functions to mitigate sparse-reward problems in RL-style training.

## Prerequisites
- Python 3.12 and standard ML libraries (see `requirements.txt`).
- Terraform and an AWS account for the recommended full training runs.
- Sufficient GPU resources for model fine-tuning (the project uses LoRA to reduce but not eliminate memory needs).

## Quickstart (local overview)

1. Inspect main code and data

   - Puzzle data and example responses are in `recipe/grid_dapo` and `data/`.

2. Infrastructure (optional — recommended for full training)

   This repository includes Terraform configuration to provision AWS resources used for training. If you plan to run experiments on AWS, edit the Terraform files in `terraform-aws/` to point to your SSH `.pem` key and provide required secrets (e.g., Hugging Face token) as inputs.

   ```bash
   cd terraform-aws
   terraform init
   terraform apply
   # follow prompts and provide any required values (e.g. HF API key)
   ```

3. Connect to your provisioned instance

   After the instance is up, SSH into it (using your configured key). On the instance, set up Python and dependencies (or use the provided virtual environment layout). Example commands:

   ```bash
   # on the remote instance
   source ai/bin/activate
   ```

4. Run experiments

   The repository contains main recipe and scripts under `recipe/`. For the DAPO experiment (example):

   ```bash
   # start Ray on the head node (if using Ray)
   ray start --head
   
   cd rlf-small-lm-grid-puzzles

   # run the DAPO script (adjust path as needed)
   ./recipe/grid_dapo/my_dapo.sh
   ```

## Viewing results (MLflow)

Experiment runs are tracked with MLflow. The tracking URI is logged when runs start (example location shown in run logs below). To view results locally:
```logs
Example tacking uri log:
[TM] Tracking URI: file:/tmp/ray/session_2025-12-08_20-01-50_498060_3402/runtime_resources/working_dir_files/_ray_pkg_34596ddf3f0d3362/mlruns
```

1. Find the `mlruns` parent directory from the run logs (the code prints the tracking URI when it starts).
2. From the parent directory of `mlruns` run:

```bash
mlflow ui
# open http://localhost:5000 and select the relevant experiment (e.g. "DAPO")
```

Note: Run `mlflow ui` from the parent directory of `mlruns`, not from inside an `mlruns` subdirectory.

## Contents of interest
- `examples_1(grid_puzzles)/`: example scripts, training/eval pipelines, and sample responses.
- `recipe/grid_dapo/`: DAPO-related recipes and runner scripts.
- `GridPuzzleGenerator/`: Jupyter notebooks and generator code used to create puzzle datasets.
- `terraform-aws/`: Terraform configs used to provision AWS infrastructure for training.

## Contributing
- Issues and pull requests are welcome. For reproducibility, prefer small, self-contained changes and include instructions to reproduce results.

## Suggested next steps
- Create terraform script to launch ray cluster and run bigger language models.

## License
- This project follows the license in the repository root (`LICENSE`).

## Contact
- For questions about these experiments, open an issue or contact the maintainer in the repo.

