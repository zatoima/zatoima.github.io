---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflake Cortex の AGENT_RUN と DATA_AGENT_RUN の違いを検証する"
subtitle: ""
summary: " "
tags: ["Snowflake", "Cortex", "AI"]
categories: ["Snowflake"]
url: snowflake-cortex-agent-run-vs-data-agent-run
date: 2026-03-02
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## はじめに

Snowflake Cortex には、エージェントを SQL から呼び出す関数が2つある。

- [AGENT_RUN (SNOWFLAKE.CORTEX)](https://docs.snowflake.com/en/sql-reference/functions/agent_run-snowflake-cortex) — エージェントオブジェクトなしで直接実行する関数
- [DATA_AGENT_RUN (SNOWFLAKE.CORTEX)](https://docs.snowflake.com/en/sql-reference/functions/data_agent_run-snowflake-cortex) — 事前に作成したエージェントオブジェクトを呼び出す関数

どちらも [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) の SQL ラッパーだが、設計思想と使い方が異なる。本記事では両関数の違いを Snowflake 上で実際に検証し、使い分けのポイントを整理する。

## Cortex Agents の基本概念

### Cortex Agents とは

Cortex Agents は、構造化データと非構造化データを横断してオーケストレーションを行い、インサイトを提供する AI エージェント機能。タスクの計画、ツールによる実行、レスポンス生成を一貫して処理する。2025年11月に GA となった機能で、以下のツールを組み合わせて利用できる。

| ツール | 種別 | 概要 |
|--------|------|------|
| Cortex Analyst (semantic view) | 構造化データ | セマンティックビューを使った Text-to-SQL |
| Cortex Search Service | 非構造化データ | ベクトル検索による文書検索 |
| Custom tools | カスタム | 外部 API や Snowpark Container Services |

### エージェントオブジェクトとは

`CREATE AGENT` コマンドで Snowflake 上に作成する管理オブジェクト。モデル設定、指示（instructions）、ツール定義などをオブジェクトとして保存し、再利用できる。`DATA_AGENT_RUN` を使う際は、このオブジェクトの作成が前提となる。

## AGENT_RUN と DATA_AGENT_RUN の概要比較

| 項目 | AGENT_RUN | DATA_AGENT_RUN |
|------|-----------|----------------|
| エージェントオブジェクト | 不要 | 必須（`CREATE AGENT` で事前作成） |
| 第1引数 | なし（request_body のみ） | エージェントの完全修飾名 |
| 設定の渡し方 | request_body に直接記述 | エージェントオブジェクトに定義済み |
| request_body で指定できる設定 | model, instructions, orchestration, tools など全項目 | messages, stream, tool_choice など実行時パラメータのみ |
| CI/CD 対応 | △（設定がコードに分散） | ○（`ALTER AGENT` で設定を集中管理） |
| 主なユースケース | 試験・プロトタイピング | 本番運用・エンタープライズ向け |

## 検証：AGENT_RUN（エージェントオブジェクトなし）

エージェントオブジェクトを作成せず、設定をすべて request_body に含めて実行する。

```sql
SELECT SNOWFLAKE.CORTEX.AGENT_RUN(
  '{
    "messages": [
      {
        "role": "user",
        "content": [{"type": "text", "text": "Snowflake Cortex Agentsとは何ですか？2文で簡潔に答えてください。"}]
      }
    ],
    "stream": false
  }'
) AS response;
```

実行結果（整形）:

```json
{
  "schema_version": "v2",
  "sequence_number": 29,
  "metadata": {
    "usage": {
      "tokens_consumed": [
        {
          "context_window": 200000,
          "input_tokens": {"cache_read": 0, "cache_write": 0, "total": 82, "uncached": 82},
          "model_name": "claude-sonnet-4-5",
          "output_tokens": {"total": 76}
        }
      ]
    }
  },
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Snowflake Cortex Agents is a framework within Snowflake that enables users to build and deploy AI-powered conversational agents that can interact with data directly in Snowflake. These agents leverage large language models and can execute SQL queries, access Snowflake data, and provide intelligent responses to natural language questions about enterprise data."
    }
  ]
}
```

設定なしのシンプルな呼び出しでも動作する。`model` を指定しない場合は自動選択されるが、今回の検証では `claude-sonnet-4-5` が選択された。

## 検証：DATA_AGENT_RUN（エージェントオブジェクトあり）

### Step 1: エージェントオブジェクトの作成

`CREATE AGENT` の構文は `FROM SPECIFICATION $$...$$` を使う。`SPECIFICATION = $$...$$` では構文エラーになるため注意が必要。

```sql
CREATE OR REPLACE AGENT CORTEX_VERIFY_DB.AGENT_TEST.SIMPLE_AGENT
  COMMENT = 'Cortex Agent検証用シンプルエージェント'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-5
  instructions:
    response: "日本語で簡潔に回答する"
  $$;
```

```
+------------------------------------------+
| status                                   |
|------------------------------------------|
| Agent SIMPLE_AGENT successfully created. |
+------------------------------------------+
```

### Step 2: SHOW AGENTS / DESCRIBE AGENT で確認

```sql
SHOW AGENTS;
```

```
+-------------------------+--------------+------------------+------------+----------+---------------------------+---------+
| created_on              | name         | database_name    | schema_name| owner    | comment                   | profile |
|-------------------------+--------------+------------------+------------+----------+---------------------------+---------|
| 2026-03-02 15:26:49.715 | SIMPLE_AGENT | CORTEX_VERIFY_DB | AGENT_TEST | SYSADMIN | Cortex Agent検証用シンプルエージェント | None    |
+-------------------------+--------------+------------------+------------+----------+---------------------------+---------+
```

```sql
DESCRIBE AGENT CORTEX_VERIFY_DB.AGENT_TEST.SIMPLE_AGENT;
```

`agent_spec` カラムに YAML で定義した設定が JSON 形式で格納されているのが確認できる。

```json
{
  "models": {"orchestration": "claude-sonnet-4-5"},
  "instructions": {"response": "日本語で簡潔に回答する"}
}
```

### Step 3: DATA_AGENT_RUN で呼び出し

第1引数にエージェントの完全修飾名（`DB.SCHEMA.AGENT_NAME`）を指定する。

```sql
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'CORTEX_VERIFY_DB.AGENT_TEST.SIMPLE_AGENT',
  '{
    "messages": [
      {
        "role": "user",
        "content": [{"type": "text", "text": "Snowflake Cortex Agentsとは何ですか？2文で簡潔に答えてください。"}]
      }
    ],
    "stream": false
  }'
) AS response;
```

実行結果（整形）:

```json
{
  "schema_version": "v2",
  "sequence_number": 31,
  "metadata": {
    "usage": {
      "tokens_consumed": [
        {
          "context_window": 200000,
          "input_tokens": {"cache_read": 0, "cache_write": 0, "total": 106, "uncached": 106},
          "model_name": "claude-sonnet-4-5",
          "output_tokens": {"total": 97}
        }
      ]
    }
  },
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Snowflake Cortex Agentsは、Snowflakeのデータプラットフォーム上で動作するAIエージェントフレームワークです。自然言語でデータにアクセスし、分析タスクを自動化できる対話型のインテリジェントエージェントを構築するためのサービスです。"
    }
  ]
}
```

エージェントオブジェクトに `instructions: response: "日本語で簡潔に回答する"` を定義しているため、日本語で回答が返っている。`AGENT_RUN` と回答言語が異なる点がわかりやすい違いとなっている。

### 入力トークン数の比較

同じ質問での入力トークン数を比較すると、`DATA_AGENT_RUN` の方が多くなる。

| 関数 | input_tokens | output_tokens |
|------|-------------|---------------|
| AGENT_RUN | 82 | 76 |
| DATA_AGENT_RUN | 106 | 97 |

`DATA_AGENT_RUN` は エージェントオブジェクトに定義した `instructions` などの設定がシステムプロンプトとして自動的に付加されるため、入力トークン数が増加する。

## レスポンスのパース

どちらの関数も JSON 文字列を返す。`TRY_PARSE_JSON` で VARIANT 型に変換することで、後続のクエリで各フィールドにアクセスできる。

```sql
WITH agent_response AS (
  SELECT TRY_PARSE_JSON(
    SNOWFLAKE.CORTEX.AGENT_RUN(
      '{
        "messages": [
          {"role": "user", "content": [{"type": "text", "text": "Snowflake Cortex Agentsとは？"}]}
        ],
        "stream": false
      }'
    )
  ) AS response
)
SELECT
  response:schema_version::STRING                  AS schema_version,
  response:role::STRING                            AS role,
  response:content[0]:text::STRING                 AS answer_text,
  response:metadata:usage:tokens_consumed[0]:model_name::STRING AS model_name,
  response:metadata:usage:tokens_consumed[0]:input_tokens:total::INT  AS input_tokens,
  response:metadata:usage:tokens_consumed[0]:output_tokens:total::INT AS output_tokens
FROM agent_response;
```

```
+----------------+-----------+---------------------------------------+------------------+--------------+---------------+
| SCHEMA_VERSION | ROLE      | ANSWER_TEXT                           | MODEL_NAME       | INPUT_TOKENS | OUTPUT_TOKENS |
|----------------+-----------+---------------------------------------+------------------+--------------+---------------|
| v2             | assistant | Snowflake Cortex Agentsは、Snowflake... | claude-sonnet-4-5 | 82           | 76            |
+----------------+-----------+---------------------------------------+------------------+--------------+---------------+
```

`DATA_AGENT_RUN` でも全く同じパス記法でアクセスできる。レスポンスのスキーマは両関数で共通している。

## 使い分けのポイント

| 観点 | AGENT_RUN を選ぶ | DATA_AGENT_RUN を選ぶ |
|------|-----------------|----------------------|
| 目的 | 試験・プロトタイピング | 本番アプリケーション |
| 設定管理 | コード（SQL）で管理したい | Snowflake オブジェクトとして管理したい |
| 再利用性 | 毎回設定を渡すため低い | エージェントオブジェクトを複数クライアントで共有 |
| CI/CD | 向いていない | `ALTER AGENT` で設定変更を一元管理できる |
| 権限設定 | `CORTEX_USER` または `CORTEX_AGENT_USER` | 上記に加え `CREATE AGENT`、`USAGE ON AGENT` が必要 |
| トークン消費 | 必要最小限 | エージェント設定分が加算される |

どちらを選ぶかの判断基準:

- **まず動かして試したい** → `AGENT_RUN` で設定を直接渡せば、エージェントオブジェクトなしで即座に検証できる
- **チームで共有・継続運用する** → `DATA_AGENT_RUN` + `CREATE AGENT` で設定をオブジェクトとして管理し、`ALTER AGENT` で変更を集中管理する

## まとめ

- `AGENT_RUN` はエージェントオブジェクト不要。モデル、指示、ツールを request_body に直接渡して即時実行できる。試験・プロトタイピングに向いている
- `DATA_AGENT_RUN` は `CREATE AGENT` で作成したオブジェクトを名前で呼び出す。設定の再利用・CI/CD 対応が必要な本番運用向けの選択肢
- どちらも内部的には Cortex Agents Run REST API のラッパーで、レスポンスのスキーマは共通（`schema_version`, `role`, `content`, `metadata` を含む JSON）
- `DATA_AGENT_RUN` はエージェントオブジェクトの設定がシステムプロンプトに付加されるため、同じ質問でも入力トークン数が `AGENT_RUN` より多くなる

## 参考資料

{{< linkcard "https://docs.snowflake.com/en/sql-reference/functions/agent_run-snowflake-cortex" >}}

{{< linkcard "https://docs.snowflake.com/en/sql-reference/functions/data_agent_run-snowflake-cortex" >}}

{{< linkcard "https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents" >}}

{{< linkcard "https://docs.snowflake.com/en/sql-reference/sql/create-agent" >}}
