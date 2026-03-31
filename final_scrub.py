import torch
import os

src = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Native.pt"
dst = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Final.pt"

print("Binary-X: 启动全量逻辑净化 (NaN + Inf)...")

try:
    weights = torch.load(src).cuda()
    
    # 1. 识别所有非有限值 (NaN, Inf, -Inf)
    invalid_mask = ~torch.isfinite(weights)
    invalid_count = invalid_mask.sum().item()
    total_count = weights.numel()
    
    print(f"--- 深度审计报告 ---")
    print(f"非法逻辑点 (NaN/Inf): {invalid_count}")
    print(f"总污染率: {(invalid_count / total_count) * 100:.6f}%")
    
    if invalid_count > 0:
        print("正在强制归零非法逻辑点...")
        weights[invalid_mask] = 0.0
    
    # 2. 最终统计自检
    final_mean = weights.mean().item()
    final_std = weights.std().item()
    
    print(f"--- 净化完成 ---")
    print(f"最终均值: {final_mean:.8f}")
    print(f"最终标准差: {final_std:.8f}")
    
    if torch.isnan(torch.tensor(final_mean)):
        print("警告: 均值仍为 NaN，可能存在底层硬件映射错误。")
    else:
        torch.save(weights, dst)
        print(f"Binary-X: 12GB 资产已完全脱毒，存入: {dst}")

except Exception as e:
    print(f"净化失败: {e}")
