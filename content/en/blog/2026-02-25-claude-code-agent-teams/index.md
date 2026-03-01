---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Claude Code Agent Teams - Parallel Collaborative Work with Multiple Agents"
subtitle: ""
summary: " "
tags: ["Claude Code","AI","エージェント"]
categories: ["Claude Code"]
url: claude-code-agent-teams-parallel-collaboration
date: 2026-02-25
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

Claude Code has an "agent teams" feature that enables multiple Claude Code instances to work together as a team. One session functions as the leader, assigning tasks to multiple teammates who communicate directly with each other and work in parallel.

This article summarizes how to set up agent teams, the differences from subagents, use cases, and best practices.

Note that agent teams are an **experimental feature** and are disabled by default.

{{< linkcard "https://code.claude.com/docs/ja/agent-teams" >}}

## Agent Team Architecture

Agent teams consist of the following 4 components:

| Component | Role |
|-----------|------|
| Team Leader | The main session that creates the team and generates/coordinates teammates |
| Teammates | Individual Claude Code instances that execute assigned tasks |
| Task List | Shared work item list that teammates request and complete |
| Mailbox | Messaging system for communication between agents |

Each teammate has its own context window and operates completely independently. The leader's conversation history is not inherited, but project context such as CLAUDE.md, MCP servers, and skills are automatically loaded.

## Differences from Subagents

Claude Code has two parallelization means: "subagents (Task tool)" and "agent teams." The core difference is **whether teammates can directly converse with each other**.

| Item | Subagent | Agent Team |
|------|----------|------------|
| Context | Own window. Results returned to caller | Own window. Completely independent |
| Communication | Reports only to main agent | Can send direct messages between teammates |
| Coordination | Main agent manages all work | Self-coordination via shared task list |
| Best for | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| Token Cost | Low (results summarized in main context) | High (each teammate is a separate instance) |

**Selection guideline:**
- "Just return the answer" → subagent
- "Discussion, counterarguments, and collaboration add value" → agent team

## Setup

### Enabling Environment Variables

Add the following to `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

After configuration, restart the Claude Code session to enable it.

### Choosing a Display Mode

Agent teams support two display modes:

| Mode | Description | Requirements |
|------|-------------|--------------|
| in-process | All teammates run within the main terminal | None (default) |
| Split pane | Each teammate gets its own pane | tmux or iTerm2 |

Default is `auto` (split pane within tmux session, otherwise in-process). Can also be explicitly specified via CLI flag:

```bash
claude --teammate-mode in-process
```

## Usage

### Creating a Team

Instruct team creation in natural language. Claude automatically determines the number of teammates, but explicit specification is also possible.

```
Review this PR. Create an agent team with:
- A reviewer focusing on security aspects
- A reviewer focusing on performance aspects
- A reviewer focusing on test coverage aspects
```

To specify count and model explicitly:

```
Parallel refactor this module with 4 teammates.
Use Sonnet for each teammate
```

### Direct Interaction with Teammates

- **in-process mode**: `Shift+Down` to switch between teammates, then enter a message
- **Split pane mode**: Click on the teammate's pane

### Main Operation Keys

| Operation | Key |
|-----------|-----|
| Switch teammate | `Shift+Down` |
| Show task list | `Ctrl+T` |
| Interrupt teammate | `Escape` |
| Show teammate session | `Enter` |

### Requiring Plan Approval

For complex work, you can require teammates to get plan approval before implementing:

```
Create a teammate for auth module refactoring.
Make plan approval mandatory before any changes
```

### Team Cleanup

Always run cleanup from the leader after work is complete:

```
Shutdown teammates
Cleanup the team
```

## Use Cases

### 1. Parallel Code Review

Divide review criteria into independent domains, simultaneously verifying security, performance, and test coverage:

```
Create an agent team to review PR #142:
- A reviewer focusing on security impacts
- A reviewer checking performance impacts
- A reviewer verifying test coverage
Have each report findings after their review
```

### 2. Debugging with Competing Hypotheses

For bugs with unknown causes, verify different hypotheses in parallel and have teammates argue against each other to improve accuracy:

```
Investigate the app disconnecting after 1 message.
Have 5 teammates verify different hypotheses and
argue against each other's theories like a scientific debate.
Document what they agree on
```

### 3. Large-Scale Refactoring

Divide responsibilities by module or layer and work independently in parallel. Be careful that multiple teammates don't edit the same file:

```
Refactor the auth system. Create an agent team:
- Frontend auth-related components lead
- Backend API/middleware lead
- Test rewrite lead
```

### 4. Cross-Layer Coordination

Make changes spanning frontend, backend, and tests with different teammates handling different layers. Unlike subagents, if there are interface changes, teammates can communicate directly to coordinate.

## Best Practices

### Team Size

- Recommended size is **3-5 people**
- Aim for 5-6 tasks per teammate
- 3 focused teammates often outperform 5 diffuse ones

### Task Granularity

| Size | Problem |
|------|---------|
| Too small | Coordination overhead exceeds benefits |
| Too large | Operates for extended periods without check-ins, increased risk of wasted effort |
| Appropriate | Self-contained units that produce clear deliverables like functions, test files, or reviews |

### Avoiding File Conflicts

If 2 teammates edit the same file, overwrites will occur. Divide work so each teammate is responsible for different file sets.

### Monitoring and Steering

Don't let the team run unattended for long periods. Check progress and redirect approaches that aren't working.

### Quality Gates with Hooks

Hooks can be used to enforce rules when teammates complete work:

- `TeammateIdle`: Runs when a teammate becomes idle. Exit code 2 sends feedback and continues work
- `TaskCompleted`: Runs when a task completes. Exit code 2 prevents completion and sends feedback

## Limitations

- in-process teammates are not restored on session resume (`/resume`, `/rewind`)
- Task status updates may be delayed
- Shutdown can take time (waits for current tool calls to complete)
- Only one team per session
- Team nesting is not possible (teammates cannot create their own teams)
- Leader is fixed (cannot be transferred)
- Split pane mode is not supported in VS Code integrated terminal, Windows Terminal, or Ghostty

## Summary

Agent teams are effective for complex tasks requiring "discussion, collaboration, and self-coordination" that subagents cannot handle. They are particularly powerful for parallel code review, debugging with competing hypotheses, and cross-layer refactoring.

However, since token costs increase proportionally with the number of teammates, they are not suitable for routine tasks or sequentially dependent work. Be mindful of when to use subagents versus agent teams, and leverage agent teams when parallel exploration genuinely adds value.

## References

{{< linkcard "https://code.claude.com/docs/ja/agent-teams" >}}

{{< linkcard "https://code.claude.com/docs/ja/sub-agents" >}}
