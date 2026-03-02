---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Verifying the Differences Between Snowflake Cortex AGENT_RUN and DATA_AGENT_RUN"
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

## Introduction

Snowflake Cortex provides two functions for calling agents from SQL.

- [AGENT_RUN (SNOWFLAKE.CORTEX)](https://docs.snowflake.com/en/sql-reference/functions/agent_run-snowflake-cortex) — A function that executes directly without an agent object
- [DATA_AGENT_RUN (SNOWFLAKE.CORTEX)](https://docs.snowflake.com/en/sql-reference/functions/data_agent_run-snowflake-cortex) — A function that calls a pre-created agent object

Both are SQL wrappers for [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents), but they differ in design philosophy and usage. In this article, I verify the differences between the two functions on Snowflake and summarize when to use each one.

## Basic Concepts of Cortex Agents

### What Are Cortex Agents?

Cortex Agents is an AI agent feature that orchestrates across structured and unstructured data to provide insights. It handles task planning, tool-based execution, and response generation in a unified pipeline. This feature became GA in November 2025 and supports the following tools in combination.

| Tool | Type | Overview |
|------|------|----------|
| Cortex Analyst (semantic view) | Structured data | Text-to-SQL using semantic views |
| Cortex Search Service | Unstructured data | Document search via vector search |
| Custom tools | Custom | External APIs and Snowpark Container Services |

### What Is an Agent Object?

An agent object is a managed object created on Snowflake using the `CREATE AGENT` command. It stores model settings, instructions, tool definitions, and other configurations as an object for reuse. Creating this object is a prerequisite for using `DATA_AGENT_RUN`.

## Overview Comparison of AGENT_RUN and DATA_AGENT_RUN

| Item | AGENT_RUN | DATA_AGENT_RUN |
|------|-----------|----------------|
| Agent object | Not required | Required (pre-created with `CREATE AGENT`) |
| First argument | None (only request_body) | Fully qualified name of the agent |
| How settings are passed | Specified directly in request_body | Pre-defined in the agent object |
| Settings available in request_body | All items including model, instructions, orchestration, tools | Only runtime parameters such as messages, stream, tool_choice |
| CI/CD support | △ (settings scattered across code) | ○ (centralized management via `ALTER AGENT`) |
| Primary use case | Testing and prototyping | Production and enterprise use |

## Verification: AGENT_RUN (Without Agent Object)

This executes without creating an agent object, including all settings in the request_body.

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

Execution result (formatted):

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

It works even with a simple call without any settings. When `model` is not specified, it is automatically selected — in this verification, `claude-sonnet-4-5` was chosen.

## Verification: DATA_AGENT_RUN (With Agent Object)

### Step 1: Creating the Agent Object

The `CREATE AGENT` syntax uses `FROM SPECIFICATION $$...$$`. Note that using `SPECIFICATION = $$...$$` will result in a syntax error.

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

### Step 2: Confirming with SHOW AGENTS / DESCRIBE AGENT

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

The settings defined in YAML are stored in JSON format in the `agent_spec` column.

```json
{
  "models": {"orchestration": "claude-sonnet-4-5"},
  "instructions": {"response": "日本語で簡潔に回答する"}
}
```

### Step 3: Calling with DATA_AGENT_RUN

Specify the fully qualified name of the agent (`DB.SCHEMA.AGENT_NAME`) as the first argument.

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

Execution result (formatted):

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

Since the agent object has `instructions: response: "日本語で簡潔に回答する"` (respond concisely in Japanese) defined, the response is returned in Japanese. This difference in response language compared to `AGENT_RUN` clearly illustrates the distinction.

### Comparing Input Token Counts

Comparing input token counts for the same question shows that `DATA_AGENT_RUN` consumes more tokens.

| Function | input_tokens | output_tokens |
|----------|-------------|---------------|
| AGENT_RUN | 82 | 76 |
| DATA_AGENT_RUN | 106 | 97 |

`DATA_AGENT_RUN` automatically appends settings such as `instructions` defined in the agent object as a system prompt, which increases the input token count.

## Parsing the Response

Both functions return a JSON string. By converting it to a VARIANT type with `TRY_PARSE_JSON`, you can access individual fields in subsequent queries.

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

The same path notation works for `DATA_AGENT_RUN` as well. The response schema is identical for both functions.

## When to Use Which

| Perspective | Choose AGENT_RUN | Choose DATA_AGENT_RUN |
|-------------|-----------------|----------------------|
| Purpose | Testing and prototyping | Production applications |
| Configuration management | Want to manage in code (SQL) | Want to manage as Snowflake objects |
| Reusability | Low, as settings must be passed each time | Agent object can be shared across multiple clients |
| CI/CD | Not well suited | Centralized configuration management via `ALTER AGENT` |
| Permissions | `CORTEX_USER` or `CORTEX_AGENT_USER` | Above plus `CREATE AGENT` and `USAGE ON AGENT` required |
| Token consumption | Minimum necessary | Agent configuration overhead is added |

Decision criteria:

- **Want to quickly test things out** → Use `AGENT_RUN` to pass settings directly and verify immediately without creating an agent object
- **Need to share across teams and operate continuously** → Use `DATA_AGENT_RUN` + `CREATE AGENT` to manage settings as objects and centralize changes with `ALTER AGENT`

## Summary

- `AGENT_RUN` does not require an agent object. You can pass the model, instructions, and tools directly in the request_body for immediate execution. Best suited for testing and prototyping
- `DATA_AGENT_RUN` calls an object created with `CREATE AGENT` by name. It is the choice for production use where configuration reuse and CI/CD support are needed
- Both are internally wrappers for the Cortex Agents Run REST API, and the response schema is identical (JSON containing `schema_version`, `role`, `content`, and `metadata`)
- `DATA_AGENT_RUN` appends agent object settings as a system prompt, so input token counts are higher than `AGENT_RUN` for the same question

## References

{{< linkcard "https://docs.snowflake.com/en/sql-reference/functions/agent_run-snowflake-cortex" >}}

{{< linkcard "https://docs.snowflake.com/en/sql-reference/functions/data_agent_run-snowflake-cortex" >}}

{{< linkcard "https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents" >}}

{{< linkcard "https://docs.snowflake.com/en/sql-reference/sql/create-agent" >}}