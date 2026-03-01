---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Creating a Snowflake Documentation Search MCP Server"
subtitle: ""
summary: " "
tags: ["Snowflake","MCP","Claude Code"]
categories: ["Snowflake","AI"]
url: snowflake-docs-mcp-server-architecture
date: 2026-02-24
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

I created an MCP server that enables searching and retrieving Snowflake official documentation from Claude Code. No API keys or authentication are required; it works by utilizing the internal structure of docs.snowflake.com.

This article describes the technical mechanism of this MCP server.

- GitHub: https://github.com/zatoima/snowflake-docs-mcp-server

## MCP Server Overview

Two tools are provided:

| Tool Name | Function |
|-----------|----------|
| `search_snowflake_docs` | Full-text search of documentation by keyword |
| `get_doc_content` | Retrieve page content of a specified URL in Markdown format |

Register with Claude Code using the following command:

```bash
claude mcp add snowflake-docs -- uv run --directory /path/to/snowflake-docs-mcp-server python server.py
```

## Leveraging Next.js Internal Data Retrieval

The key to this MCP server's implementation is that docs.snowflake.com is built with Next.js. Next.js has an internal endpoint that returns data fetched by `getServerSideProps` as JSON, which this server utilizes.

### Processing Flow

```
1. Fetch HTML from docs.snowflake.com
2. Extract Next.js buildId from HTML using regex
3. Request _next/data/{buildId}/{lang}/search.json?q=...
4. Extract search results from returned JSON
```

### Obtaining the buildId

Next.js applications generate a unique `buildId` at build time. This value is embedded in the HTML source of pages.

```python
async def _get_build_id() -> str:
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        resp = await client.get("https://docs.snowflake.com")
        resp.raise_for_status()
    m = re.search(r'"buildId":"([^"]+)"', resp.text)
    if not m:
        raise ValueError("Could not extract buildId from docs.snowflake.com")
    return m.group(1)
```

The obtained buildId is a random string like `4Vr4FcaZt5TNi0rcHXIGK`. This value changes every time the site is redeployed.

### Request to Search API

Using the buildId, a request is sent to the following URL:

```
https://docs.snowflake.com/_next/data/{buildId}/en/search.json?q=Dynamic+Tables
```

The response is in JSON format, with `pageProps.searchResults.results` containing an array of search results. Each result has fields such as `title`, `href`, `description`, and `category`.

### Retrieving Document Content

The `get_doc_content` tool parses the HTML page at the specified URL using BeautifulSoup and returns the content formatted in Markdown-style.

The processing flow is as follows:

1. Fetch HTML and extract `<article>` or `role="main"` elements
2. Remove unnecessary elements such as `nav`, `footer`, `aside`, sidebar, toc, etc.
3. Convert headings, paragraphs, code blocks, lists, and tables to Markdown format
4. Truncate if `max_length` is exceeded

For security, URLs other than `docs.snowflake.com` are rejected.

## Limitations

- May stop working due to structural changes to docs.snowflake.com (such as changes to the Next.js buildId scheme)
- Since it relies on internal, non-public behavior of the site rather than official APIs, there is a risk it may stop working without notice
- Search accuracy for Japanese documentation (`language: "ja"`) may be lower than for English

## Summary

The Snowflake documentation search MCP server searches and retrieves using Next.js internal endpoints of docs.snowflake.com. Since it doesn't depend on official APIs, no API keys are needed, but the tradeoff is vulnerability to site structure changes.

## Related Articles

{{< linkcard url="https://zatoima.github.io/mcp-server-context-usage-optimization/" title="Measuring and Improving Context Usage of Document MCP Servers" description="Process and results of measuring and improving the context usage of the MCP server created in this article" >}}

{{< linkcard url="https://zatoima.github.io/snowflake-mcp-documentation-server-benchmark/" title="Benchmark Comparison of Two Snowflake MCP Documentation Servers" description="Comparison of this MCP server and Cortex Agent + CKE-based MCP server across 20 queries and 5 evaluation axes" >}}

## References

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}

{{< linkcard "https://modelcontextprotocol.io/" >}}

{{< linkcard "https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props" >}}
