import torch
print(f"torch版本: {torch.__version__}")
print(f"CUDA可用性: {torch.cuda.is_available()}")
print(f"当前设备编号: {torch.cuda.current_device()}")
print(f"当前设备信息: {torch.cuda.get_device_name()}")
