import os
from transformers import AutoTokenizer

# 1. 强制使用镜像源绕过网络封锁
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

model_id = "Qwen/Qwen2-7B-Instruct"
save_dir = "/home/xsuper/Binary-X/Models/Teacher_11B/Final_Brain"

print(f"Binary-X: 正在从镜像站拉取 {model_id} 的分词器逻辑...")

try:
    # 仅下载分词器，不下载庞大的权重
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    tokenizer.save_pretrained(save_dir)
    print(f"--- 补齐成功 ---")
    print(f"分词器组件已存入: {save_dir}")
except Exception as e:
    print(f"下载失败: {e}")
