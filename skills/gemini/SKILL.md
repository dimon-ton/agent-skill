---
name: gemini
description: Use this skill whenever the user wants to interact with Google's Gemini CLI tool — including running AI queries, asking Gemini to analyze files or code, managing Gemini extensions, configuring MCP servers, managing skills, resuming sessions, or piping content to Gemini. Trigger on phrases like "ask gemini", "run gemini", "use gemini to", "gemini query", "query with gemini", "send this to gemini", "pipe to gemini", "gemini extensions", "gemini mcp", "gemini skills", "install gemini extension", or any time the user wants to use Gemini as an AI assistant from the terminal. Also trigger when user says things like "can gemini do X" or "have gemini look at this".
---

# Gemini CLI Skill

This skill helps you run Google's Gemini CLI (`@google/gemini-cli`) effectively — constructing the right command for the user's intent and executing it.

## How to use this skill

1. **Understand intent**: Figure out what the user wants to do with Gemini
2. **Construct command**: Pick the right flags and subcommands (see reference below)
3. **Execute**: Run via `Bash` tool — for non-interactive use always use `-p` flag
4. **Handle output**: Show results, pipe further if needed

## Key decision: interactive vs non-interactive

- **Non-interactive** (use `-p`): When you're running gemini programmatically, analyzing files, answering questions, scripting — the vast majority of Claude Code invocations. Output goes to stdout. This is what you should almost always use.
- **Interactive** (no `-p`): Only suggest this when the user explicitly wants a back-and-forth conversation session in their own terminal. You cannot run this via Bash tool — tell the user to run it themselves.

## Core command patterns

```bash
# Non-interactive query (most common — use this for programmatic use)
gemini -p "your question or task here"

# Non-interactive with specific model
gemini -m flash -p "summarize this"

# Non-interactive with JSON output (for scripting)
gemini -o json -p "extract the key points"

# Pipe file content to gemini
cat file.txt | gemini -p "summarize this"

# Pipe and analyze
cat error.log | gemini -p "what caused these errors and how do I fix them?"

# Non-interactive with sandbox (safer for code execution tasks)
gemini -s -p "run the tests and tell me what failed"

# Resume a previous session non-interactively
gemini -r latest -p "now also check for type errors"

# List sessions
gemini --list-sessions

# Check version
gemini --version

# Update gemini
gemini update
```

## When the user wants an interactive session

If the user says "open gemini", "start a gemini session", "chat with gemini" — they want interactive mode. You **cannot** run this via Bash since it needs a TTY. Instead, tell them to run one of these in their terminal:

```bash
gemini                          # Start fresh interactive session
gemini "explain this project"   # Start with an initial prompt, then continue
gemini -i "fix the bug"         # Run prompt then drop into interactive mode
gemini -r latest                # Resume last session interactively
```

## Model selection

The `-m` / `--model` flag accepts these aliases:
- `auto` (default) — best available pro model
- `pro` — Gemini 2.5 Pro, best reasoning
- `flash` — Gemini 2.5 Flash, fast and balanced
- `flash-lite` — Gemini 2.5 Flash Lite, fastest for simple tasks

Use `flash` for quick tasks, `pro` for complex reasoning, leave as default if unsure.

## Subcommand management

For extensions, MCP, and skills management, see `references/subcommands.md` for the full command reference. These are always non-interactive and safe to run via Bash.

## Output formats

- `text` (default) — human-readable
- `json` — structured JSON, good for piping to `jq`
- `stream-json` — newline-delimited JSON events for real-time streaming

Example with JSON output:
```bash
gemini -o json -p "list the top 5 issues in this code" | jq '.[]'
```

## Piping patterns

```bash
# Analyze a file
cat README.md | gemini -p "what does this project do?"

# Analyze code
cat src/main.py | gemini -p "find potential bugs"

# Multiple files (use shell substitution)
gemini -p "review these files for security issues: $(cat auth.py database.py)"

# Git diff review
git diff | gemini -p "summarize these changes and flag any concerns"

# Log analysis
tail -n 100 app.log | gemini -p "what errors are happening and why?"
```

## Important notes

- Gemini CLI is installed at `@google/gemini-cli` (npm global). The `gemini` command should be available in PATH.
- If `gemini` is not found, the user may need to run: `npm install -g @google/gemini-cli`
- Auth: Gemini needs either a Google account (OAuth) or `GEMINI_API_KEY` env var set. If it fails with auth errors, ask the user to run `gemini` interactively once to authenticate.
- The `-p` flag forces non-interactive mode and is essential for scripted/automated use.

## Reference

See `references/subcommands.md` for the full reference on:
- Extensions management commands
- MCP server management commands
- Skills management commands
- All CLI flags and options
