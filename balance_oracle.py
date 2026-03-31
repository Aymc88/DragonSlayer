import torch
import os

src = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Final.pt"
dst = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Balanced.pt"

print("Binary-X: 正在执行权重压力平衡 (Weight Clipping)...")

try:
    weights = torch.load(src).cuda()
    
    # 1. 执行截断：将所有极端值限制在 [-3, 3] 之间
    # 这是一个经验值，能保留 99% 的有效交易逻辑，同时剔除噪声
    balanced_weights = torch.clamp(weights, min=-3.0, max=3.0)
    
    # 2. 最终统计自检
    final_mean = balanced_weights.mean().item()
    final_std = balanced_weights.std().item()
    
    print(f"--- 平衡报告 ---")
    print(f"平衡后均值: {final_mean:.6f}")
    print(f"平衡后标准差: {final_std:.6f}")
    
    torch.save(balanced_weights, dst)
    print(f"Binary-X: 12GB 资产已完成压力平衡，存入: {dst}")

except Exception as e:
    print(f"平衡失败: {e}")
