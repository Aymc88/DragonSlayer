# OFFICE HOURS: DragonSlayer 2.8GB Design Doc
**Author**: Antigravity (as YC Partner)
**Date**: 2026-04-19
**Project**: DragonSlayer 2.8GB
**Status**: APPROVED_WITH_CONCERNS (Design document approved, with open questions for live testing)

---

## 1. Executive Summary: The Thesis
**DragonSlayer 2.8GB** addresses the "Latency Gap" in LLM-assisted trading. Current massive LLMs (>100B params) are non-starters for high-frequency 0DTE (Zero Days to Expiration) options due to mult-second inference lag. 

**The Non-Obvious Truth**: High-fidelity financial intelligence can be distilled and quantised into a 2.8GB footprint without losing critical tactical edge, enabling **25ms inference** on edge devices like NVIDIA DGX Spark.

---

## 2. Core Architecture: The Multi-Agent Pipeline

The system is designed as a self-auditing triad on-device:

- **Oracle-Forger (The Brain)**: A distilled Minitron 4.5B-INT4 model optimized for 0DTE SPY/VIX volatility analysis.
- **Oathkeeper (The Auditor)**: A deterministic + heuristic risk-check agent that audits every signal against hard-coded safety parameters (Greeks limit, exposure caps).
- **X-Ray (The Monitor)**: Real-time VRAM and latency tracker ensuring zero-OOM (Out-of-Memory) and consistent execution speed.

---

## 3. Pivot: Transition to the Agentic Economy
Based on Office Hours discussions, the project is pivoting from a "Human-centric Trading Tool" to **"Infrastructure for AI Agents"**.

- **Customer**: Autonomous AI Agents (non-human traders) with capital to deploy.
- **Product**: **Trading Intuition API**. Agents outsource the low-latency signal finding and risk-auditing to DragonSlayer.
- **Delivery**: Locally deployed NIM containers or low-latency SDKs that treat DragonSlayer as a "co-processor" for financial decisions.

---

## 4. Key Premise Challenges & Mitigations

### Challenge: The 8% Accuracy Gap
- **Risk**: A distilled model (92% fidelity) might miss a catastrophic outlier event that the teacher model would have caught.
- **Mitigation**: Implement **"Hybrid Intelligence"**. The 2.8GB model acts as a high-speed Sentinel. For high-conviction trades over a certain $ threshold, the system triggers an asynchronous "Deep Review" by a larger 12GB teacher model.

### Challenge: Execution Overhead
- **Risk**: Generating Polars code at runtime adds parsing/execution latency.
- **Mitigation**: Shift from **Code Generation** to **Parameter Injection**. The model outputs weight-vectors and factor parameters fed into a pre-compiled Rust-based execution engine.

---

## 5. Monetization Strategy: The "Arm" Strategy
Instead of competing as a fund (Linear scaling) or a retail SaaS (Trust issues), DragonSlayer will follow the **Infrastucture Provider** route:
1. **Tier 1**: SDK License for independent AI Agent developers.
2. **Tier 2**: "Sovereign Node" rentals (Hardware + Software) for family offices and small quant shops.
3. **Tier 3**: Success-fee based on "Risk-Adjusted Alpha" provided to agent pools.

---

## 6. Mandatory Action Plan (The "Assignment")

### Phase 1: Distortion Audit (1 week)
- Compare the last 30 days of 0DTE SPY signals between the 4.5TB Teacher and 2.8GB Student.
- **Deliverable**: A heatmap of "Accuracy Loss" to identify if the 8% error is random noise or systemic bias.

### Phase 2: Total-Link Latency Test (2 weeks)
- Measure the **entire loop**: Tick data ingest -> DragonSlayer Inference -> Oathkeeper Audit -> API Order Placement.
- **Goal**: Ensure the "System-Wide Latency" remains under 150ms (inference target <25ms).

### Phase 3: Agentic API Alpha
- Wrap the model in a minimal `DragonSlayer-SDK`.
- **Deliverable**: A Python script where a "Dummy Agent" can get a "Trade/No-Trade" signal with risk analytics in one function call.

---

## 7. YC Partner Verdict
DragonSlayer has the technical "Schlep" YC loves. By moving toward the **Agentic Economy** and solving the **Latency/Size** bottleneck, this could become the "Financial Co-processor" for the next generation of autonomous finance.

> *"Fix the distortion, prove the link, and you have a billion-dollar infra company."*

---
**Status**: [DONE] ｜ Action Items assigned to Founder.
