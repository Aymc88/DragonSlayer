import torch
from transformers import Qwen2Config, Qwen2ForCausalLM
import os

# 1. 定义 Qwen2-7B 标准配置
config = Qwen2Config(
    vocab_size=152064,
    hidden_size=3584,
    intermediate_size=18944,
    num_hidden_layers=28,
    num_attention_heads=28,
    num_key_value_heads=4,
    torch_dtype="float16"
)

src_path = "/home/xsuper/Binary-X/Models/Teacher_11B/Teacher_Balanced.pt"
dst_model_dir = "/home/xsuper/Binary-X/Models/Teacher_11B/Final_Brain"

print("Binary-X: 正在启动逻辑器官重构...")

try:
    # 2. 在 GB10 显存中初始化空壳模型
    with torch.device("cuda:0"):
        model = Qwen2ForCausalLM(config).half()
    
    # 3. 加载 12GB 纯净逻辑流
    print("加载平衡后的 1D 逻辑核...")
    flat_weights = torch.load(src_path).cuda()
    
    # 4. 执行“手术”：将 1D 权重按顺序填充到 state_dict 中
    print("正在进行神经元层级映射 (Neuron Mapping)...")
    current_pos = 0
    state_dict = model.state_dict()
    
    for key in state_dict.keys():
        param_shape = state_dict[key].shape
        param_size = state_dict[key].numel()
        
        # 从扁平流中切出对应大小的块，并重塑形状
        if current_pos + param_size <= flat_weights.numel():
            sliced_weight = flat_weights[current_pos : current_pos + param_size].view(param_shape)
            state_dict[key].copy_(sliced_weight)
            current_pos += param_size
        else:
            print(f"警告: 权重流在 {key} 处耗尽")
            break

    # 5. 保存完整架构模型
    print(f"重组完成。映射了 {current_pos} 个参数。")
    model.save_pretrained(dst_model_dir)
    print(f"Binary-X: 12GB 完整大脑已就绪，存入: {dst_model_dir}")

except Exception as e:
    print(f"重组失败: {e}")
