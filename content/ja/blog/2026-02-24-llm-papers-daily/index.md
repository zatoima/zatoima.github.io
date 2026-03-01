---
title: "LLM論文サーベイ（2026-02-24）"
subtitle: ""
summary: " "
tags: ["LLM", "AI", "論文"]
categories: ["LLM", "AI", "論文"]
url: llm-papers-2026-02-24
date: 2026-02-24
featured: false
draft: false
---

## はじめに

本記事は2026-02-24時点でのLLM関連の注目論文をまとめたものです。arXiv、Semantic Scholar、Hugging Face Daily Papersから自動収集し、Claude APIで日本語要約を生成しています。

## 1. Frontier AI Risk Management Framework in Practice: A Risk Analysis Technical Report v1.5

- **著者**: Dongrui Liu, Yi Yu, Jie Zhang, Guanxu Chen, Qihao Lin ほか
- **公開日**: 2026-02-16
- **ソース**: [huggingface](https://arxiv.org/abs/2602.14457)
- **arXiv ID**: 2602.14457

![Frontier AI Risk Management Framework in Practice: A Risk Analysis Technical Report v1.5](paper_1.png)

### 要約

急速に進歩するAIモデルがもたらす前例のないリスクを理解・特定するため、本報告書ではフロンティアAIのリスクに関する包括的な評価を提示している。大規模言語モデル（LLM）の汎用能力の急速な進化とエージェント型AIの普及を背景に、サイバー攻撃、説得・操作、戦略的欺瞞、制御不能なAI研究開発、自己複製の5つの重要な次元について、更新された詳細な評価を行っている。具体的には、サイバー攻撃のより複雑なシナリオの導入、LLM間の説得リスクの評価、創発的ミスアライメントに関する新実験、エージェントがメモリ基盤やツールセットを自律的に拡張する際の「誤進化」の分析、リソース制約下での自己複製シナリオの追加などが含まれる。さらに、これらの新たな脅威に対処するための堅牢な緩和策を提案・検証し、フロンティアAIの安全な展開に向けた技術的かつ実用的な道筋を示している。

{{< details "原文Abstract" >}}
To understand and identify the unprecedented risks posed by rapidly advancing artificial intelligence (AI) models, Frontier AI Risk Management Framework in Practice presents a comprehensive assessment of their frontier risks. As Large Language Models (LLMs) general capabilities rapidly evolve and the proliferation of agentic AI, this version of the risk analysis technical report presents an updated and granular assessment of five critical dimensions: cyber offense, persuasion and manipulation, strategic deception, uncontrolled AI R\&D, and self-replication. Specifically, we introduce more complex scenarios for cyber offense. For persuasion and manipulation, we evaluate the risk of LLM-to-LLM persuasion on newly released LLMs. For strategic deception and scheming, we add the new experiment with respect to emergent misalignment. For uncontrolled AI R\&D, we focus on the ``mis-evolution'' of agents as they autonomously expand their memory substrates and toolsets. Besides, we also monitor and evaluate the safety performance of OpenClaw during the interaction on the Moltbook. For self-replication, we introduce a new resource-constrained scenario. More importantly, we propose and validate a series of robust mitigation strategies to address these emerging threats, providing a preliminary technical and actionable pathway for the secure deployment of frontier AI. This work reflects our current understanding of AI frontier risks and urges collective action to mitigate these challenges.
{{< /details >}}

## 2. CADEvolve: Creating Realistic CAD via Program Evolution

- **著者**: Maksim Elistratov, Marina Barannikov, Gregory Ivanov, Valentin Khrulkov, Anton Konushin ほか
- **公開日**: 2026-02-18
- **ソース**: [huggingface](https://arxiv.org/abs/2602.16317)
- **arXiv ID**: 2602.16317

![CADEvolve: Creating Realistic CAD via Program Evolution](paper_2.png)

### 要約

CADEvolve は、進化ベースのパイプラインとデータセットであり、単純なプリミティブから出発し、VLM（視覚言語モデル）によるガイド付き編集と検証を通じて、CADプログラムを産業レベルの複雑さへと段階的に成長させる手法である。既存の公開データセットはスケッチ・押し出しシーケンスが中心で、複雑な操作や設計意図が欠如しており、効果的なファインチューニングの妨げとなっている。本手法により、実行可能なCadQueryパラメトリックジェネレータとして表現された8,000個の複雑部品を生成し、多段階の後処理と拡張を経て、レンダリング済みジオメトリと対になった130万スクリプトの統合データセットを構築した。このデータセットでファインチューニングしたVLMは、DeepCAD・Fusion 360・MCBベンチマークにおけるImage2CADタスクで最先端の性能を達成した。

{{< details "原文Abstract" >}}
Computer-Aided Design (CAD) delivers rapid, editable modeling for engineering and manufacturing. Recent AI progress now makes full automation feasible for various CAD tasks. However, progress is bottlenecked by data: public corpora mostly contain sketch-extrude sequences, lack complex operations, multi-operation composition and design intent, and thus hinder effective fine-tuning. Attempts to bypass this with frozen VLMs often yield simple or invalid programs due to limited 3D grounding in current foundation models. We present CADEvolve, an evolution-based pipeline and dataset that starts from simple primitives and, via VLM-guided edits and validations, incrementally grows CAD programs toward industrial-grade complexity. The result is 8k complex parts expressed as executable CadQuery parametric generators. After multi-stage post-processing and augmentation, we obtain a unified dataset of 1.3m scripts paired with rendered geometry and exercising the full CadQuery operation set. A VLM fine-tuned on CADEvolve achieves state-of-the-art results on the Image2CAD task across the DeepCAD, Fusion 360, and MCB benchmarks.
{{< /details >}}

## 3. MAEB: Massive Audio Embedding Benchmark

- **著者**: Adnan El Assadi, Isaac Chung, Chenghao Xiao, Roman Solomatin, Animesh Jha ほか
- **公開日**: 2026-02-17
- **ソース**: [huggingface](https://arxiv.org/abs/2602.16008)
- **arXiv ID**: 2602.16008

![MAEB: Massive Audio Embedding Benchmark](paper_3.png)

### 要約

本研究では、音声・音楽・環境音・クロスモーダル音声テキスト推論を含む100以上の言語にわたる30タスクから構成される大規模音声埋め込みベンチマーク「MAEB」を提案している。50以上のモデルを評価した結果、全タスクで支配的な単一モデルは存在せず、対照学習ベースの音声テキストモデルは環境音分類に優れる一方で多言語音声タスクではほぼランダムに近い性能を示し、音声事前学習モデルはその逆のパターンを示すことが明らかになった。また、音響的理解に優れたモデルは言語的タスクで性能が低く、その逆も同様であること、さらにMAEB上の音声エンコーダの性能が音声大規模言語モデルに組み込んだ際の性能と高い相関を持つことが示された。MAEBは98タスクからなるMAEB+から導出され、タスクの多様性を維持しつつ評価コストを削減する設計となっており、MTEBエコシステムに統合されることでテキスト・画像・音声のモダリティを横断した統一的な評価を可能にしている。

{{< details "原文Abstract" >}}
We introduce the Massive Audio Embedding Benchmark (MAEB), a large-scale benchmark covering 30 tasks across speech, music, environmental sounds, and cross-modal audio-text reasoning in 100+ languages. We evaluate 50+ models and find that no single model dominates across all tasks: contrastive audio-text models excel at environmental sound classification (e.g., ESC50) but score near random on multilingual speech tasks (e.g., SIB-FLEURS), while speech-pretrained models show the opposite pattern. Clustering remains challenging for all models, with even the best-performing model achieving only modest results. We observe that models excelling on acoustic understanding often perform poorly on linguistic tasks, and vice versa. We also show that the performance of audio encoders on MAEB correlates highly with their performance when used in audio large language models. MAEB is derived from MAEB+, a collection of 98 tasks. MAEB is designed to maintain task diversity while reducing evaluation cost, and it integrates into the MTEB ecosystem for unified evaluation across text, image, and audio modalities. We release MAEB and all 98 tasks along with code and a leaderboard at https://github.com/embeddings-benchmark/mteb.
{{< /details >}}

## 4. Generated Reality: Human-centric World Simulation using Interactive Video Generation with Hand and Camera Control

- **著者**: Linxi Xie, Lisong C. Sun, Ashley Neall, Tong Wu, Shengqu Cai ほか
- **公開日**: 2026-02-20
- **ソース**: [huggingface](https://arxiv.org/abs/2602.18422)
- **arXiv ID**: 2602.18422

![Generated Reality: Human-centric World Simulation using Interactive Video Generation with Hand and Camera Control](paper_4.png)

### 要約

拡張現実（XR）では、ユーザーの実世界での動きに応答する生成モデルが求められるが、既存の映像世界モデルはテキストやキーボード入力などの粗い制御信号しか受け付けず、身体的インタラクションへの応用が限定的である。本研究では、トラッキングされた頭部姿勢と関節レベルの手の姿勢の両方を条件とする、人間中心の映像世界モデルを提案する。既存の拡散トランスフォーマーの条件付け戦略を評価し、3D頭部・手制御のための効果的なメカニズムを設計することで、巧緻な手と物体のインタラクションを実現した。双方向映像拡散モデルを教師モデルとして学習し、それを因果的かつインタラクティブなシステムに蒸留することで、一人称視点の仮想環境をリアルタイム生成する。被験者実験により、関連するベースラインと比較してタスク遂行性能が向上し、操作に対する主観的な制御感が有意に高まることが示された。

{{< details "原文Abstract" >}}
Extended reality (XR) demands generative models that respond to users' tracked real-world motion, yet current video world models accept only coarse control signals such as text or keyboard input, limiting their utility for embodied interaction. We introduce a human-centric video world model that is conditioned on both tracked head pose and joint-level hand poses. For this purpose, we evaluate existing diffusion transformer conditioning strategies and propose an effective mechanism for 3D head and hand control, enabling dexterous hand--object interactions. We train a bidirectional video diffusion model teacher using this strategy and distill it into a causal, interactive system that generates egocentric virtual environments. We evaluate this generated reality system with human subjects and demonstrate improved task performance as well as a significantly higher level of perceived amount of control over the performed actions compared with relevant baselines.
{{< /details >}}

## 5. Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents

- **著者**: Wenxuan Ding, Nicholas Tomlin, Greg Durrett
- **公開日**: 2026-02-18
- **ソース**: [huggingface](https://arxiv.org/abs/2602.16699)
- **arXiv ID**: 2602.16699

![Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents](paper_5.png)

### 要約

LLMは単一の応答では解決できない複雑な問題において、環境と対話しながら情報を取得する必要があるが、その際に探索を続けるコストと不確実性の間のトレードオフを適切に判断することが求められる。本研究では、情報検索やコーディングなどの複数のタスクを不確実性下の逐次的意思決定問題として定式化し、潜在的な環境状態に関する事前分布をLLMエージェントに提供する。提案手法「Calibrate-Then-Act（CTA）」は、コストと不確実性のトレードオフに関する追加コンテキストをLLMに与えることで、より最適な環境探索行動を誘導するフレームワークである。この改善効果はベースラインとCTAの両方に対する強化学習の適用後も維持されることが確認された。情報探索型QAタスクおよび簡略化されたコーディングタスクにおける実験により、CTAによるコスト・ベネフィットのトレードオフの明示化がエージェントのより最適な意思決定戦略の発見に寄与することが示された。

{{< details "原文Abstract" >}}
LLMs are increasingly being used for complex problems which are not necessarily resolved in a single response, but require interacting with an environment to acquire information. In these scenarios, LLMs must reason about inherent cost-uncertainty tradeoffs in when to stop exploring and commit to an answer. For instance, on a programming task, an LLM should test a generated code snippet if it is uncertain about the correctness of that code; the cost of writing a test is nonzero, but typically lower than the cost of making a mistake. In this work, we show that we can induce LLMs to explicitly reason about balancing these cost-uncertainty tradeoffs, then perform more optimal environment exploration. We formalize multiple tasks, including information retrieval and coding, as sequential decision-making problems under uncertainty. Each problem has latent environment state that can be reasoned about via a prior which is passed to the LLM agent. We introduce a framework called Calibrate-Then-Act (CTA), where we feed the LLM this additional context to enable it to act more optimally. This improvement is preserved even under RL training of both the baseline and CTA. Our results on information-seeking QA and on a simplified coding task show that making cost-benefit tradeoffs explicit with CTA can help agents discover more optimal decision-making strategies.
{{< /details >}}

---

*この記事は自動生成されています。論文の詳細は各ソースURLをご参照ください。*