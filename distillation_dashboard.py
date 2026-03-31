from flask import Flask, render_template, jsonify
import math
import time
import random

app = Flask(__name__)

# 全局变量记录点火时间 (模拟蒸馏开始)
START_TIME = time.time()
TOTAL_ITERATIONS = 50000
ITERATIONS_PER_SEC = 25  # 为了在视觉上能够快速感受到进度（如果是真实的 1it/s 则太慢）

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/telemetry")
def get_telemetry():
    elapsed = time.time() - START_TIME
    
    # 动态推演进度
    current_step = int(elapsed * ITERATIONS_PER_SEC)
    if current_step > TOTAL_ITERATIONS:
        current_step = TOTAL_ITERATIONS
    
    # 模拟 KL 散度下降：指数衰减 + 震荡噪声
    # 起始为 3.45，最终趋近于 0.01 左右
    kl_loss = max(0.01, 3.45 * math.exp(-current_step / 8000.0) + random.uniform(-0.02, 0.05))
    
    # 交叉熵损失 (CE) 下降较慢但稳定
    ce_loss = max(0.05, 1.25 * math.exp(-current_step / 15000.0) + random.uniform(-0.01, 0.02))
    
    # Cosine Annealing 学习率曲线
    min_lr = 1e-6
    max_lr = 2e-5
    lr = min_lr + 0.5 * (max_lr - min_lr) * (1 + math.cos(math.pi * current_step / TOTAL_ITERATIONS))
    
    # 模拟硬件读数变化
    gpu_util = random.randint(96, 100)
    temp = 73 + random.uniform(-1, 2)
    vram = 2.84 + random.uniform(-0.03, 0.05)
    
    # 返回给前端画图
    return jsonify({
        "step": current_step,
        "total": TOTAL_ITERATIONS,
        "percentage": round(current_step / TOTAL_ITERATIONS * 100, 2),
        "kl_loss": round(kl_loss, 4),
        "ce_loss": round(ce_loss, 4),
        "lr": f"{lr:.2e}",
        "gpu_util": gpu_util,
        "temperature": round(temp, 1),
        "vram": round(vram, 2)
    })

if __name__ == "__main__":
    # 本地跑在 5050 端口
    app.run(host="0.0.0.0", port=5050, debug=False)
