# DragonSlayer 2.8GB
## ——Next-Generation AI Quantitative Model
> 🏆 **3rd Place** — 2026 NVIDIA DGX Spark Hackathon
> *Team project; see §5 for contributions.*
---

## 1. Project Overview

### 1.1 Project Name
**DragonSlayer 2.8GB**

### 1.2 Project Objectives
To build a **2.8GB ultra-lightweight financial large model** purpose-built for **0DTE (Zero Days to Expiration)** high-frequency trading scenarios. The project aims to break through the "high latency, high compute dependency" bottleneck of traditional large models, enabling localized, real-time trading decisions on edge devices (NVIDIA DGX Spark), with AI inference latency compressed to roughly the **25-millisecond** level for millisecond-scale trading.

### 1.3 Background & Pain Points
In 0DTE trading, market movements are measured in milliseconds and opportunity windows are fleeting. Current applications of AI in quantitative trading face three core pain points:

1. **The Speed Gap**: A single inference pass on traditional large models typically takes seconds (>5s), far exceeding the 0DTE tolerance threshold (<300ms) and causing strategies to fail.
2. **Resource Dependency**: High-performance models carry large VRAM footprints and often require cloud clusters, which introduces network latency and data-privacy risk.
3. **The Black Box of Trust**: The limited interpretability of deep models makes traders hesitant to commit capital decisions to AI.

### 1.4 Solution
DragonSlayer uses **two-stage knowledge distillation**, **extreme quantization**, and a **multi-agent collaboration framework** to compress a high-capability teacher model — trained on **4.5TB of financial corpora** — into a 2.8GB student model. It seeks to preserve a high degree of decision consistency while substantially reducing inference latency, and provides a transparent, auditable risk-control mechanism.

> **Note**: Performance figures in this document (e.g., decision consistency, speedup ratios) come from the project's internal test environment; methodology and control settings are in `/results`. Results may vary under different hardware and data conditions.

---

## 2. Highlights & Features

### 2.1 Core Highlights
- **Extreme Compression**: A two-stage distillation pipeline compresses the model along **4.5TB corpora → 12GB intermediate model → 2.8GB student model**, enabling a large model to run on edge devices.
- **Low-Latency Inference**: Core inference latency reduced from seconds to roughly the 25ms level, fitting the speed demands of high-frequency trading.
- **Decision Fidelity**: The student model aims to retain high decision consistency with the teacher on key trading signals (metrics and evaluation method in `/results`).
- **Local Deployment**: A local closed-loop deployment on NVIDIA DGX Spark keeps data on-site, reducing network latency and leakage risk.

### 2.2 Main Features
- **0DTE Real-Time Strategy Generation**: Generates Polars-based vectorized trading-factor code in real time for assets such as SPX, VIX, and NVDA.
- **Multi-Agent Risk Audit**: A built-in Reflection Agent mechanism — Oracle-Forger (strategy generation), Oathkeeper (risk audit), and X-Ray (VRAM monitoring) — performs safety and compliance checks on each trade.
- **Visualization Workstation**: A Streamlit-based interactive interface supporting asset allocation, strategy selection, latency monitoring, and instant code preview.
- **Dynamic VRAM Management**: Real-time monitoring of VRAM usage, locked within 2.8GB to prevent OOM (out-of-memory) crashes.

---

## 3. Technical Innovations

### 3.1 Algorithm: Two-Stage Knowledge Distillation
- **Stage 1 (Synthesis)**: Uses Nemotron-4 340B's SteerLM for Synthetic Data Generation (SDG) to build high-quality financial corpora, training an approximately **12GB intermediate teacher model**.
- **Stage 2 (Distillation & Pruning)**: Uses the **NVIDIA NeMo** framework locally for structural pruning and deep distillation, with **Qwen2.5-3B** as the student-model base, producing the ~**2.8GB** student model that retains core financial decision logic.

### 3.2 Representation Alignment in Segmented Distillation
Because the teacher model and intermediate data exceeded the single-machine memory limit for whole-model processing, the distillation used a **segmented** strategy: the model was split structurally and each segment distilled separately. This introduces a core technical challenge — **after independent distillation, each segment converges to its own representation space, so the vectors at segment boundaries fail to align; naive concatenation breaks at the seams, causing information loss and accuracy degradation**.

To address this, the project designed a **boundary-alignment ("edge-blurring") method**: softening and aligning the boundary regions of adjacent segments so they recombine into one coherent model rather than fracturing at the seams. This method is the key step for resolving accuracy loss under extreme compression.

> The problem definition, method details, and controlled experiments for this component constitute a relatively self-contained algorithmic research topic that can be studied independently.

### 3.3 Architecture: NVFP4 & GQA Fusion Engine
- **NVFP4/NVFP8 Quantization**: Adapted to the NVIDIA Blackwell architecture, using the next-generation 4-bit floating-point format to raise throughput while controlling precision loss.
- **GQA (Grouped-Query Attention)**: Optimizes the attention mechanism to reduce KV-Cache VRAM footprint, making long-context processing feasible under low-memory constraints.

### 3.4 System: Transparent Multi-Agent Pipeline
- **X-Ray Visualization**: Maps internal model state to readable metrics, mitigating the black-box trust problem.
- **Reflection Mechanism**: Introduces Actor (execution), Risk (governance), and Backtest (verification) agents for real-time checks, letting trade instructions self-audit within milliseconds.

---

## 4. NVIDIA Stack & Open Source Integration

The project integrates the NVIDIA full stack to leverage hardware performance:

| Component | Application & Contribution |
| --- | --- |
| **NVIDIA NeMo** | Core training framework, used for structural pruning, knowledge distillation, and fine-tuning. |
| **TensorRT-LLM** | Inference acceleration engine; implements NVFP4/NVFP8 quantization and kernel optimization to reduce latency. |
| **NVIDIA NIM** | Microservice deployment; packages the model as standardized containers for stability and scalability. |
| **NVIDIA DGX Spark** | Hardware foundation; Blackwell-based, providing local compute for the 2.8GB model. |
| **Open Source Models** | **Teacher**: Nemotron-4 340B (source of high-level financial capability); **Student Base**: Qwen2.5-3B (lightweight architectural foundation). |

---

## 5. Team Contributions

This project is an official entry for the **NVIDIA DGX Spark Hackathon**, completed collaboratively by a highly complementary, interdisciplinary team. Roles and core contributions are outlined below:

- 👑 **Amanda Chen | Project Lead / Algorithm Architect**
  * **Role**: Overall technical roadmap and architecture design; R&D and hyperparameter tuning of the two-stage knowledge distillation algorithm.
  * **Contribution**: Established the underlying 2.8GB compression strategy; independently proposed and implemented the **boundary-alignment ("edge-blurring") method for segmented distillation** (see §3.2), resolving the accuracy-loss and representation-mismatch problems of segment reassembly under extreme constraints.
- ⚡ **Connie Chen | Core Development Engineer**
  * **Role**: TensorRT-LLM kernel optimization, low-bit quantization implementation, and hardware-level acceleration.
  * **Contribution**: Implemented NVFP4/NVFP8 quantization and custom kernel tuning within TensorRT-LLM, driving end-to-end inference latency down to the **~25ms** level and maximizing Blackwell architecture throughput.
- 📊 **Yan Zhang | Data Engineering**
  * **Role**: High-quality financial corpora construction, data engineering, and instructional dataset curation.
  * **Contribution**: Built the Synthetic Data Generation (SDG) pipeline using Nemotron-4 340B's SteerLM, creating the foundational financial instruction dataset that supports the distilled student model's decision fidelity.
- 💻 **Hui Li | Full-Stack Development Engineer**
  * **Role**: Front-end workstation UX/UI development, back-end service architecture, and API integration.
  * **Contribution**: Delivered the Streamlit-based interactive workstation featuring asset allocation, instant Polars-based vectorized strategy code generation, latency monitoring, and real-time VRAM telemetry.
- ✍️ **Huiwen Wu | Technical Documentation & Compliance**
  * **Role**: Technical report writing, demo video production, open-source governance, and financial risk-control audit compliance.
  * **Contribution**: Maintained the completeness, accuracy, and professional presentation of all project deliverables, and helped align the multi-agent pipeline with quantitative compliance considerations.

---

## 6. Future Roadmap

- **Multi-Modal Fusion**: Introduce Vision-Language Models (VLM) so the model can directly read K-line charts and technical patterns, enriching decision dimensions.
- **Auto-Backtest Flywheel**: Build a closed-loop system that adjusts factor weights based on daily win rates for self-iterating strategies.
- **Mobile Ecosystem (NemoClaw)**: Plan a mobile app for monitoring runtime status and receiving key signals anywhere.
- **Domain Expansion**: Migrate the architecture to crypto perpetual contracts and forex markets to test generalizability and scalability.

---

*This project is a collaborative Hackathon entry. Member contributions are as described in §5.*
> [!NOTE]
> ### 📝 Infrastructure & Implementation Notice 
>
> * **🌐 Infrastructure:** The core training pipeline was developed and deployed on an **NVIDIA DGX Spark server** during the **2026 Hackathon**.
> * **💻 Script Purpose:** The scripts provided in this repository (`dragon_slayer.py`, `multi_agent_pipeline.py`) serve as **conceptual demonstrations** of the execution flow. They do not contain the full distributed training implementation.
> * **📦 Model Artifacts:** The final optimized models are maintained and hosted separately.
