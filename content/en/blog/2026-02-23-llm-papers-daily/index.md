---
title: "LLM Papers Survey (2026-02-23)"
subtitle: ""
summary: " "
tags: ["LLM", "AI", "論文"]
categories: ["LLM", "AI", "論文"]
url: llm-papers-2026-02-23
date: 2026-02-23
featured: false
draft: false
---

## Introduction

This article summarizes notable LLM-related papers as of 2026-02-23. Papers are automatically collected from arXiv, Semantic Scholar, and Hugging Face Daily Papers, with Japanese summaries generated using the Claude API.

## 1. VESPO: Variational Sequence-Level Soft Policy Optimization for Stable Off-Policy LLM Training

- **Authors**: Guobin Shen, Chenghao Zhao, Xiang Cheng, Lei Huang, Xing Yu
- **Published**: 2026-02-11
- **Source**: [huggingface](https://arxiv.org/abs/2602.10693)
- **arXiv ID**: 2602.10693

### Summary

This research addresses training stability challenges in reinforcement learning for large language models (LLMs). Policy staleness, asynchronous training, and mismatches between training and inference engines cause the behavior policy to diverge from the current policy, risking training collapse. The paper proposes VESPO (Variational sEquence-level Soft Policy Optimization), which incorporates variance reduction into a variational formulation over proposal distributions and derives a closed-form reshaping kernel that operates directly on sequence-level importance weights without length normalization. Experiments on mathematical reasoning benchmarks show VESPO maintains stable training under staleness ratios up to 64x and fully asynchronous execution, delivering consistent gains across both dense and Mixture-of-Experts models.

{{< details "Original Abstract" >}}
Training stability remains a central challenge in reinforcement learning (RL) for large language models (LLMs). Policy staleness, asynchronous training, and mismatches between training and inference engines all cause the behavior policy to diverge from the current policy, risking training collapse. Importance sampling provides a principled correction for this distribution shift but suffers from high variance; existing remedies such as token-level clipping and sequence-level normalization lack a unified theoretical foundation. We propose Variational sEquence-level Soft Policy Optimization (VESPO). By incorporating variance reduction into a variational formulation over proposal distributions, VESPO derives a closed-form reshaping kernel that operates directly on sequence-level importance weights without length normalization. Experiments on mathematical reasoning benchmarks show that VESPO maintains stable training under staleness ratios up to 64x and fully asynchronous execution, and delivers consistent gains across both dense and Mixture-of-Experts models. Code is available at https://github.com/FloyedShen/VESPO
{{< /details >}}

## 2. Does Your Reasoning Model Implicitly Know When to Stop Thinking?

- **Authors**: Zixuan Huang, Xin Xia, Yuxi Ren, Jianbin Zheng, Xuanda Wang et al.
- **Published**: 2026-02-09
- **Source**: [huggingface](https://arxiv.org/abs/2602.08354)
- **arXiv ID**: 2602.08354

### Summary

Large reasoning models (LRMs) have improved performance on complex reasoning tasks through long chains of thought (CoT), but redundant reasoning impairs computational efficiency and causes delays in real-time applications. Prior research shows that longer reasoning chains don't necessarily improve accuracy and can even be detrimental. This study discovers and empirically verifies that LRMs implicitly know the appropriate time to stop thinking, but current sampling paradigms obscure this capability. Based on this finding, the paper proposes SAGE (Self-Aware Guided Efficient Reasoning), a novel sampling approach, and further integrates SAGE into group-based reinforcement learning (SAGE-RL), demonstrating significant improvements in both reasoning accuracy and efficiency across multiple mathematical benchmarks.

{{< details "Original Abstract" >}}
Recent advancements in large reasoning models (LRMs) have greatly improved their capabilities on complex reasoning tasks through Long Chains of Thought (CoTs). However, this approach often results in substantial redundancy, impairing computational efficiency and causing significant delays in real-time applications. Recent studies show that longer reasoning chains are frequently uncorrelated with correctness and can even be detrimental to accuracy. In a further in-depth analysis of this phenomenon, we surprisingly uncover and empirically verify that LRMs implicitly know the appropriate time to stop thinking, while this capability is obscured by current sampling paradigms. Motivated by this, we introduce SAGE (Self-Aware Guided Efficient Reasoning), a novel sampling paradigm that unleashes this efficient reasoning potential. Furthermore, integrating SAGE as mixed sampling into group-based reinforcement learning (SAGE-RL) enables SAGE-RL to effectively incorporate SAGE-discovered efficient reasoning patterns into standard pass@1 inference, markedly enhancing both the reasoning accuracy and efficiency of LRMs across multiple challenging mathematical benchmarks.
{{< /details >}}

## 3. SLA2: Sparse-Linear Attention with Learnable Routing and QAT

- **Authors**: Jintao Zhang, Haoxu Wang, Kai Jiang, Kaiwen Zheng, Youhe Jiang et al.
- **Published**: 2026-02-13
- **Source**: [huggingface](https://arxiv.org/abs/2602.12675)
- **arXiv ID**: 2602.12675

### Summary

Sparse-Linear Attention (SLA) combines sparse and linear attention to accelerate diffusion models, but has two issues: heuristic splitting that can be suboptimal, and a mismatch between SLA's attention error and a direct decomposition into sparse and linear attention. The proposed SLA2 introduces: a learnable router that dynamically selects whether each attention computation uses sparse or linear attention; a more faithful formulation combining sparse and linear attention branches with a learnable ratio; and a sparse + low-bit attention design via quantization-aware fine-tuning. Experiments on video diffusion models show SLA2 achieves 97% attention sparsity with an 18.6x attention speedup while preserving generation quality.

{{< details "Original Abstract" >}}
Sparse-Linear Attention (SLA) combines sparse and linear attention to accelerate diffusion models and has shown strong performance in video generation. However, (i) SLA relies on a heuristic split that assigns computations to the sparse or linear branch based on attention-weight magnitude, which can be suboptimal. Additionally, (ii) after formally analyzing the attention error in SLA, we identify a mismatch between SLA and a direct decomposition into sparse and linear attention. We propose SLA2, which introduces (I) a learnable router that dynamically selects whether each attention computation should use sparse or linear attention, (II) a more faithful and direct sparse-linear attention formulation that uses a learnable ratio to combine the sparse and linear attention branches, and (III) a sparse + low-bit attention design, where low-bit attention is introduced via quantization-aware fine-tuning to reduce quantization error. Experiments on video diffusion models show that on video diffusion models, SLA2 can achieve 97% attention sparsity and deliver an 18.6x attention speedup while preserving generation quality.
{{< /details >}}

## 4. SpargeAttention2: Trainable Sparse Attention via Hybrid Top-k+Top-p Masking and Distillation Fine-Tuning

- **Authors**: Jintao Zhang, Kai Jiang, Chendong Xiang, Weiqi Feng, Yuezhou Hu et al.
- **Published**: 2026-02-13
- **Source**: [huggingface](https://arxiv.org/abs/2602.13515)
- **arXiv ID**: 2602.13515

### Summary

The paper proposes SpargeAttention2, a trainable sparse attention method for accelerating diffusion models. It analyzes failure cases for two common masking rules (Top-k and Top-p) and achieves robust masking at high sparsity by combining them into a hybrid masking approach. It also points out limitations of fine-tuning with diffusion loss and introduces a distillation-based fine-tuning objective to maintain generation quality. Experiments on video diffusion models demonstrate 95% attention sparsity with 16.2x attention speedup while maintaining generation quality, consistently outperforming existing sparse attention methods.

{{< details "Original Abstract" >}}
Many training-free sparse attention methods are effective for accelerating diffusion models. Recently, several works suggest that making sparse attention trainable can further increase sparsity while preserving generation quality. We study three key questions: (1) when do the two common masking rules, i.e., Top-k and Top-p, fail, and how can we avoid these failures? (2) why can trainable sparse attention reach higher sparsity than training-free methods? (3) what are the limitations of fine-tuning sparse attention using the diffusion loss, and how can we address them? Based on this analysis, we propose SpargeAttention2, a trainable sparse attention method that achieves high sparsity without degrading generation quality. SpargeAttention2 includes (i) a hybrid masking rule that combines Top-k and Top-p for more robust masking at high sparsity, (ii) an efficient trainable sparse attention implementation, and (iii) a distillation-inspired fine-tuning objective to better preserve generation quality during fine-tuning using sparse attention. Experiments on video diffusion models show that SpargeAttention2 reaches 95% attention sparsity and a 16.2x attention speedup while maintaining generation quality, consistently outperforming prior sparse attention methods.
{{< /details >}}

## 5. Mobile-Agent-v3.5: Multi-platform Fundamental GUI Agents

- **Authors**: Haiyang Xu, Xi Zhang, Haowei Liu, Junyang Wang, Zhaozai Zhu et al.
- **Published**: 2026-02-15
- **Source**: [huggingface](https://arxiv.org/abs/2602.16855)
- **arXiv ID**: 2602.16855

### Summary

GUI-Owl-1.5 is a native GUI agent model supporting multiple platforms including desktop, mobile, and browser. It offers instruct/thinking variants in multiple sizes from 2B to 235B, enabling cloud-edge collaboration and real-time interaction. It achieves state-of-the-art performance as an open-source model on 20+ GUI benchmarks including OSWorld (56.5), AndroidWorld (71.6), WebArena (48.4), and ScreenSpotPro (80.3). Key innovations include a hybrid data flywheel combining simulated and cloud sandbox environments, a unified thought synthesis pipeline enhancing agent capabilities (including tool/MCP use, memory, and multi-agent adaptation), and a new environment RL algorithm MRPO addressing multi-platform conflicts and low training efficiency of long-horizon tasks.

{{< details "Original Abstract" >}}
The paper introduces GUI-Owl-1.5, the latest native GUI agent model that features instruct/thinking variants in multiple sizes (2B/4B/8B/32B/235B) and supports a range of platforms (desktop, mobile, browser, and more) to enable cloud-edge collaboration and real-time interaction. GUI-Owl-1.5 achieves state-of-the-art results on more than 20+ GUI benchmarks on open-source models: (1) on GUI automation tasks, it obtains 56.5 on OSWorld, 71.6 on AndroidWorld, and 48.4 on WebArena; (2) on grounding tasks, it obtains 80.3 on ScreenSpotPro; (3) on tool-calling tasks, it obtains 47.6 on OSWorld-MCP, and 46.8 on MobileWorld; (4) on memory and knowledge tasks, it obtains 75.5 on GUI-Knowledge Bench. GUI-Owl-1.5 incorporates several key innovations: (1) Hybird Data Flywheel: we construct the data pipeline for UI understanding and trajectory generation based on a combination of simulated environments and cloud-based sandbox environments, in order to improve the efficiency and quality of data collection. (2) Unified Enhancement of Agent Capabilities: we use a unified thought-synthesis pipeline to enhance the model's reasoning capabilities, while placing particular emphasis on improving key agent abilities, including Tool/MCP use, memory and multi-agent adaptation; (3) Multi-platform Environment RL Scaling: We propose a new environment RL algorithm, MRPO, to address the challenges of multi-platform conflicts and the low training efficiency of long-horizon tasks. The GUI-Owl-1.5 models are open-sourced, and an online cloud-sandbox demo is available at https://github.com/X-PLUG/MobileAgent.
{{< /details >}}

---

*This article is auto-generated. Please refer to each source URL for details about the papers.*
