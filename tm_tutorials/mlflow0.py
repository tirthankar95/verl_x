import os 
import mlflow 

'''
Checks if MLFLOW_TRACKING_URI environment variable exists
If it does, sets MLflow to use that tracking server
If not, MLflow uses the default local tracking (stores in ./mlruns directory)
'''
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", None)
if MLFLOW_TRACKING_URI:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

PROJECT_NAME = "dummy_project"
EXPERIMENT_NAME = "exp1"

'''
Sets the experiment name to "dummy_project"
mlflow.set_experiment() either finds an existing experiment with that name or creates a new one
Returns an experiment object
'''
experiment = mlflow.set_experiment(PROJECT_NAME)
mlflow.start_run(experiment_id=experiment.experiment_id, run_name=EXPERIMENT_NAME)
mlflow.log_metric('Accuracy', 0.7)
mlflow.log_metrics(metrics={'Loss': 4}, step=1)
mlflow.log_metrics(metrics={'Loss': 2}, step=2)
mlflow.end_run()