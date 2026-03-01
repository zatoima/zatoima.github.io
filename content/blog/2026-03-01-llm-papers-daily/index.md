---
title: "LLM論文サーベイ（2026-03-01）"
subtitle: ""
summary: " "
tags: ["LLM", "AI", "論文"]
categories: ["LLM", "AI", "論文"]
url: llm-papers-2026-03-01
date: 2026-03-01
featured: false
draft: false
---

## はじめに

本記事は2026-03-01時点でのLLM関連の注目論文をまとめたものです。arXiv、Semantic Scholar、Hugging Face Daily Papersから自動収集し、Claude APIで日本語要約を生成しています。

## 1. MediX-R1: Open Ended Medical Reinforcement Learning

- **著者**: Sahal Shaji Mullappilly, Mohammed Irfan Kurpath, Omair Mohamed, Mohamed Zidan, Fahad Khan ほか
- **公開日**: 2026-02-26
- **ソース**: [huggingface](https://arxiv.org/abs/2602.23363)
- **arXiv ID**: 2602.23363

![MediX-R1: Open Ended Medical Reinforcement Learning](paper_1.png)

### 要約

MediX-R1は、医療マルチモーダル大規模言語モデル（MLLM）向けのオープンエンド強化学習フレームワークであり、従来の多肢選択形式を超えた臨床的に根拠のある自由形式の回答生成を可能にする。グループベース強化学習と医療推論に特化した複合報酬関数（LLMベースの精度報酬、医療埋め込みベースの意味的報酬、フォーマット・モダリティ報酬）を用いてビジョン言語モデルをファインチューニングする。評価には、従来の文字列一致指標に代わり、参照ベースのLLM審判を用いた統一評価フレームワークを提案し、意味的正確性・推論・文脈整合性を捕捉する。約5万1千件の指示データのみで訓練したにもかかわらず、テキストのみおよび画像＋テキストの両方の医療ベンチマークで強力なオープンソースベースラインを上回り、特にオープンエンドな臨床タスクで大幅な性能向上を達成した。

{{< details "原文Abstract" >}}
We introduce MediX-R1, an open-ended Reinforcement Learning (RL) framework for medical multimodal large language models (MLLMs) that enables clinically grounded, free-form answers beyond multiple-choice formats. MediX-R1 fine-tunes a baseline vision-language backbone with Group Based RL and a composite reward tailored for medical reasoning: an LLM-based accuracy reward that judges semantic correctness with a strict YES/NO decision, a medical embedding-based semantic reward to capture paraphrases and terminology variants, and lightweight format and modality rewards that enforce interpretable reasoning and modality recognition. This multi-signal design provides stable, informative feedback for open-ended outputs where traditional verifiable or MCQ-only rewards fall short. To measure progress, we propose a unified evaluation framework for both text-only and image+text tasks that uses a Reference-based LLM-as-judge in place of brittle string-overlap metrics, capturing semantic correctness, reasoning, and contextual alignment. Despite using only sim51K instruction examples, MediX-R1 achieves excellent results across standard medical LLM (text-only) and VLM (image + text) benchmarks, outperforming strong open-source baselines and delivering particularly large gains on open-ended clinical tasks. Our results demonstrate that open-ended RL with comprehensive reward signals and LLM-based evaluation is a practical path toward reliable medical reasoning in multimodal models. Our trained models, curated datasets and source code are available at https://medix.cvmbzuai.com
{{< /details >}}

## 2. Accelerating Diffusion via Hybrid Data-Pipeline Parallelism Based on Conditional Guidance Scheduling

- **著者**: Euisoo Jung, Byunghyun Kim, Hyunjin Kim, Seonghye Cho, Jae-Gil Lee
- **公開日**: 2026-02-25
- **ソース**: [huggingface](https://arxiv.org/abs/2602.21760)
- **arXiv ID**: 2602.21760

![Accelerating Diffusion via Hybrid Data-Pipeline Parallelism Based on Conditional Guidance Scheduling](paper_2.png)

### 要約

拡散モデルは高品質な画像・動画・音声生成で顕著な進歩を遂げているが、推論の計算コストが依然として高い。既存の分散並列化による高速化手法は生成品質の劣化やGPU数に比例した十分な高速化が達成できないという課題がある。本研究では、条件付き・無条件のデノイジングパスを新たなデータ分割の観点として活用するデータ並列戦略と、両パス間のデノイジング差異に応じて最適なパイプライン並列に適応的に切り替えるスケジューリング手法を組み合わせたハイブリッド並列化フレームワークを提案する。2台のNVIDIA RTX 3090を用いた実験では、SDXLで2.31倍、SD3で2.07倍のレイテンシ削減を画質を維持しつつ達成し、U-NetベースおよびDiTベースの両アーキテクチャへの汎用性を実証した。さらに、高解像度生成設定においても既存手法を上回る高速化性能を示している。

{{< details "原文Abstract" >}}
Diffusion models have achieved remarkable progress in high-fidelity image, video, and audio generation, yet inference remains computationally expensive. Nevertheless, current diffusion acceleration methods based on distributed parallelism suffer from noticeable generation artifacts and fail to achieve substantial acceleration proportional to the number of GPUs. Therefore, we propose a hybrid parallelism framework that combines a novel data parallel strategy, condition-based partitioning, with an optimal pipeline scheduling method, adaptive parallelism switching, to reduce generation latency and achieve high generation quality in conditional diffusion models. The key ideas are to (i) leverage the conditional and unconditional denoising paths as a new data-partitioning perspective and (ii) adaptively enable optimal pipeline parallelism according to the denoising discrepancy between these two paths. Our framework achieves 2.31times and 2.07times latency reductions on SDXL and SD3, respectively, using two NVIDIA RTX~3090 GPUs, while preserving image quality. This result confirms the generality of our approach across U-Net-based diffusion models and DiT-based flow-matching architectures. Our approach also outperforms existing methods in acceleration under high-resolution synthesis settings. Code is available at https://github.com/kaist-dmlab/Hybridiff.
{{< /details >}}

## 3. EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents

- **著者**: Wenjia Wang, Liang Pan, Huaijin Pi, Yuke Lou, Xuqian Ren ほか
- **公開日**: 2026-02-26
- **ソース**: [huggingface](https://arxiv.org/abs/2602.23205)
- **arXiv ID**: 2602.23205

![EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents](paper_3.png)

### 要約

EmbodMocapは、2台のiPhoneを用いた携帯可能かつ低コストな4Dヒューマン・シーン復元パイプラインであり、スタジオ設備やウェアラブルデバイスなしに日常環境での人間行動データの大規模収集を可能にする。核となる手法は、2台のRGB-Dシーケンスを統一的なメートルスケールの世界座標系で共同キャリブレーションし、人間とシーンの両方を整合的に復元する点にある。単眼やシングルiPhoneと比較して、デュアルビュー設定は奥行き曖昧性を大幅に軽減し、優れたアライメントと復元精度を達成することが示された。収集データを活用し、単眼ヒューマン・シーン復元のファインチューニング、物理ベースキャラクタアニメーションにおける人物・物体インタラクションスキルのスケーリング、sim-to-real強化学習によるヒューマノイドロボットの動作制御という3つの身体性AIタスクへの有効性が実験的に検証されている。

{{< details "原文Abstract" >}}
Human behaviors in the real world naturally encode rich, long-term contextual information that can be leveraged to train embodied agents for perception, understanding, and acting. However, existing capture systems typically rely on costly studio setups and wearable devices, limiting the large-scale collection of scene-conditioned human motion data in the wild. To address this, we propose EmbodMocap, a portable and affordable data collection pipeline using two moving iPhones. Our key idea is to jointly calibrate dual RGB-D sequences to reconstruct both humans and scenes within a unified metric world coordinate frame. The proposed method allows metric-scale and scene-consistent capture in everyday environments without static cameras or markers, bridging human motion and scene geometry seamlessly. Compared with optical capture ground truth, we demonstrate that the dual-view setting exhibits a remarkable ability to mitigate depth ambiguity, achieving superior alignment and reconstruction performance over single iphone or monocular models. Based on the collected data, we empower three embodied AI tasks: monocular human-scene-reconstruction, where we fine-tune on feedforward models that output metric-scale, world-space aligned humans and scenes; physics-based character animation, where we prove our data could be used to scale human-object interaction skills and scene-aware motion tracking; and robot motion control, where we train a humanoid robot via sim-to-real RL to replicate human motions depicted in videos. Experimental results validate the effectiveness of our pipeline and its contributions towards advancing embodied AI research.
{{< /details >}}

## 4. AI Gamestore: Scalable, Open-Ended Evaluation of Machine General Intelligence with Human Games

- **著者**: Lance Ying, Ryan Truong, Prafull Sharma, Kaiya Ivy Zhao, Nathan Cloos ほか
- **公開日**: 2026-02-19
- **ソース**: [huggingface](https://arxiv.org/abs/2602.17594)
- **arXiv ID**: 2602.17594

![AI Gamestore: Scalable, Open-Ended Evaluation of Machine General Intelligence with Human Games](paper_4.png)

### 要約

人間の汎用知能に対してAIを厳密に評価するため、人間が人間のために設計したあらゆるゲーム（「人間ゲームのマルチバース」）をプレイ・学習する能力を測定するという新たな評価アプローチを提案している。この構想の第一歩として、LLMとヒューマン・イン・ザ・ループを活用し、Apple App StoreやSteamなどの人気ゲームプラットフォームから標準化・コンテナ化されたゲーム環境を自動的に収集・適応させるスケーラブルかつオープンエンドな評価基盤「AI GameStore」を構築した。概念実証として人気ランキング上位から100種のゲームを生成し、7つの最先端ビジョン言語モデル（VLM）を評価した結果、最良モデルでも大半のゲームで人間の平均スコアの10%未満にとどまり、特に世界モデルの学習・記憶・計画を要するゲームで大きく苦戦した。

{{< details "原文Abstract" >}}
Rigorously evaluating machine intelligence against the broad spectrum of human general intelligence has become increasingly important and challenging in this era of rapid technological advance. Conventional AI benchmarks typically assess only narrow capabilities in a limited range of human activity. Most are also static, quickly saturating as developers explicitly or implicitly optimize for them. We propose that a more promising way to evaluate human-like general intelligence in AI systems is through a particularly strong form of general game playing: studying how and how well they play and learn to play all conceivable human games, in comparison to human players with the same level of experience, time, or other resources. We define a "human game" to be a game designed by humans for humans, and argue for the evaluative suitability of this space of all such games people can imagine and enjoy -- the "Multiverse of Human Games". Taking a first step towards this vision, we introduce the AI GameStore, a scalable and open-ended platform that uses LLMs with humans-in-the-loop to synthesize new representative human games, by automatically sourcing and adapting standardized and containerized variants of game environments from popular human digital gaming platforms. As a proof of concept, we generated 100 such games based on the top charts of Apple App Store and Steam, and evaluated seven frontier vision-language models (VLMs) on short episodes of play. The best models achieved less than 10\% of the human average score on the majority of the games, and especially struggled with games that challenge world-model learning, memory and planning. We conclude with a set of next steps for building out the AI GameStore as a practical way to measure and drive progress toward human-like general intelligence in machines.
{{< /details >}}

## 5. Causal Motion Diffusion Models for Autoregressive Motion Generation

- **著者**: Qing Yu, Akihisa Watanabe, Kent Fujiwara
- **公開日**: 2026-02-26
- **ソース**: [huggingface](https://arxiv.org/abs/2602.22594)
- **arXiv ID**: 2602.22594

![Causal Motion Diffusion Models for Autoregressive Motion Generation](paper_5.png)

### 要約

近年のモーション拡散モデルは人体動作合成のリアリズムを大幅に向上させたが、既存手法は双方向生成による時間的因果性の欠如やリアルタイム性の制約、あるいは自己回帰モデルにおける不安定性と累積誤差という課題を抱えている。本研究では、意味的に整合した潜在空間上で動作する因果拡散Transformerに基づく自己回帰モーション生成の統一フレームワーク「Causal Motion Diffusion Models（CMDM）」を提案する。CMDMは、動作系列を時間的因果性を持つ潜在表現に符号化するMotion-Language-Aligned Causal VAE（MAC-VAE）を基盤とし、その上で因果拡散フォーシングによる自己回帰拡散Transformerを学習することで、時間順序に沿ったデノイジングを実現する。高速推論のために、部分的にデノイズされた前フレームから次フレームを予測する因果不確実性付きフレーム単位サンプリングスケジュールを導入し、テキストからのモーション生成、ストリーミング合成、長期間動作生成をインタラクティブな速度で実現する。HumanML3DおよびSnapMoGenでの実験により、CMDMは意味的忠実度と時間的滑らかさの両面で既存の拡散モデルおよび自己回帰モデルを上回り、推論遅延も大幅に削減されることが示された。

{{< details "原文Abstract" >}}
Recent advances in motion diffusion models have substantially improved the realism of human motion synthesis. However, existing approaches either rely on full-sequence diffusion models with bidirectional generation, which limits temporal causality and real-time applicability, or autoregressive models that suffer from instability and cumulative errors. In this work, we present Causal Motion Diffusion Models (CMDM), a unified framework for autoregressive motion generation based on a causal diffusion transformer that operates in a semantically aligned latent space. CMDM builds upon a Motion-Language-Aligned Causal VAE (MAC-VAE), which encodes motion sequences into temporally causal latent representations. On top of this latent representation, an autoregressive diffusion transformer is trained using causal diffusion forcing to perform temporally ordered denoising across motion frames. To achieve fast inference, we introduce a frame-wise sampling schedule with causal uncertainty, where each subsequent frame is predicted from partially denoised previous frames. The resulting framework supports high-quality text-to-motion generation, streaming synthesis, and long-horizon motion generation at interactive rates. Experiments on HumanML3D and SnapMoGen demonstrate that CMDM outperforms existing diffusion and autoregressive models in both semantic fidelity and temporal smoothness, while substantially reducing inference latency.
{{< /details >}}

---

*この記事は自動生成されています。論文の詳細は各ソースURLをご参照ください。*