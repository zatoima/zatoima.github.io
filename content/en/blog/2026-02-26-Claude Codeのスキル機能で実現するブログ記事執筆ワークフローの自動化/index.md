---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Automating Blog Post Writing Workflows with Claude Code's Skills Feature"
subtitle: ""
summary: "A summary of a configuration that automates the entire Hugo blog post writing workflow using Claude Code's skills feature, with 9 skills working in coordination. Covers the design patterns and implementation from structure planning, body writing, tag icon generation, a 4-stage quality check (AI writing detection, fact-check, SEO verification, internal link suggestions), and deployment."
tags: ["Claude Code","Hugo","自動化"]
categories: ["Claude Code"]
url: claude-code-skills-blog-writing-automation
date: 2026-02-26
featured: false
draft: true

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## Introduction

This article summarizes a configuration that automates the entire Hugo blog post writing workflow using Claude Code's [skills feature](https://code.claude.com/docs/en/skills). With just a single instruction like "write an article about X," 9 coordinated skills handle everything from structure planning, body writing, a 4-stage quality check, and deployment.

## Overview of Claude Code's Skills Feature

Claude Code skills are a mechanism that extends Claude's capabilities by placing a `.claude/skills/<skill-name>/SKILL.md` file. By simply writing YAML front matter and instructions in Markdown format, the following behaviors become possible:

| Feature | Description |
|---------|-------------|
| Auto trigger | Claude automatically loads skills in conversations that match keywords in the `description` field |
| Manual execution | Can be explicitly launched with a `/skill-name` slash command |
| Subagent integration | Can be isolated for execution within a subagent by specifying `context: fork` |
| Tool restriction | Can limit the available tools with `allowed-tools` |
| Support files | Files other than SKILL.md (templates, references, scripts, etc.) can be stored in the same directory and referenced |

Coordination between skills is also possible—by using the Task tool from one skill's instructions to launch another skill, complex workflows can be built.

## Overall Workflow

The built workflow has 9 skills operating in the following sequence:

```
┌─────────────────────────────────────────────────────────────┐
│  User: "Write an article about X"                           │
└─────────────┬───────────────────────────────────────────────┘
              ▼
┌─────────────────────────┐
│ 1. article-planner      │ ← Structure planning (collect references, generate outline)
│    [User approval gate] │
└─────────────┬───────────┘
              ▼
┌─────────────────────────┐
│ 2. hugo-blog-post       │ ← Write article body and output to file
│    + chart-visualizer   │   (only when diagrams are needed)
└─────────────┬───────────┘
              ▼
┌─────────────────────────┐
│ 3. tag-icon-generator   │ ← Generate SVG icons for unregistered tags
└─────────────┬───────────┘
              ▼
┌─────────────────────────┐
│ 4. Quality checks       │
│  4-1. ai-writing-checker │ ← AI writing detection and auto-fix
│  4-2. blog-fact-checker  │ ← Fact-checking and auto-fix
│  4-3. seo-checker        │ ← SEO verification and summary generation
│  4-4. internal-link-     │ ← Internal link suggestions
│       checker            │
└─────────────┬───────────┘
              ▼
┌─────────────────────────┐
│ 5. hugo-deploy          │ ← Build + GitHub Pages deployment
│    (only on user request)│
└─────────────────────────┘
```

The role of each skill:

| # | Skill name | Role | Execution timing |
|---|------------|------|-----------------|
| 1 | `hugo-blog-post` | Main orchestrator. Defines overall control flow | Launched by user instruction |
| 2 | `article-planner` | Topic analysis, reference collection, outline generation | Auto-launched in Step 2 |
| 3 | `chart-visualizer` | Generating Plotly chart images | When the outline includes diagram instructions |
| 4 | `tag-icon-generator` | Fetching/generating SVG icons for tags | Auto-launched after article output |
| 5 | `ai-writing-checker` | Detection and auto-fix of AI-like writing | Quality check Stage 1 |
| 6 | `blog-fact-checker` | Verification and correction of technical accuracy | Quality check Stage 2 |
| 7 | `seo-checker` | SEO metadata verification and summary generation | Quality check Stage 3 |
| 8 | `internal-link-checker` | Internal link suggestions against existing articles | Quality check Stage 4 |
| 9 | `hugo-deploy` | Hugo build and deployment | Only on explicit user instruction |

## Design and Implementation of Each Skill

### hugo-blog-post (Orchestrator)

This is the main skill that controls the overall workflow. The SKILL.md defines the following information:

- **Project info**: Article storage path, folder naming conventions
- **Front matter template**: YAML header for Hugo articles
- **Writing style rules**: Plain style (da/de aru form), no emojis, concise writing, and other constraints
- **Shortcodes**: Format for link cards, collapsible sections, and callout boxes
- **Execution steps**: Detailed procedures for Steps 1-9 and how to invoke each skill

All other skills are launched as Task tool (subagents) from within this orchestrator's instructions. The advantage is that each check process runs without consuming the main context window.

### article-planner (Structure Planning)

Handles structure planning before article writing. Upon receiving a topic, it executes the following:

1. **Topic analysis**: Clarifying scope and estimating target reader level
2. **Reference collection**: For Snowflake topics, searches with the Snowflake Docs MCP server; otherwise collects official documentation with WebSearch
3. **Outline generation**: Outputs a metadata table (title candidates, URL slug, recommended tags) and section structure
4. **User approval**: Presents the outline and waits for approval before proceeding

The "list of reference document URLs" and "list of technical claims to verify" generated here are handed off to subsequent fact-checking. This design prevents searching for the same information twice.

### Quality Check Pipeline

After article output, 4 stages of checks are executed **sequentially**. They are sequential rather than parallel because each checker reads and writes to the same file, and file conflicts need to be prevented.

**ai-writing-checker (AI Writing Check)**

Uses a two-stage approach of regex patterns and structural analysis to detect characteristics of AI-generated text.

| Check type | Content |
|-----------|---------|
| Regex patterns | Detects mixing of polite form (desu/masu), AI staple phrases like "zehi" (please do), "ikaga deshita desho ka" (how did you find it), etc. |
| Structural analysis | Evaluates diversity of sentence-ending patterns, introduction/conclusion structure, heading count, and logical flow |
| Burstiness | Calculates standard deviation of sentence length and warns when too uniform |

Detection results are quantified as an AI-likeness score from 0-100 and reported in 3 levels: CRITICAL/WARNING/INFO. CRITICAL and mechanically fixable WARNING items are auto-fixed with the Edit tool.

**blog-fact-checker (Fact Check)**

Verifies technical claims in the article against official documentation.

| Verification item | Method |
|------------------|--------|
| Technical accuracy | Searches and cross-references official documentation with Snowflake Docs MCP |
| SQL syntax | Cross-references against syntax references, checks bracket/quote matching |
| URL validity | Access verification via WebFetch (404 detection, redirect detection) |
| Version/date | Verifies consistency with latest versions via WebSearch |

Leverages the reference URL list handed off from article-planner to avoid duplicate searches.

**seo-checker (SEO Check)**

Verifies SEO metadata and auto-generates the `summary` field.

| Check item | Criteria |
|-----------|---------|
| summary | When empty, automatically generates a 100-160 character summary from the article body |
| Title length | 41-59 characters recommended. Warning if out of range |
| URL slug | Must be in English with hyphen separators, within 30 characters |
| og:image | Verifies existence of featured.jpg/png |

**internal-link-checker (Internal Link Check)**

Compares tags and keywords of the new article with existing articles to suggest adding links. Scans front matter of the latest 100 articles and matches articles with matching tags. Designed to output suggestions only without auto-fixing.

### Supplementary Skills

**tag-icon-generator** fetches SVGs from the Simple Icons CDN when a tag in the article's front matter has no registered icon. For tags that don't exist in the CDN, it generates text-based fallback SVGs and automatically updates the mappings in Hugo templates (`tag-icon.html` / `tag-badge-icon.html`).

**hugo-deploy** builds with `hugo --config hugo.toml -d docs` and deploys to GitHub Pages via git commit + push. Executes only when the user explicitly instructs it.

## Design Patterns for Inter-Skill Coordination

The design patterns adopted in this workflow:

**Deduplication via data handoff**

The "list of reference document URLs" and "list of technical claims to verify" collected by article-planner are handed off to blog-fact-checker. The fact-checker first checks the handed-off information and only searches for what's missing. This eliminates the waste of fetching the same document twice.

**Sequential execution for conflict prevention**

The 4 quality check stages run sequentially. Since each checker modifies the same `index.md` with the Edit tool, parallel execution would cause read/write conflicts. Step 9-2 (fact-check) launches after Step 9-1 (AI writing check) completes, and subsequent steps follow the same sequential pattern.

**Delegation to subagents**

Each step of the quality check is launched as a Task tool (`subagent_type="general-purpose"`). This prevents detailed check results from accumulating in the main context window, and only a summary of results is returned when each checker completes.

**User approval gate**

A user approval step is inserted after article-planner presents its outline. By checking the title, URL slug, tags, and section structure before generating the body, direction mismatches can be corrected early.

## Summary

Using Claude Code's skills feature, the entire blog post writing workflow was automated with 9 coordinated skills. From structure planning, article writing, tag icon generation, a 4-stage quality check (AI writing, facts, SEO, internal links), and deployment—everything can be triggered with a single "write an article about X" instruction. The key design points are: deduplication through inter-skill data handoff, conflict prevention through sequential execution, and context preservation through delegation to subagents.

## References

{{< linkcard "https://code.claude.com/docs/en/skills" >}}
