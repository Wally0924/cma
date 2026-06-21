"""Environment verification test for the CMA repo.

Checks: package versions, GPU compute on the actual device, import of all
project modules, and JIT-build + execution of the custom CUDA correlation op.
Run with the `cma` conda env active:  python -m tools.env_test
"""
import importlib
import sys


def section(t):
    print("\n" + "=" * 60 + f"\n{t}\n" + "=" * 60)


ok = True

section("1. Package versions")
import torch
import torchvision
import pytorch_lightning as pl
import torchmetrics
import numpy as np
import h5py
print("python        ", sys.version.split()[0])
print("torch         ", torch.__version__)
print("torchvision   ", torchvision.__version__)
print("pytorch_lightning", pl.__version__)
print("torchmetrics  ", torchmetrics.__version__)
print("numpy         ", np.__version__)
print("h5py          ", h5py.__version__)
assert np.__version__.startswith("1."), "numpy must be <2 for torch 2.0.1 ABI"

section("2. GPU compute on real device")
assert torch.cuda.is_available(), "CUDA not available!"
dev = torch.cuda.get_device_name(0)
cap = torch.cuda.get_device_capability(0)
print("device        ", dev, "sm_%d%d" % cap)
x = torch.randn(2048, 2048, device="cuda")
y = (x @ x).sum().item()  # real kernel launch on the GPU
torch.cuda.synchronize()
print("GPU matmul sum", round(y, 2), "-> kernel executed OK")

section("3. Import all project modules")
mods = [
    "tools.run",
    "models", "models.model", "models.utils", "models.losses",
    "models.backbones.resnet", "models.backbones.mix_transformer", "models.backbones.vgg",
    "models.heads.segformer", "models.heads.deeplabv2", "models.heads.uawarpc",
    "models.heads.projection", "models.heads.base", "models.heads.modules",
    "data_modules", "data_modules.combined_data_module", "data_modules.transforms",
    "data_modules.datasets.acdc", "data_modules.datasets.darkzurich",
    "data_modules.datasets.robotcar", "data_modules.datasets.acg",
    "helpers.metrics", "helpers.lr_scheduler", "helpers.pseudo_labels",
]
for m in mods:
    importlib.import_module(m)
    print("  imported", m)

section("4. JIT-build + run custom CUDA correlation extension")
from models.correlation_ops.correlation_function import spatial_correlation_sample
a = torch.randn(1, 8, 32, 32, device="cuda")
b = torch.randn(1, 8, 32, 32, device="cuda")
out = spatial_correlation_sample(a, b, kernel_size=1, patch_size=3,
                                 stride=1, padding=0, dilation=1, dilation_patch=1)
torch.cuda.synchronize()
print("correlation output shape:", tuple(out.shape), "-> CUDA extension OK")

section("ALL CHECKS PASSED")
