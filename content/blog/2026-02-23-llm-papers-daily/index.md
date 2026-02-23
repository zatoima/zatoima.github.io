---
title: "LLM論文サーベイ（2026-02-23）"
subtitle: ""
summary: " "
tags: ["LLM", "AI", "論文"]
categories: ["LLM", "AI", "論文"]
url: llm-papers-2026-02-23
date: 2026-02-23
featured: false
draft: false
---

## はじめに

本記事は2026-02-23時点でのLLM関連の注目論文をまとめたものです。arXiv、Semantic Scholar、Hugging Face Daily Papersから自動収集し、Claude APIで日本語要約を生成しています。

## 1. VESPO: Variational Sequence-Level Soft Policy Optimization for Stable Off-Policy LLM Training

- **著者**: Guobin Shen, Chenxiao Zhao, Xiang Cheng, Lei Huang, Xing Yu
- **公開日**: 2026-02-11
- **ソース**: [huggingface](https://arxiv.org/abs/2602.10693)
- **arXiv ID**: 2602.10693

### 要約

大規模言語モデル（LLM）の強化学習における訓練安定性の課題に取り組んだ研究である。ポリシーの陳腐化や非同期訓練、訓練エンジンと推論エンジンの不一致により行動ポリシーが現行ポリシーから乖離し、訓練崩壊を引き起こすリスクがある。本研究では、提案分布に対する変分定式化に分散削減を組み込んだVESPO（Variational sEquence-level Soft Policy Optimization）を提案し、長さ正規化を必要とせずシーケンスレベルの重要度重みに直接作用する閉形式の再形成カーネルを導出した。数学的推論ベンチマークにおける実験では、VESPOは陳腐化比率64倍および完全非同期実行下でも安定した訓練を維持し、密結合モデルとMixture-of-Expertsモデルの両方で一貫した性能向上を達成した。

{{< details "原文Abstract" >}}
Training stability remains a central challenge in reinforcement learning (RL) for large language models (LLMs). Policy staleness, asynchronous training, and mismatches between training and inference engines all cause the behavior policy to diverge from the current policy, risking training collapse. Importance sampling provides a principled correction for this distribution shift but suffers from high variance; existing remedies such as token-level clipping and sequence-level normalization lack a unified theoretical foundation. We propose Variational sEquence-level Soft Policy Optimization (VESPO). By incorporating variance reduction into a variational formulation over proposal distributions, VESPO derives a closed-form reshaping kernel that operates directly on sequence-level importance weights without length normalization. Experiments on mathematical reasoning benchmarks show that VESPO maintains stable training under staleness ratios up to 64x and fully asynchronous execution, and delivers consistent gains across both dense and Mixture-of-Experts models. Code is available at https://github.com/FloyedShen/VESPO
{{< /details >}}

## 2. Does Your Reasoning Model Implicitly Know When to Stop Thinking?

- **著者**: Zixuan Huang, Xin Xia, Yuxi Ren, Jianbin Zheng, Xuanda Wang ほか
- **公開日**: 2026-02-09
- **ソース**: [huggingface](https://arxiv.org/abs/2602.08354)
- **arXiv ID**: 2602.08354

### 要約

大規模推論モデル（LRM）は長い思考連鎖（CoT）により複雑な推論タスクの性能を向上させてきたが、冗長な推論が計算効率を損ない、リアルタイム応用での遅延を引き起こすという課題がある。先行研究では、推論連鎖が長いほど正答率が上がるわけではなく、むしろ精度を低下させる場合があることが示されている。本研究では、LRMが思考を停止すべき適切なタイミングを暗黙的に把握しているが、現行のサンプリング手法がその能力を覆い隠していることを発見・実証した。この知見に基づき、効率的な推論能力を引き出す新たなサンプリング手法SAGE（Self-Aware Guided Efficient Reasoning）を提案し、さらにSAGEをグループベース強化学習に統合したSAGE-RLにより、複数の数学ベンチマークにおいて推論の精度と効率の両方を大幅に改善することを示した。

{{< details "原文Abstract" >}}
Recent advancements in large reasoning models (LRMs) have greatly improved their capabilities on complex reasoning tasks through Long Chains of Thought (CoTs). However, this approach often results in substantial redundancy, impairing computational efficiency and causing significant delays in real-time applications. Recent studies show that longer reasoning chains are frequently uncorrelated with correctness and can even be detrimental to accuracy. In a further in-depth analysis of this phenomenon, we surprisingly uncover and empirically verify that LRMs implicitly know the appropriate time to stop thinking, while this capability is obscured by current sampling paradigms. Motivated by this, we introduce SAGE (Self-Aware Guided Efficient Reasoning), a novel sampling paradigm that unleashes this efficient reasoning potential. Furthermore, integrating SAGE as mixed sampling into group-based reinforcement learning (SAGE-RL) enables SAGE-RL to effectively incorporate SAGE-discovered efficient reasoning patterns into standard pass@1 inference, markedly enhancing both the reasoning accuracy and efficiency of LRMs across multiple challenging mathematical benchmarks.
{{< /details >}}

## 3. SLA2: Sparse-Linear Attention with Learnable Routing and QAT

- **著者**: Jintao Zhang, Haoxu Wang, Kai Jiang, Kaiwen Zheng, Youhe Jiang ほか
- **公開日**: 2026-02-13
- **ソース**: [huggingface](https://arxiv.org/abs/2602.12675)
- **arXiv ID**: 2602.12675

### 要約

Sparse-Linear Attention（SLA）はスパース注意と線形注意を組み合わせて拡散モデルを高速化する手法であるが、ヒューリスティックな分割方式が最適でない点と、SLAの注意誤差にスパース・線形注意の直接分解との不一致が存在する点が課題であった。本論文で提案するSLA2は、各注意計算をスパースと線形のどちらで処理するかを動的に選択する学習可能なルーター、学習可能な比率でスパースと線形の注意分岐を組み合わせるより忠実な定式化、および量子化認識ファインチューニングによる低ビット注意設計の3つを導入する。実験の結果、SLA2は動画拡散モデルにおいて97%の注意スパース性を達成し、生成品質を維持しながら注意計算で18.6倍の高速化を実現した。

{{< details "原文Abstract" >}}
Sparse-Linear Attention (SLA) combines sparse and linear attention to accelerate diffusion models and has shown strong performance in video generation. However, (i) SLA relies on a heuristic split that assigns computations to the sparse or linear branch based on attention-weight magnitude, which can be suboptimal. Additionally, (ii) after formally analyzing the attention error in SLA, we identify a mismatch between SLA and a direct decomposition into sparse and linear attention. We propose SLA2, which introduces (I) a learnable router that dynamically selects whether each attention computation should use sparse or linear attention, (II) a more faithful and direct sparse-linear attention formulation that uses a learnable ratio to combine the sparse and linear attention branches, and (III) a sparse + low-bit attention design, where low-bit attention is introduced via quantization-aware fine-tuning to reduce quantization error. Experiments show that on video diffusion models, SLA2 can achieve 97% attention sparsity and deliver an 18.6x attention speedup while preserving generation quality.
{{< /details >}}

## 4. SpargeAttention2: Trainable Sparse Attention via Hybrid Top-k+Top-p Masking and Distillation Fine-Tuning

- **著者**: Jintao Zhang, Kai Jiang, Chendong Xiang, Weiqi Feng, Yuezhou Hu ほか
- **公開日**: 2026-02-13
- **ソース**: [huggingface](https://arxiv.org/abs/2602.13515)
- **arXiv ID**: 2602.13515

### 要約

拡散モデルの高速化に向けた学習可能なスパースアテンション手法SpargeAttention2を提案している。Top-kとTop-pという2つの一般的なマスキングルールそれぞれの失敗ケースを分析し、両者を組み合わせたハイブリッドマスキングにより高スパース性でもロバストなマスキングを実現する。さらに、拡散損失によるファインチューニングの限界を指摘し、蒸留に基づくファインチューニング目的関数を導入することで生成品質の維持を図る。動画拡散モデルでの実験では、アテンションスパース性95%、アテンション処理の16.2倍の高速化を達成しつつ生成品質を維持し、既存のスパースアテンション手法を一貫して上回る性能を示した。

{{< details "原文Abstract" >}}
Many training-free sparse attention methods are effective for accelerating diffusion models. Recently, several works suggest that making sparse attention trainable can further increase sparsity while preserving generation quality. We study three key questions: (1) when do the two common masking rules, i.e., Top-k and Top-p, fail, and how can we avoid these failures? (2) why can trainable sparse attention reach higher sparsity than training-free methods? (3) what are the limitations of fine-tuning sparse attention using the diffusion loss, and how can we address them? Based on this analysis, we propose SpargeAttention2, a trainable sparse attention method that achieves high sparsity without degrading generation quality. SpargeAttention2 includes (i) a hybrid masking rule that combines Top-k and Top-p for more robust masking at high sparsity, (ii) an efficient trainable sparse attention implementation, and (iii) a distillation-inspired fine-tuning objective to better preserve generation quality during fine-tuning using sparse attention. Experiments on video diffusion models show that SpargeAttention2 reaches 95% attention sparsity and a 16.2x attention speedup while maintaining generation quality, consistently outperforming prior sparse attention methods.
{{< /details >}}

## 5. Mobile-Agent-v3.5: Multi-platform Fundamental GUI Agents

- **著者**: Haiyang Xu, Xi Zhang, Haowei Liu, Junyang Wang, Zhaozai Zhu ほか
- **公開日**: 2026-02-15
- **ソース**: [huggingface](https://arxiv.org/abs/2602.16855)
- **arXiv ID**: 2602.16855

### 要約

GUI-Owl-1.5は、デスクトップ・モバイル・ブラウザなど複数プラットフォームに対応したネイティブGUIエージェントモデルであり、2Bから235Bまでの複数サイズでinstruct/thinkingの両バリアントを提供し、クラウド・エッジ連携とリアルタイムインタラクションを実現する。OSWorld（56.5）、AndroidWorld（71.6）、WebArena（48.4）、ScreenSpotPro（80.3）など20以上のGUIベンチマークでオープンソースモデルとして最高性能を達成した。主要な技術革新として、シミュレーション環境とクラウドサンドボックス環境を組み合わせたハイブリッドデータフライホイール、ツール/MCP利用・記憶・マルチエージェント適応を含む統一的な思考合成パイプラインによるエージェント能力の強化、そしてマルチプラットフォーム間の競合と長期タスクの低訓練効率に対処する新しい環境強化学習アルゴリズムMRPOを提案している。

{{< details "原文Abstract" >}}
The paper introduces GUI-Owl-1.5, the latest native GUI agent model that features instruct/thinking variants in multiple sizes (2B/4B/8B/32B/235B) and supports a range of platforms (desktop, mobile, browser, and more) to enable cloud-edge collaboration and real-time interaction. GUI-Owl-1.5 achieves state-of-the-art results on more than 20+ GUI benchmarks on open-source models: (1) on GUI automation tasks, it obtains 56.5 on OSWorld, 71.6 on AndroidWorld, and 48.4 on WebArena; (2) on grounding tasks, it obtains 80.3 on ScreenSpotPro; (3) on tool-calling tasks, it obtains 47.6 on OSWorld-MCP, and 46.8 on MobileWorld; (4) on memory and knowledge tasks, it obtains 75.5 on GUI-Knowledge Bench. GUI-Owl-1.5 incorporates several key innovations: (1) Hybird Data Flywheel: we construct the data pipeline for UI understanding and trajectory generation based on a combination of simulated environments and cloud-based sandbox environments, in order to improve the efficiency and quality of data collection. (2) Unified Enhancement of Agent Capabilities: we use a unified thought-synthesis pipeline to enhance the model's reasoning capabilities, while placing particular emphasis on improving key agent abilities, including Tool/MCP use, memory and multi-agent adaptation; (3) Multi-platform Environment RL Scaling: We propose a new environment RL algorithm, MRPO, to address the challenges of multi-platform conflicts and the low training efficiency of long-horizon tasks. The GUI-Owl-1.5 models are open-sourced, and an online cloud-sandbox demo is available at https://github.com/X-PLUG/MobileAgent.
{{< /details >}}

---

*この記事は自動生成されています。論文の詳細は各ソースURLをご参照ください。*