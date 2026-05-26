---
name: mcp-locator
description: |
  Locate, list, diagnose, and manage MCP servers in Claude Code. Use this skill whenever
  the user asks about MCP servers — even if they phrase it casually. Trigger on: "where is
  my mcp", "list mcp servers", "check mcp", "find mcp server", "mcp not showing", "mcp not
  connected", "add mcp server", "mcp server location", "why is mcp not working", "how do I
  add an mcp", "what mcps do I have", "show my mcp tools", or any variation of these.
  Also trigger when the user says an MCP server is missing, disabled, or not appearing in
  /mcp — they almost certainly need this skill.
---

# MCP Locator

This skill helps users find, check, diagnose, and add MCP servers in Claude Code on Windows.

## Key Fact: Where Claude Code Reads MCP Config

**The only file that matters is `~/.claude.json`** (i.e., `C:\Users\<username>\.claude.json`).

Common misconceptions to watch for:
- `~/.claude/.mcp.json` — Claude Code does NOT read this for MCP servers
- `~/.claude/settings.json` — does NOT support `mcpServers` field
- `.mcp.json` in project directories — only works for project-scoped servers when explicitly approved

## Step 1: List Configured MCP Servers

Read `~/.claude.json` and extract the `mcpServers` section using PowerShell:

```powershell
$config = Get-Content "$env:USERPROFILE\.claude.json" -Raw | ConvertFrom-Json
$config.mcpServers | ConvertTo-Json -Depth 5
```

For each server, show:
| Field | What to display |
|---|---|
| Name | The key (e.g., `word-document-server`) |
| Type | `stdio` or `http` |
| Command | For stdio: `command` + `args` joined; for http: `url` |
| Status hint | See diagnosis section below |

## Step 2: Diagnose Connection Issues

If the user says a server isn't showing as connected in `/mcp`, walk through this checklist:

1. **Wrong config file** — Is the server in `~/.claude.json`? If it's only in `~/.claude/.mcp.json` or `settings.json`, it won't appear. Fix: add it to `~/.claude.json`.

2. **Needs restart** — Claude Code only loads MCP config at startup. After editing `~/.claude.json`, the user must fully restart Claude Code (not just start a new session).

3. **Command not found** — For `stdio` servers, test if the command actually runs:
   - `uvx`-based: `uvx --from <package> <command> --version`
   - `npx`-based: `npx -y <package> --version`
   - Absolute path: verify the path exists with `Test-Path "<path>"`

4. **Missing dependencies** — `uvx` requires Python + uv installed; `npx` requires Node.js + npm.

5. **Server marked disabled** — In `/mcp` dialog, the server shows `◯ disabled`. The user needs to enable it there.

## Step 3: Add a New MCP Server

When the user wants to add a server, collect:
- **Name**: short identifier (e.g., `word-document-server`)
- **Type**: `stdio` or `http`
- For `stdio`: `command` (e.g., `uvx`) and `args` array
- For `http`: `url` and optional `headers`

Then add it to `~/.claude.json` using PowerShell. Read the file first, add the entry, write it back:

```powershell
$config = Get-Content "$env:USERPROFILE\.claude.json" -Raw | ConvertFrom-Json

# For stdio server:
$config.mcpServers | Add-Member -NotePropertyName "<server-name>" -NotePropertyValue ([PSCustomObject]@{
    type    = "stdio"
    command = "<command>"
    args    = @("<arg1>", "<arg2>")
})

# For http server:
$config.mcpServers | Add-Member -NotePropertyName "<server-name>" -NotePropertyValue ([PSCustomObject]@{
    type = "http"
    url  = "<url>"
})

$config | ConvertTo-Json -Depth 10 | Set-Content "$env:USERPROFILE\.claude.json" -Encoding utf8
```

After adding, always remind the user to **restart Claude Code** and then check `/mcp`.

## Common Server Patterns

### Python-based (uvx)
```json
{
  "type": "stdio",
  "command": "uvx",
  "args": ["--from", "<pip-package-name>", "<entry-point>"]
}
```
Example: `uvx --from office-word-mcp-server word_mcp_server`

### Node-based (npx)
```json
{
  "type": "stdio",
  "command": "C:\\Users\\<user>\\AppData\\Roaming\\npm\\npx.cmd",
  "args": ["-y", "<npm-package>"]
}
```
Use the full path to `npx.cmd` on Windows — bare `npx` often fails.

### HTTP server
```json
{
  "type": "http",
  "url": "https://mcp.example.com/mcp",
  "headers": { "Authorization": "Bearer <token>" }
}
```

## What the /mcp Dialog Shows

When the user runs `/mcp` inside Claude Code, they see:
- `✔ connected` — server is running and Claude can use its tools
- `◯ disabled` — server is registered but turned off (enable it in the dialog)
- Missing entirely — server is not in `~/.claude.json` or config was not reloaded

## Verifying a Server Works

To quickly test if a stdio MCP server binary is accessible before adding it:

```powershell
# For uvx-based:
uvx --from <package> <entrypoint> --version 2>&1

# For npx-based:
& "C:\Users\$env:USERNAME\AppData\Roaming\npm\npx.cmd" -y <package> --version 2>&1
```

A successful start (even if it exits with code 1) means the binary works — stdio MCP servers exit when no client connects, which is normal.
