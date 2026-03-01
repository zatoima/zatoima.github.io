---
title: "LLM論文サーベイ（2026-02-27）"
subtitle: ""
summary: " "
tags: ["LLM", "AI", "論文"]
categories: ["LLM", "AI", "論文"]
url: llm-papers-2026-02-27
date: 2026-02-27
featured: false
draft: false
---

## はじめに

本記事は2026-02-27時点でのLLM関連の注目論文をまとめたものです。arXiv、Semantic Scholar、Hugging Face Daily Papersから自動収集し、Claude APIで日本語要約を生成しています。

## 1. ARLArena: A Unified Framework for Stable Agentic Reinforcement Learning

- **著者**: Xiaoxuan Wang, Han Zhang, Haixin Wang, Yidan Shi, Ruoyan Li ほか
- **公開日**: 2026-02-25
- **ソース**: [huggingface](https://arxiv.org/abs/2602.21534)
- **arXiv ID**: 2602.21534

![ARLArena: A Unified Framework for Stable Agentic Reinforcement Learning](paper_1.png)

### 要約

エージェント強化学習（ARL）は、複雑なマルチステップの対話タスクを解くエージェントの訓練パラダイムとして注目されているが、訓練の不安定性（崩壊）が深刻な課題となっている。本論文では、訓練の安定性を制御・再現可能な環境で体系的に分析するためのフレームワーク「ARLArena」を提案し、標準化されたテストベッド上でポリシー勾配を4つの設計次元に分解して各次元の性能と安定性を評価する。この精緻な分析に基づき、ARLにおける主要な不安定要因を緩和する安定的なエージェントポリシー最適化手法「SAMPO」を提案する。実験では、SAMPOが多様なエージェントタスクにおいて一貫して安定した訓練と高い性能を達成することを示し、LLMベースのエージェント訓練パイプラインの構築に向けた実践的な指針を提供している。

{{< details "原文Abstract" >}}
Agentic reinforcement learning (ARL) has rapidly gained attention as a promising paradigm for training agents to solve complex, multi-step interactive tasks. Despite encouraging early results, ARL remains highly unstable, often leading to training collapse. This instability limits scalability to larger environments and longer interaction horizons, and constrains systematic exploration of algorithmic design choices. In this paper, we first propose ARLArena, a stable training recipe and systematic analysis framework that examines training stability in a controlled and reproducible setting. ARLArena first constructs a clean and standardized testbed. Then, we decompose policy gradient into four core design dimensions and assess the performance and stability of each dimension. Through this fine-grained analysis, we distill a unified perspective on ARL and propose SAMPO, a stable agentic policy optimization method designed to mitigate the dominant sources of instability in ARL. Empirically, SAMPO achieves consistently stable training and strong performance across diverse agentic tasks. Overall, this study provides a unifying policy gradient perspective for ARL and offers practical guidance for building stable and reproducible LLM-based agent training pipelines.
{{< /details >}}

## 2. World Guidance: World Modeling in Condition Space for Action Generation

- **著者**: Yue Su, Sijin Chen, Haixin Shi, Mingyu Liu, Zhengshen Zhang ほか
- **公開日**: 2026-02-25
- **ソース**: [huggingface](https://arxiv.org/abs/2602.22010)
- **arXiv ID**: 2602.22010

![World Guidance: World Modeling in Condition Space for Action Generation](paper_2.png)

### 要約

Vision-Language-Action（VLA）モデルにおいて、将来の観測情報を活用した行動生成を改善するフレームワーク「WoG（World Guidance）」を提案している。既存手法では、効率的で予測可能な将来表現の維持と、精密な行動生成に必要な細粒度情報の保持との間でトレードオフが生じていた。WoGは将来の観測をコンパクトな条件表現に圧縮し、行動推論パイプラインに注入することで、条件空間内での世界モデリングを実現する。この条件空間の学習・予測により、細粒度の行動生成が可能になるだけでなく、優れた汎化性能を示し、大量の人間の操作動画からも効果的に学習できることが示された。シミュレーションおよび実環境での広範な実験により、将来予測に基づく既存手法を大幅に上回る性能が確認された。

{{< details "原文Abstract" >}}
Leveraging future observation modeling to facilitate action generation presents a promising avenue for enhancing the capabilities of Vision-Language-Action (VLA) models. However, existing approaches struggle to strike a balance between maintaining efficient, predictable future representations and preserving sufficient fine-grained information to guide precise action generation. To address this limitation, we propose WoG (World Guidance), a framework that maps future observations into compact conditions by injecting them into the action inference pipeline. The VLA is then trained to simultaneously predict these compressed conditions alongside future actions, thereby achieving effective world modeling within the condition space for action inference. We demonstrate that modeling and predicting this condition space not only facilitates fine-grained action generation but also exhibits superior generalization capabilities. Moreover, it learns effectively from substantial human manipulation videos. Extensive experiments across both simulation and real-world environments validate that our method significantly outperforms existing methods based on future prediction. Project page is available at: https://selen-suyue.github.io/WoGNet/
{{< /details >}}

## 3. PETS: A Principled Framework Towards Optimal Trajectory Allocation for Efficient Test-Time Self-Consistency

- **著者**: Zhangyi Liu, Huaizhi Qu, Xiaowei Yin, He Sun, Yanjun Han ほか
- **公開日**: 2026-02-18
- **ソース**: [huggingface](https://arxiv.org/abs/2602.16745)
- **arXiv ID**: 2602.16745

![PETS: A Principled Framework Towards Optimal Trajectory Allocation for Efficient Test-Time Self-Consistency](paper_3.png)

### 要約

テスト時スケーリングにおいて、限られた計算予算の下で効率的に自己一貫性を達成するための原理的フレームワークPETSを提案している。中核となるのは「自己一貫性率」という新しい指標で、無限予算での多数決結果との一致度として定義され、理論的に厳密なトラジェクトリ配分の最適化を可能にする。オフライン設定では、推論トレースをワーカーとみなすことでクラウドソーシング理論と接続し、理論保証付きの多数決ベース配分アルゴリズムを導出した。オンラインストリーミング設定では、問題の難易度に応じて予算を適応的に配分する新手法を提案し、理論保証と計算効率を両立させている。実験では、GPQAベンチマークにおいて均一配分と比較してオフラインで最大75%、オンラインで最大55%のサンプリング予算削減を達成しつつ、完全な自己一貫性を実現した。

{{< details "原文Abstract" >}}
Test-time scaling can improve model performance by aggregating stochastic reasoning trajectories. However, achieving sample-efficient test-time self-consistency under a limited budget remains an open challenge. We introduce PETS (Principled and Efficient Test-TimeSelf-Consistency), which initiates a principled study of trajectory allocation through an optimization framework. Central to our approach is the self-consistency rate, a new measure defined as agreement with the infinite-budget majority vote. This formulation makes sample-efficient test-time allocation theoretically grounded and amenable to rigorous analysis. We study both offline and online settings. In the offline regime, where all questions are known in advance, we connect trajectory allocation to crowdsourcing, a classic and well-developed area, by modeling reasoning traces as workers. This perspective allows us to leverage rich existing theory, yielding theoretical guarantees and an efficient majority-voting-based allocation algorithm. In the online streaming regime, where questions arrive sequentially and allocations must be made on the fly, we propose a novel method inspired by the offline framework. Our approach adapts budgets to question difficulty while preserving strong theoretical guarantees and computational efficiency. Experiments show that PETS consistently outperforms uniform allocation. On GPQA, PETS achieves perfect self-consistency in both settings while reducing the sampling budget by up to 75% (offline) and 55% (online) relative to uniform allocation. Code is available at https://github.com/ZDCSlab/PETS.
{{< /details >}}

## 4. The Trinity of Consistency as a Defining Principle for General World Models

- **著者**: Jingxuan Wei, Siyuan Li, Yuhang Xu, Zheng Sun, Junjie Jiang ほか
- **公開日**: 2026-02-26
- **ソース**: [huggingface](https://arxiv.org/abs/2602.23152)
- **arXiv ID**: 2602.23152

![The Trinity of Consistency as a Defining Principle for General World Models](paper_4.png)

### 要約

本論文は、汎用世界モデル（General World Model）が備えるべき本質的な性質を定義する理論的枠組みとして「一貫性の三位一体（Trinity of Consistency）」を提案する。この枠組みは、意味的インターフェースとしてのモーダル一貫性、幾何学的基盤としての空間一貫性、因果推論エンジンとしての時間一貫性の3要素から構成される。Soraに代表される動画生成モデルやUnified Multimodal Model（UMM）の進展を踏まえ、マルチモーダル学習の進化を体系的にレビューし、疎結合な専門モジュールから統合アーキテクチャへの発展軌跡を明らかにしている。さらに、マルチフレーム推論・生成シナリオに焦点を当てたベンチマーク「CoW-Bench」を導入し、動画生成モデルとUMMを統一的な評価プロトコルで評価する手法を提示している。

{{< details "原文Abstract" >}}
The construction of World Models capable of learning, simulating, and reasoning about objective physical laws constitutes a foundational challenge in the pursuit of Artificial General Intelligence. Recent advancements represented by video generation models like Sora have demonstrated the potential of data-driven scaling laws to approximate physical dynamics, while the emerging Unified Multimodal Model (UMM) offers a promising architectural paradigm for integrating perception, language, and reasoning. Despite these advances, the field still lacks a principled theoretical framework that defines the essential properties requisite for a General World Model. In this paper, we propose that a World Model must be grounded in the Trinity of Consistency: Modal Consistency as the semantic interface, Spatial Consistency as the geometric basis, and Temporal Consistency as the causal engine. Through this tripartite lens, we systematically review the evolution of multimodal learning, revealing a trajectory from loosely coupled specialized modules toward unified architectures that enable the synergistic emergence of internal world simulators. To complement this conceptual framework, we introduce CoW-Bench, a benchmark centered on multi-frame reasoning and generation scenarios. CoW-Bench evaluates both video generation models and UMMs under a unified evaluation protocol. Our work establishes a principled pathway toward general world models, clarifying both the limitations of current systems and the architectural requirements for future progress.
{{< /details >}}

## 5. From Statics to Dynamics: Physics-Aware Image Editing with Latent Transition Priors

- **著者**: Liangbing Zhao, Le Zhuo, Sayak Paul, Hongsheng Li, Mohamed Elhoseiny
- **公開日**: 2026-02-25
- **ソース**: [huggingface](https://arxiv.org/abs/2602.21778)
- **arXiv ID**: 2602.21778

![From Statics to Dynamics: Physics-Aware Image Editing with Latent Transition Priors](paper_5.png)

### 要約

指示ベースの画像編集はセマンティックな整合性において大きな成功を収めているが、屈折や材料変形などの複雑な因果的ダイナミクスを伴う編集では、物理的に妥当な結果を生成できないことが多い。本研究では、この問題を画像ペア間の離散的マッピングとして編集を扱う従来のパラダイムに起因するものとし、物理的に意識した編集を予測的な物理状態遷移として再定式化する。5つの物理ドメインにわたる3万8千件の遷移軌跡を含む大規模ビデオベースデータセットPhysicTran38Kを構築し、これを教師データとして、テキストと視覚の双方向推論メカニズムを備えたエンドツーエンドフレームワークPhysicEditを提案する。PhysicEditは、凍結したQwen2.5-VLによる物理的推論と、拡散バックボーンにタイムステップ適応型の視覚的ガイダンスを提供する学習可能な遷移クエリを組み合わせている。実験の結果、PhysicEditはQwen-Image-Editに対して物理的リアリズムで5.9%、知識に基づく編集で10.1%の改善を達成し、オープンソース手法として新たな最先端性能を記録した。

{{< details "原文Abstract" >}}
Instruction-based image editing has achieved remarkable success in semantic alignment, yet state-of-the-art models frequently fail to render physically plausible results when editing involves complex causal dynamics, such as refraction or material deformation. We attribute this limitation to the dominant paradigm that treats editing as a discrete mapping between image pairs, which provides only boundary conditions and leaves transition dynamics underspecified. To address this, we reformulate physics-aware editing as predictive physical state transitions and introduce PhysicTran38K, a large-scale video-based dataset comprising 38K transition trajectories across five physical domains, constructed via a two-stage filtering and constraint-aware annotation pipeline. Building on this supervision, we propose PhysicEdit, an end-to-end framework equipped with a textual-visual dual-thinking mechanism. It combines a frozen Qwen2.5-VL for physically grounded reasoning with learnable transition queries that provide timestep-adaptive visual guidance to a diffusion backbone. Experiments show that PhysicEdit improves over Qwen-Image-Edit by 5.9% in physical realism and 10.1% in knowledge-grounded editing, setting a new state-of-the-art for open-source methods, while remaining competitive with leading proprietary models.
{{< /details >}}

---

*この記事は自動生成されています。論文の詳細は各ソースURLをご参照ください。*