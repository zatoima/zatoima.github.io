---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Measuring and Improving Context Usage of Document MCP Servers"
subtitle: ""
summary: " "
tags: ["MCP","Claude","LLM","Snowflake"]
categories: ["MCP","LLM"]
url: mcp-server-context-usage-optimization
date: 2026-02-25
featured: false
draft: false

# Featured image
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## Introduction

MCP servers provide external tools to LLM agents, but all tool responses go into the LLM's context window. This means the amount of data an MCP tool returns directly translates to context consumption.

This article documents the process and results of measuring the context usage of my custom Snowflake Docs MCP server, identifying issues, and implementing improvements.

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}


## The Relationship Between MCP Tool Responses and Context

The results of MCP tool calls are loaded into the context window as input to the LLM.

```text
[User message] + [System prompt] + [MCP tool results] + [Past conversation] = Context consumption
```

Document retrieval MCP tools can return thousands to tens of thousands of characters per call. Without careful design, just a few calls can consume most of the context, making it difficult to continue the conversation.

### When Using Subagents

When MCP tools are used via Claude Code's subagent (Task tool), the raw tool responses stay within the subagent's context, and only a summary is returned to the main context. This can dramatically reduce main context consumption.

| Method | Main context consumption |
|---|---|
| Direct call | Full text of tool results |
| Via subagent | Summary only (50-90% reduction) |

However, since subagents increase total token consumption and add latency, routing everything through subagents is not practical. It is important to control response sizes appropriately on the MCP server side.

## State Before Improvement

Before improvement, the server provided two tools.

| Tool | Function |
|---|---|
| `search_snowflake_docs` | Keyword search (excerpt 200 chars, max 20 results) |
| `get_doc_content` | Full page retrieval (HTML to Markdown conversion) |

### Measurement Results

Measurements were taken using the CREATE TABLE page (one of the largest pages in Snowflake documentation).

**search_snowflake_docs:**

| max_results | Response chars | Estimated tokens |
|---|---|---|
| 3 results | ~850 | ~250 |
| 5 results (default) | ~1,400 | ~400 |
| 10 results | ~2,800 | ~800 |
| 20 results (max) | ~5,500 | ~1,500 |

The search tool is lightweight and not problematic.

**get_doc_content:**

| max_length | Response chars | Estimated tokens | Notes |
|---|---|---|---|
| 2,000 | ~2,200 | ~600 | |
| 4,000 | ~4,200 | ~1,100 | |
| 8,000 (default) | ~8,200 | ~2,200 | |
| 0 (unlimited) | **102,079** | **~25,000+** | Exceeds context limit |

### Issues Identified

**1. Text Duplication Bug**

The HTML to Markdown conversion used a `descendants` iterator, causing the same text to appear twice for `<p>` tags inside `<li>` elements.

```text
- Requires a value (NOT NULL).
Requires a value (NOT NULL).          ← duplicate

- Has a default value.
Has a default value.                  ← duplicate
```

A list of 10 items expanded to 20 lines, with **30-40% of content wasted on unnecessary duplication**.

**2. Context Failure at max_length=0**

Retrieving the CREATE TABLE page without limits returned 102,079 characters, exceeding Claude Code's token limit and being offloaded to a file. Once offloaded to a file, it can no longer be directly referenced within the context, making it essentially unusable.

**3. No Way to Retrieve Specific Sections**

The approach of truncating from the beginning of the page to `max_length` characters made it impossible to reach important information in the latter half of pages, such as Usage Notes or Examples.

**4. No Way to Check Page Structure**

To find out what sections existed, a full page retrieval with `get_doc_content` was required.

**5. Noise in Markdown Output**

After HTML to Markdown conversion, many unnecessary artifacts remained for the LLM.

```text
## Usage notes[¶](#usage-notes "Link to this heading")     ← pilcrow links (~40 chars/heading)
Copy                                                        ← remnants of copy buttons
[COPY INTO <table>](copy-into-table)                        ← unresolvable relative links
```

The CREATE TABLE page alone (with 24 headings) consumed approximately 960 characters in pilcrow links.

## Improvement Process

### Studying the AWS Official MCP Server

As a reference for improvements, I studied the implementation of the documentation MCP server officially provided by AWS. Key design points that were instructive:

- **Using the markdownify library**: Rather than a hand-written HTML parser, it uses the `markdownify` library for HTML to Markdown conversion, which structurally prevents issues like duplication bugs
- **Pagination via start_index**: Design for reading long documents in chunks using the `start_index` parameter
- **Safe max_length constraint**: Pydantic Field with `gt=0, lt=1000000` constraint to prevent 0 (unlimited) input
- **Best practices in instructions**: Explicitly states "Stop reading documents over 30,000 characters once the needed information is found"

### Improvement 1: HTML to Markdown Conversion Quality

Replaced the hand-written `descendants` loop with the `markdownify` library. This resolved the text duplication bug, effectively increasing the information density by approximately 1.5x for the same character count.

Additionally, implemented noise removal after Markdown conversion:

- Remove pilcrow links (`[¶](...)`)
- Remove copy button remnants (`Copy`)
- Remove link URLs (keep text only)
- Remove image and SVG tags
- Remove feedback, rating, survey, and form elements

The key is separating the removal stages. Buttons and images are removed at the HTML stage with `decompose()`, while pilcrow and Copy remnants are removed at the text level after Markdown conversion. `<a>` tags are `unwrap()`-ed to remove the tag while preserving the text.

### Improvement 2: Introducing Gradual Information Retrieval

Expanded from 2 tools to 5, enabling gradual information retrieval.

```text
search_snowflake_docs  → Document search (with include_headings=True, can also get TOC simultaneously)
search_in_doc          → In-page keyword search (auto-selects relevant sections)
get_doc_toc            → Get page table of contents (lightweight)
get_doc_section        → Retrieve a specific section
get_doc_content        → Retrieve full page content (with pagination)
```

Recommended usage flow:

```text
1. search_snowflake_docs(include_headings=True) to get search results + TOC in one call
2. search_in_doc to automatically extract only relevant sections
3. Only specify include_code_blocks=True when code examples are needed
```

### Improvement 3: Response Size Control

Added a hard cap on `max_length` to prevent context failures.

| max_length value | Behavior |
|---|---|
| 0 | Honors full retrieval intent, returns up to hard cap (20,000) |
| 1–20,000 | Uses specified value as-is |
| 20,001+ | Capped at 20,000 |
| Negative | Falls back to default (5,000) |

Additionally introduced pagination via `start_index` parameter and natural boundary cutting (priority: paragraph → line → sentence → word).

### Improvement 4: Code Blocks Off by Default

Code blocks occupy the majority of context on syntax reference pages. Measurements on the CREATE TABLE page showed that removing code blocks achieves a **37.7% context reduction**.

| Mode | Size | Reduction |
|---|---|---|
| Code blocks ON | 52,694 chars | - |
| Code blocks OFF | 32,851 chars | 37.7% |

Changed the default value of the `include_code_blocks` parameter to `False`, requiring explicit specification only when syntax or code examples are needed.

### Improvement 5: Reducing Tool Call Count

Added the `include_headings` parameter to `search_snowflake_docs`, enabling retrieval of heading structure simultaneously with search.

```text
Before: search → get_doc_toc → get_doc_section  (3 calls)
After:  search(include_headings=True) → get_doc_section  (2 calls)
```

However, pages with many headings (DB2 migration guides with 120+ headings, etc.) caused response bloat, so a cap of 30 headings per result was added. When exceeded, it narrows down to h1-h3 only.

### Improvement 6: In-Page Keyword Search

Added the `search_in_doc` tool. Passing a URL and keyword scores all sections within the page and returns only the most relevant sections. This enables the MCP server itself to handle the judgment of TOC review → section selection.

A scoring accuracy issue arose: because a parent section's `get_text()` includes all child section text, parent scores were always higher. Resolved by excluding child section text from parent scores and deduplicating nested results.

### Improvement 7: Caching and Performance Improvements

- In-memory cache with TTL to eliminate duplicate HTTP fetches of the same URL (5 minutes, LRU limit of 50 entries)
- buildId cache (1 hour TTL)
- Connection pooling via shared HTTP client
- Parallel heading retrieval via `asyncio.gather`

## Improvement Results

### Full Page Retrieval Comparison for get_doc_content

Comparison of full page retrieval of the CREATE TABLE page using `get_doc_content(include_code_blocks=False)`.

| Condition | Before | After | Notes |
|---|---|---|---|
| max_length=2000 | ~2,200 chars (30-40% duplicate) | 2,269 chars (no duplicates) | ~1.5x information per character |
| max_length=5000 | — | 5,351 chars | New default after improvement |
| max_length=8000 | ~8,200 chars (30-40% duplicate) | 8,450 chars (no duplicates) | Previous default |
| max_length=0 | **102,079 chars (context failure)** | **20,000 or less (safe)** | 95%+ reduction |

### Full Page Retrieval Comparison Across Multiple Pages

Verified the same effect applies to pages other than CREATE TABLE.

| Page | Before | After | Reduction |
|---|---|---|---|
| CREATE TABLE (large SQL reference) | 70,948 chars | 44,503 chars | **37.3%** |
| SELECT (large SQL reference) | 25,068 chars | 10,538 chars | **58.0%** |
| Dynamic Tables (medium guide) | 5,409 chars | 4,529 chars | **16.3%** |
| **Total** | **101,425 chars** | **59,570 chars** | **41.3%** |

Reference pages with many links show greater improvement, achieving 58% reduction on the SELECT page. Small guide pages show relatively smaller reduction rates, but since the original size is small, the practical impact is minimal.

### Typical Usage Pattern Comparison

| Pattern | Before | After | Improvement |
|---|---|---|---|
| search + get_doc_content | ~9,600 chars | 7,378 chars | 23% reduction |
| search + 2x get_doc_content | ~17,800 chars | 12,714 chars | 29% reduction |
| search + TOC + 1 section | Not possible | 9,408 chars | New feature |
| search(headings) + section(code=OFF) | Not possible | 3,115 chars | **Optimal flow** |
| Want only Usage Notes | Not possible (unreachable) | 5,267 chars | New feature |

The most efficient flow (`search(max_results=1, include_headings=True)` → `get_doc_section(code=OFF)`) achieves approximately **58% context reduction** compared to the typical pre-improvement flow.

### Context Consumption of New Tools

| Tool | Consumption | Use case |
|---|---|---|
| `search_snowflake_docs` (3 results) | ~850 chars | Search results only |
| `get_doc_toc` | ~600 chars | Checking page structure |
| `get_doc_section` (1 section) | ~528 chars | Retrieving a specific section |
| `search_in_doc` (3 sections) | ~2,400 chars | Auto-extracting relevant sections |
| `get_doc_content` (full, code=OFF) | ~44,503 chars | Entire page |

Using `search_in_doc` to retrieve only needed sections requires about 1/9th the context of a full `get_doc_content` retrieval.

### Impact of include_headings

| Pattern | Estimated chars |
|---|---|
| search (5 results, headings=false) | ~500 chars |
| search (5 results, headings=true) | ~3,500–5,000 chars |

`include_headings=true` consumes approximately 7-10x more context, but saves the `get_doc_toc` call. Before the heading cap was introduced, pages with many headings could expand to 26,443+ characters; after introduction, it stays within 10,853 characters (**59% reduction**).

## Key Points for Designing Document MCP Servers

Here is a summary of the insights gained from this improvement work.

1. **Set a hard cap on response size** — Unlimited retrieval risks context failure
2. **Provide pagination** — Enable chunked reading with `start_index` + `max_length`
3. **Enable gradual information retrieval** — Search → lightweight TOC check → section retrieval (only what's needed)
4. **Use a library for HTML to Markdown conversion** — Hand-written HTML parsers are a source of bugs
5. **Document best practices in instructions** — Provide guidance from the server side on how the LLM should use the tools
6. **Reduce tool call count** — Provide options to consolidate multiple tool calls into one
7. **Exclude code blocks by default** — Code blocks occupy 30-40% of responses on syntax reference pages
8. **Cache to eliminate duplicate HTTP fetches** — Consecutive access to the same URL is common
9. **Remove noise from Markdown output** — Remove pilcrow links, copy buttons, link URLs, image tags, etc.
10. **Add safety limits to parameters returning large amounts of data** — Set caps like heading caps

## Summary

The context usage of my custom Snowflake Docs MCP server was measured and the following improvements were made.

| Improvement | Effect |
|---|---|
| HTML to Markdown conversion quality | Eliminated duplication, noise removal: **average 41.3% reduction** in full retrieval |
| Gradual information retrieval | Retrieve only needed sections: **about 1/9th** of full page |
| Code blocks off by default | **37.7% reduction** |
| Reduced tool call count | 3 steps → 2 steps |
| Response size control | 102,079 chars → **20,000 or less** (prevents failure) |
| Optimal flow overall | **~58% context reduction** |

When designing MCP servers, it is important to be aware that response size equals LLM context consumption, and to design with the principle of "returning only the necessary information, in the necessary amount, without noise."

## Related Articles

{{< linkcard url="https://zatoima.github.io/snowflake-docs-mcp-server-architecture/" title="Creating a Snowflake Documentation Search MCP Server" description="Technical mechanism of the MCP server (Next.js buildId retrieval, search API, HTML to Markdown conversion)" >}}

{{< linkcard url="https://zatoima.github.io/snowflake-mcp-documentation-server-benchmark/" title="Benchmark Comparison of Two Snowflake MCP Documentation Servers" description="Comparison of this MCP server and a Cortex Agent + CKE-based MCP server across 20 queries and 5 evaluation axes" >}}

## References

{{< linkcard "https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server" >}}

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}

{{< linkcard "https://pypi.org/project/markdownify/" >}}
