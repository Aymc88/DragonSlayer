# T-data: Binary-X Multi-Agent Distillation System

> **A high-performance AI model distillation and inference platform powered by NVIDIA DGX Spark.**

---

## 📖 Project Overview

**T-data** is a research-grade AI system built on the **Binary-X** architecture, implementing a multi-agent Teacher-Student knowledge distillation pipeline. The project leverages the computational power of the NVIDIA DGX Spark server to compress and deploy large language model capabilities into efficient, deployable inference units.

### Core Concept
```
Teacher Model (11B) ──distillation──▶ Student Model ──deploy──▶ Real-world Inference
```

---

## 🏗️ Architecture

```
DGX Spark/
├── multi_agent_pipeline.py    # Core multi-agent distillation orchestrator
├── distillation_dashboard.py  # Real-time training monitoring dashboard  
├── dragon_slayer.py           # DragonSlayer inference engine
├── dragonslayer_web.py        # Web-based monitoring interface
├── balance_oracle.py          # Resource balance monitoring
├── clean_oracle.py            # Data cleaning pipeline
├── final_scrub.py             # Final data preprocessing stage
├── get_tokenizer.py           # Tokenizer extraction utility
├── rebuild_qwen.py            # Qwen model rebuild & fine-tuning
├── revive_now.py              # Model revival & checkpoint recovery
├── templates/                 # Web dashboard HTML templates
└── home/xsuper/Binary-X/      # Binary-X model assets (not uploaded)
    └── Models/
        └── Teacher_11B/
            └── Final_Brain/   # Tokenizer configs (see Download section)
```

---

## ⚙️ System Requirements

| Component | Specification |
|-----------|--------------|
| **Server** | NVIDIA DGX Spark |
| **OS** | Ubuntu 22.04 / Linux (aarch64) |
| **GPU** | NVIDIA Integrated GPU (DGX Spark) |
| **RAM** | 64GB+ recommended |
| **Storage** | 4TB+ NVMe |
| **Python** | 3.10+ |

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/T-data.git
cd T-data

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Model Weights
> ⚠️ Model weights are **not included** in this repository due to file size constraints.
> Please download separately:
> - **Teacher_11B (Final_Brain)**: [Coming Soon / Contact Author]
> - Place downloaded files under: `home/xsuper/Binary-X/Models/Teacher_11B/Final_Brain/`

### 3. Run the Distillation Pipeline
```bash
# Launch the multi-agent distillation pipeline
python3 multi_agent_pipeline.py

# Monitor via web dashboard (separate terminal)
python3 dragonslayer_web.py
# Visit: http://localhost:8000
```

---

## 🧠 Key Components

### `multi_agent_pipeline.py`
The core orchestration engine that coordinates multiple AI agents through the Binary-X distillation process. Implements teacher-student knowledge transfer at scale.

### `dragon_slayer.py` / `dragonslayer_web.py`
The **DragonSlayer** inference and visualization system. Provides:
- Real-time model performance metrics
- Web-based control panel
- Multi-agent task allocation monitoring

### `distillation_dashboard.py`
Training progress dashboard with:
- Loss curve visualization
- Agent load balancing stats
- Resource utilization metrics

---

## 📊 Project Status

| Module | Status |
|--------|--------|
| Multi-Agent Pipeline | ✅ Operational |
| DragonSlayer Engine | ✅ Operational |
| Web Dashboard | ✅ Operational |
| Tokenizer Utilities | ✅ Operational |
| Model Weights | 🔒 Private / On-Request |

---

## 🔗 Related Projects
- **Alpaca MCP Trading System** *(Coming Soon)* — Financial trading agent built on top of T-data's inference core
- **OpenClaw Integration** *(Planned)* — Extended agent framework integration

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Wii Che**  
DGX Spark Research Platform  
*Built with NVIDIA DGX Spark + Binary-X Architecture*

---

*"The Dragon Awakens" — T-data v1.0*
