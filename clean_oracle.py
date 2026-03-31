import torch
import os

src = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Native.pt"
dst = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Clean.pt"

print(f"Binary-X: 正在对原生资产执行“逻辑除汞”...")

try:
    # 直接从 GB10 显存加载
    weights = torch.load(src).cuda()
    
    # 1. 统计污染点
    nan_mask = torch.isnan(weights)
    nan_count = nan_mask.sum().item()
    total_count = weights.numel()
    pollution_rate = (nan_count / total_count) * 100
    
    print(f"--- 污染审计报告 ---")
    print(f"污染点数量: {nan_count}")
    print(f"污染率: {pollution_rate:.8f}%")
    
    if nan_count > 0:
        print("正在中和 NaN 坏点（重置为 0）...")
        # 将 NaN 替换为 0 (在 HFT 中，0 权重比 NaN 安全得多)
        weights[nan_mask] = 0.0
    
    # 2. 重新计算均值
    final_mean = weights.mean().item()
    final_std = weights.std().item()
    
    print(f"修正后均值: {final_mean:.6f}")
    print(f"修正后标准差: {final_std:.6f}")
    
    # 3. 存储纯净逻辑核
    torch.save(weights, dst)
    print(f"Binary-X: 纯净资产已存入: {dst}")

except Exception as e:
    print(f"清洗失败: {e}")
