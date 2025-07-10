import wandb

# Initialize a new wandb run
wandb.init(project="dummy-project")

# Log a metric
for step in range(10):
    wandb.log({"accuracy": 0.8 + 0.01 * step, "step": step})

# Finish the run
wandb.finish()
