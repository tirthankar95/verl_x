from torch.distributed.device_mesh import init_device_mesh
import torch 
import os 

is_cuda_available = torch.cuda.is_available()
is_npu_available = False 

def get_nccl_backend() -> str:
    """Return nccl backend type based on the device type.
    Returns:
        nccl backend type string.
    """
    if is_cuda_available:
        return "nccl"
    elif is_npu_available:
        return "hccl"
    else:
        raise RuntimeError(f"No available nccl backend found on device type {get_device_name()}.")

def get_device_name() -> str:
    """Function that gets the torch.device based on the current machine.
    This currently only supports CPU, CUDA, NPU.
    Returns:
        device
    """
    if is_cuda_available:
        device = "cuda"
    elif is_npu_available:
        device = "npu"
    else:
        device = "cpu"
    return device


if __name__ == '__main__':
        os.environ["MASTER_ADDR"] = "localhost"
        os.environ["MASTER_PORT"] = "29500"
        import torch.distributed

        if not torch.distributed.is_initialized():
            rank = int(os.environ.get("RANK", 0))
            world_size = int(os.environ.get("WORLD_SIZE", 1))
            torch.distributed.init_process_group(backend=f"cpu:gloo,{get_device_name()}:{get_nccl_backend()}", rank=rank, world_size=world_size)

        # build device mesh for FSDP
        world_size = torch.distributed.get_world_size()

        # build device mesh for Ulysses Sequence Parallel
        ulysses_device_mesh = None
        ulysses_sequence_parallel_size = 1
        dp = world_size // ulysses_sequence_parallel_size
        ulysses_device_mesh = init_device_mesh(get_device_name(), mesh_shape=(dp, ulysses_sequence_parallel_size), mesh_dim_names=["dp", "sp"])