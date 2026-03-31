import torch
import numpy as np
import os

# 1. 设置 12GB 原始文件的路径
src = "/home/xsuper/Binary-X/Models/Teacher_11B/T-Data-Oracle-11B.bin"
dst = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Native.pt"

print(f"Binary-X: 正在从 DGX 存储提取逻辑资产...")

try:
    # 核心操作：按照我们在探测中发现的“大端序”读取
    # dtype='>f2' 是解锁 12GB 数据的唯一钥匙
    raw = np.fromfile(src, dtype='>f2')
    
    # 搬运到 GB10 显存并转换为本地 Float16
    weights = torch.from_numpy(raw.astype(np.float16)).cuda()
    
    print(f"--- 逻辑核复活成功 ---")
    print(f"参数量: {weights.numel()} (约 64.4 亿)")
    print(f"均值自检: {weights.mean().item():.6f}")
    
    # 保存为 GB10 原生格式，从此告别 NaN
    torch.save(weights, dst)
    print(f"资产已存入原生格式: {dst}")

except Exception as e:
    print(f"复活失败: {e}")
