import sys 
sys.path.append("/home/tmittra/verl_x/")
from verl.utils.tracking import Tracking 

config = {
    "project_name": "DAPO",
    "experiment_name": "Qwen-1.5B",
    "default_backend": ['console', 'mlflow']
}
if __name__ == '__main__':
    logger = Tracking(
        project_name=config['project_name'],
        experiment_name=config['experiment_name'],
        default_backend=config['default_backend']
    )
    logger.log(data={"best@32": 2, "mean@32": 1}, step=1)
    logger.log(data={"best@32": 4, "mean@32": 2}, step=2)
    