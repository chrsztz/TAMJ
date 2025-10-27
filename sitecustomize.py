# sitecustomize.py
import torch
import types
from contextlib import contextmanager

# 没有 MPS 就直接提示
if not torch.backends.mps.is_available():
    print("[sitecustomize] MPS 不可用。请使用 macOS + Apple Silicon + PyTorch>=1.12/2.x，并确保在非 Rosetta 环境下安装 torch。")

# ---- 1) 把常见的 .cuda() 调用重定向到 MPS ----
_orig_tensor_to = torch.Tensor.to

def _to_mps_if_cuda(self, *args, **kwargs):
    # 兼容: x.to("cuda"), x.to(torch.device("cuda")), x.to(device="cuda:0")
    def _map(dev):
        if isinstance(dev, str) and dev.startswith("cuda"):
            return "mps"
        if isinstance(dev, torch.device) and dev.type == "cuda":
            return torch.device("mps")
        return dev

    if args:
        args = list(args)
        args[0] = _map(args[0])
        args = tuple(args)
    if "device" in kwargs:
        kwargs["device"] = _map(kwargs["device"])
    return _orig_tensor_to(self, *args, **kwargs)

torch.Tensor.to = _to_mps_if_cuda

def _tensor_cuda(self, *args, **kwargs):
    # 兼容 x.cuda() / x.cuda(non_blocking=True)
    return _orig_tensor_to(self, device="mps", **kwargs)

torch.Tensor.cuda = _tensor_cuda

# nn.Module.cuda() -> .to("mps")
_orig_module_to = torch.nn.Module.to
def _module_cuda(self, device=None, **kwargs):
    return _orig_module_to(self, device="mps", **kwargs)
torch.nn.Module.cuda = _module_cuda

# ---- 2) 覆盖 torch.cuda 常用接口，指向 MPS / no-op ----
# 注意: torch.cuda 是个模块，这里只“局部重写”常用属性/方法
def _cuda_is_available():
    # 让代码里 if torch.cuda.is_available() 走 True
    return torch.backends.mps.is_available()

def _cuda_device_count():
    return 1 if torch.backends.mps.is_available() else 0

def _cuda_current_device():
    return 0

def _cuda_get_device_name(index=0):
    return "mps"

def _cuda_empty_cache():
    # MPS 没有 empty_cache；保持兼容即可
    pass

def _cuda_synchronize(device=None):
    if hasattr(torch, "mps") and hasattr(torch.mps, "synchronize"):
        torch.mps.synchronize()

@contextmanager
def _cuda_device(dev):
    # 忽略 "cuda:0" 等，转为 mps 的空上下文
    yield

# 将这些方法挂到 torch.cuda 上：
torch.cuda.is_available   = _cuda_is_available
torch.cuda.device_count   = _cuda_device_count
torch.cuda.current_device = _cuda_current_device
torch.cuda.get_device_name= _cuda_get_device_name
torch.cuda.empty_cache    = _cuda_empty_cache
torch.cuda.synchronize    = _cuda_synchronize
torch.cuda.device         = _cuda_device

# ---- 3) 默认设备改为 MPS（PyTorch 2.1+ 支持）----
if hasattr(torch, "set_default_device"):
    try:
        torch.set_default_device("mps")
    except Exception:
        pass

print("[sitecustomize] 已启用 MPS 兼容层：.cuda()/torch.cuda/* 将尽量路由到 MPS。")
