import sys 
import os 
sys.path.append(f"{os.getcwd()}")
import torch 
import ray 
from verl.single_controller.base import Worker 
from verl.single_controller.ray.base import RayClassWithInitArgs, RayWorkerGroup, RayResourcePool, merge_resource_pool

ray.init()
# resource_pool = RayResourcePool([4], use_gpu=True) -> For this you need 4 workers each with [10 CPU, 1 GPU]
resource_pool = RayResourcePool([1], use_gpu=False, max_colocate_count=os.cpu_count())

@ray.remote
class GPUAccumulator(Worker):
    def __init__(self) -> None:
        super().__init__()
        self.value = torch.zeros(size=(1,), device='cpu') + self.rank 
    def add(self, x):
        self.value += x 
        print(f'rank {self.rank}, value: {self.value}')
        self.value.cpu()

cls_with_args = RayClassWithInitArgs(cls=GPUAccumulator)
worker_group = RayWorkerGroup(resource_pool, cls_with_args)
# print(worker_group.execute_all_sync("add", [1, 1, 1, 1])) -> For this you need 4 workers each with [10 CPU, 1 GPU]
worker_group.execute_all_sync("add", [1]) # The first value in the list is passed to worker1, second to worker2, etc. 
print(f'World Size: {worker_group.world_size}') # How many worker nodes.


from verl.single_controller.base.decorator import register, Dispatch
@ray.remote
class GPUAccumulatorDecorator(Worker):
    def __init__(self) -> None:
        super().__init__()
        # The initial value of each rank is the same as the rank
        self.value = torch.zeros(size=(1,), device="cpu") + self.rank

    # map from a single input to all the worker
    @register(Dispatch.ONE_TO_ALL)
    def add(self, x):
        self.value = self.value + x
        print(f"rank {self.rank}, value: {self.value}")
        return self.value.cpu()
    
class_with_args = RayClassWithInitArgs(cls=GPUAccumulatorDecorator)
gpu_accumulator_decorator = RayWorkerGroup(resource_pool, class_with_args)
# Dispatch one value to all workers, since we have only one worker you won't notice the difference.
print(gpu_accumulator_decorator.add(x=5))