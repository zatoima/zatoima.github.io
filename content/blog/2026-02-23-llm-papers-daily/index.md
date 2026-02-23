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

## 1. VIRAASAT: Traversing Novel Paths for Indian Cultural Reasoning

- **著者**: Harshul Raj Surana, Arijit Maji, Aryan Vats, Akash Ghosh, Sriparna Saha ほか
- **公開日**: 2026-02-20
- **ソース**: [arxiv](http://arxiv.org/abs/2602.18429v1)
- **arXiv ID**: 2602.18429v1

### 要約

VIRAASATは、インド文化に関する多段階推論（マルチホップQA）データセットを半自動的に生成する新しいアプローチである。700以上の専門家が精選した文化的アーティファクトからなる知識グラフを活用し、インドの全28州・8連邦直轄領にわたる13の文化属性（歴史、祭りなど）をカバーする3,200以上のマルチホップ質問を生成した。最先端LLMの評価により、Chain-of-Thought（CoT）によるファインチューニングでは低頻度の文化的事実の統合・根拠付けに限界があることが判明した。この課題を解決するため、知識グラフ上の原子的操作を内部的にシミュレートするSymbolic Chain-of-Manipulation（SCoM）フレームワークを提案し、教師ありファインチューニングにおいて標準CoTベースラインを最大20%上回る性能を達成した。

{{< details "原文Abstract" >}}
Large Language Models (LLMs) have made significant progress in reasoning tasks across various domains such as mathematics and coding. However, their performance deteriorates in tasks requiring rich socio-cultural knowledge and diverse local contexts, particularly those involving Indian Culture. Existing Cultural benchmarks are (i) Manually crafted, (ii) contain single-hop questions testing factual recall, and (iii) prohibitively costly to scale, leaving this deficiency largely unmeasured. To address this, we introduce VIRAASAT, a novel, semi-automated multi-hop approach for generating cultural specific multi-hop Question-Answering dataset for Indian culture. VIRAASAT leverages a Knowledge Graph comprising more than 700 expert-curated cultural artifacts, covering 13 key attributes of Indian culture (history, festivals, etc). VIRAASAT spans all 28 states and 8 Union Territories, yielding more than 3,200 multi-hop questions that necessitate chained cultural reasoning. We evaluate current State-of-the-Art (SOTA) LLMs on VIRAASAT and identify key limitations in reasoning wherein fine-tuning on Chain-of-Thought(CoT) traces fails to ground and synthesize low-probability facts. To bridge this gap, we propose a novel framework named Symbolic Chain-of-Manipulation (SCoM). Adapting the Chain-of-Manipulation paradigm, we train the model to simulate atomic Knowledge Graph manipulations internally. SCoM teaches the model to reliably traverse the topological structure of the graph. Experiments on Supervised Fine-Tuning (SFT) demonstrate that SCoM outperforms standard CoT baselines by up to 20%. We release the VIRAASAT dataset along with our findings, laying a strong foundation towards building Culturally Aware Reasoning Models.
{{< /details >}}

## 2. SPQ: An Ensemble Technique for Large Language Model Compression

- **著者**: Jiamin Yao, Eren Gultepe
- **公開日**: 2026-02-20
- **ソース**: [arxiv](http://arxiv.org/abs/2602.18420v1)
- **arXiv ID**: 2602.18420v1

### 要約

本研究は、大規模言語モデル（LLM）の圧縮手法として、分散保持型特異値分解（SVD）、活性化ベースの枝刈り（Pruning）、学習後線形量子化（Quantization）を組み合わせたアンサンブル技術SPQを提案する。各手法はMLPの冗長ニューロン除去、アテンション射影の低ランク分解、全線形層の8ビット量子化というそれぞれ異なる非効率性を対象とし、同一圧縮率において単独手法よりも優れたパープレキシティを達成する。LLaMA-2-7Bへの適用では、最大75%のメモリ削減を実現しつつ、WikiText-2のパープレキシティを5.47から4.91に改善し、C4・TruthfulQA・GSM8Kなどの下流タスクでも精度を維持した。GPTQやSparseGPTといった強力なベースラインと比較しても、SPQはより少ないメモリ使用量（GPTQの7.16GBに対し6.86GB）で競争力のある性能を示し、推論スループットでは最大1.9倍の高速化を達成しており、メモリ制約環境でのLLM実用展開に有効な手法である。

{{< details "原文Abstract" >}}
This study presents an ensemble technique, SPQ (SVD-Pruning-Quantization), for large language model (LLM) compression that combines variance-retained singular value decomposition (SVD), activation-based pruning, and post-training linear quantization. Each component targets a different source of inefficiency: i) pruning removes redundant neurons in MLP layers, ii) SVD reduces attention projections into compact low-rank factors, iii) and 8-bit quantization uniformly compresses all linear layers. At matched compression ratios, SPQ outperforms individual methods (SVD-only, pruning-only, or quantization-only) in perplexity, demonstrating the benefit of combining complementary techniques. Applied to LLaMA-2-7B, SPQ achieves up to 75% memory reduction while maintaining or improving perplexity (e.g., WikiText-2 5.47 to 4.91) and preserving accuracy on downstream benchmarks such as C4, TruthfulQA, and GSM8K. Compared to strong baselines like GPTQ and SparseGPT, SPQ offers competitive perplexity and accuracy while using less memory (6.86 GB vs. 7.16 GB for GPTQ). Moreover, SPQ improves inference throughput over GPTQ, achieving up to a 1.9x speedup, which further enhances its practicality for real-world deployment. The effectiveness of SPQ's robust compression through layer-aware and complementary compression techniques may provide practical deployment of LLMs in memory-constrained environments. Code is available at: https://github.com/JiaminYao/SPQ_LLM_Compression/
{{< /details >}}

## 3. Subgroups of $U(d)$ Induce Natural RNN and Transformer Architectures

- **著者**: Joshua Nunley
- **公開日**: 2026-02-20
- **ソース**: [arxiv](http://arxiv.org/abs/2602.18417v1)
- **arXiv ID**: 2602.18417v1

### 要約

本論文は、U(d)の閉部分群上に隠れ状態を持つ系列モデルの直接的な枠組みを提示する。最小限の公理的設定から出発し、部分群の選択が状態空間・接線射影・更新写像のドロップイン置換として機能する共通の骨格から、リカレント型およびTransformer型のテンプレートを導出する。O(d)に特殊化した直交状態RNNおよびTransformerモデルを、Tiny ShakespeareとPenn Treebankにおいてパラメータ数を揃えた条件で評価している。さらに、接線空間における一般的な線形混合拡張を報告しており、これは部分群の選択に依存せず適用可能であり、現行のO(d)実験において有限パラメータ予算下での性能向上を実現している。

{{< details "原文Abstract" >}}
This paper presents a direct framework for sequence models with hidden states on closed subgroups of U(d). We use a minimal axiomatic setup and derive recurrent and transformer templates from a shared skeleton in which subgroup choice acts as a drop-in replacement for state space, tangent projection, and update map. We then specialize to O(d) and evaluate orthogonal-state RNN and transformer models on Tiny Shakespeare and Penn Treebank under parameter-matched settings. We also report a general linear-mixing extension in tangent space, which applies across subgroup choices and improves finite-budget performance in the current O(d) experiments.
{{< /details >}}

## 4. "How Do I ...?": Procedural Questions Predominate Student-LLM Chatbot Conversations

- **著者**: Alexandra Neagu, Marcus Messer, Peter Johnson, Rhodri Nelson
- **公開日**: 2026-02-20
- **ソース**: [arxiv](http://arxiv.org/abs/2602.18372v1)
- **arXiv ID**: 2602.18372v1

### 要約

本研究は、大規模言語モデル（LLM）ベースの教育用チャットボットに対する学生の質問パターンを、形成的自主学習と総括的評価課題という2つの学習文脈から分析したものである。6,113件のメッセージを11種のLLMと3名の人間評価者により、4つの既存分類スキーマを用いて分類した結果、LLMによる評価者間信頼性は中程度から良好であり、人間評価者よりも一貫性が高いことが示された。両学習文脈において「手続き的（procedural）」質問が最も多く、特に総括的評価の準備時にその傾向が顕著であった。一方で、既存の分類スキーマは複合的なプロンプトの意味的豊かさに対応しきれず、チャットボット統合のリスクと利点の理解には限界があることも明らかになった。今後は、談話心理学における会話分析手法などを適用し、複数ターンにわたる会話の微妙なニュアンスを捉えるアプローチが推奨されている。

{{< details "原文Abstract" >}}
Providing scaffolding through educational chatbots built on Large Language Models (LLM) has potential risks and benefits that remain an open area of research. When students navigate impasses, they ask for help by formulating impasse-driven questions. Within interactions with LLM chatbots, such questions shape the user prompts and drive the pedagogical effectiveness of the chatbot's response. This paper focuses on such student questions from two datasets of distinct learning contexts: formative self-study, and summative assessed coursework. We analysed 6,113 messages from both learning contexts, using 11 different LLMs and three human raters to classify student questions using four existing schemas. On the feasibility of using LLMs as raters, results showed moderate-to-good inter-rater reliability, with higher consistency than human raters. The data showed that 'procedural' questions predominated in both learning contexts, but more so when students prepare for summative assessment. These results provide a basis on which to use LLMs for classification of student questions. However, we identify clear limitations in both the ability to classify with schemas and the value of doing so: schemas are limited and thus struggle to accommodate the semantic richness of composite prompts, offering only partial understanding the wider risks and benefits of chatbot integration. In the future, we recommend an analysis approach that captures the nuanced, multi-turn nature of conversation, for example, by applying methods from conversation analysis in discursive psychology.
{{< /details >}}

## 5. Vichara: Appellate Judgment Prediction and Explanation for the Indian Judicial System

- **著者**: Pavithra PM Nair, Preethu Rose Anish
- **公開日**: 2026-02-20
- **ソース**: [arxiv](http://arxiv.org/abs/2602.18346v1)
- **arXiv ID**: 2602.18346v1

### 要約

Vicharaは、インドの司法制度における控訴審判決の予測と説明を行う新しいフレームワークである。本フレームワークは英語の控訴審訴訟文書を「決定ポイント」（法的争点、判断主体、結果、理由、時間的文脈を含む離散的な法的判断）に分解し、構造化された表現によって正確な予測と解釈可能な説明を実現する。説明の生成にはIRAC（Issue-Rule-Application-Conclusion）フレームワークをインドの法的推論に適応させた構造化フォーマットを採用している。GPT-4o mini、Llama-3.1-8B、Mistral-7B、Qwen2.5-7Bの4つの大規模言語モデルを用いてPredExおよびILDC_expertデータセットで評価した結果、既存の判決予測ベンチマークを上回り、GPT-4o miniが最高性能（F1: PredExで81.5、ILDC_expertで80.3）を達成した。

{{< details "原文Abstract" >}}
In jurisdictions like India, where courts face an extensive backlog of cases, artificial intelligence offers transformative potential for legal judgment prediction. A critical subset of this backlog comprises appellate cases, which are formal decisions issued by higher courts reviewing the rulings of lower courts. To this end, we present Vichara, a novel framework tailored to the Indian judicial system that predicts and explains appellate judgments. Vichara processes English-language appellate case proceeding documents and decomposes them into decision points. Decision points are discrete legal determinations that encapsulate the legal issue, deciding authority, outcome, reasoning, and temporal context. The structured representation isolates the core determinations and their context, enabling accurate predictions and interpretable explanations. Vichara's explanations follow a structured format inspired by the IRAC (Issue-Rule-Application-Conclusion) framework and adapted for Indian legal reasoning. This enhances interpretability, allowing legal professionals to assess the soundness of predictions efficiently. We evaluate Vichara on two datasets, PredEx and the expert-annotated subset of the Indian Legal Documents Corpus (ILDC_expert), using four large language models: GPT-4o mini, Llama-3.1-8B, Mistral-7B, and Qwen2.5-7B. Vichara surpasses existing judgment prediction benchmarks on both datasets, with GPT-4o mini achieving the highest performance (F1: 81.5 on PredEx, 80.3 on ILDC_expert), followed by Llama-3.1-8B. Human evaluation of the generated explanations across Clarity, Linking, and Usefulness metrics highlights GPT-4o mini's superior interpretability.
{{< /details >}}

---

*この記事は自動生成されています。論文の詳細は各ソースURLをご参照ください。*