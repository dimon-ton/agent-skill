# Gemini CLI — Full Subcommand & Options Reference

## All CLI Options

| Option | Alias | Type | Default | Description |
|---|---|---|---|---|
| `--debug` | `-d` | boolean | false | Verbose logging |
| `--version` | `-v` | — | — | Show version and exit |
| `--help` | `-h` | — | — | Show help |
| `--model` | `-m` | string | auto | Model: auto, pro, flash, flash-lite, or full model name |
| `--prompt` | `-p` | string | — | Prompt text; forces non-interactive mode |
| `--prompt-interactive` | `-i` | string | — | Run prompt then continue interactively (needs TTY) |
| `--worktree` | `-w` | string | — | Start in a new git worktree (requires experimental.worktrees: true) |
| `--sandbox` | `-s` | boolean | false | Run in sandboxed environment |
| `--approval-mode` | — | string | default | Tool approval: default, auto_edit, yolo |
| `--yolo` | `-y` | boolean | false | Deprecated — use `--approval-mode=yolo` |
| `--extensions` | `-e` | array | — | Specific extensions to use (comma-separated) |
| `--list-extensions` | `-l` | boolean | — | List extensions and exit |
| `--resume` | `-r` | string | — | Resume session: "latest", index number, or session ID |
| `--list-sessions` | — | boolean | — | List available sessions and exit |
| `--delete-session` | — | string | — | Delete session by index |
| `--include-directories` | — | array | — | Additional workspace directories |
| `--allowed-mcp-server-names` | — | array | — | Allowed MCP servers (comma-separated) |
| `--screen-reader` | — | boolean | — | Enable screen reader accessibility mode |
| `--output-format` | `-o` | string | text | Output format: text, json, stream-json |

## Model Aliases

| Alias | Resolves To | Best For |
|---|---|---|
| `auto` | gemini-2.5-pro (default) | General use |
| `pro` | gemini-2.5-pro | Complex reasoning |
| `flash` | gemini-2.5-flash | Fast, balanced |
| `flash-lite` | gemini-2.5-flash-lite | Simple, fast tasks |

## Extensions Management

```bash
gemini extensions list                                         # List installed extensions
gemini extensions install <url-or-path>                        # Install from Git URL or local path
gemini extensions install <url> --ref <branch-or-tag>          # Install specific ref
gemini extensions install <url> --auto-update                  # Install with auto-update
gemini extensions uninstall <name>                             # Uninstall extension
gemini extensions update <name>                                # Update specific extension
gemini extensions update --all                                 # Update all extensions
gemini extensions enable <name>                                # Enable extension
gemini extensions disable <name>                               # Disable extension
gemini extensions link <local-path>                            # Link local extension (dev)
gemini extensions new <path>                                   # Create new extension from template
gemini extensions validate <path>                              # Validate extension structure
```

## MCP Server Management

```bash
gemini mcp list                                                # List configured MCP servers
gemini mcp add <name> <command>                                # Add stdio-based MCP server
gemini mcp add <name> <url> --transport http                   # Add HTTP-based MCP server
gemini mcp add <name> <cmd> --env KEY=value                    # Add with env vars
gemini mcp add <name> <cmd> --scope user                       # Add with user scope
gemini mcp add <name> <cmd> --include-tools tool1,tool2        # Add with specific tools only
gemini mcp remove <name>                                       # Remove MCP server
```

## Skills Management

```bash
gemini skills list                                             # List discovered skills
gemini skills install <source>                                 # Install from Git, path, or file
gemini skills link <path>                                      # Link local skills via symlink
gemini skills uninstall <name>                                 # Uninstall a skill
gemini skills enable <name>                                    # Enable a skill
gemini skills disable <name>                                   # Disable a skill
gemini skills enable --all                                     # Enable all skills
gemini skills disable --all                                    # Disable all skills
```

## Interactive REPL Commands (inside a running gemini session)

These slash commands are typed inside an active `gemini` interactive session — not from the shell:

| Command | Description |
|---|---|
| `/help` | Show all available commands |
| `/quit` | Exit the session |
| `/memory reload` | Reload GEMINI.md context files |
| `/skills reload` | Reload skills from disk |
| `/agents reload` | Reload agent registry |
| `/commands reload` | Reload custom slash commands |
| `/mcp reload` | Restart and reload MCP servers |
| `/extensions reload` | Reload all active extensions |

## Session Management

```bash
gemini --list-sessions                    # Show all saved sessions
gemini -r latest                          # Resume most recent session
gemini -r latest -p "continue the task"  # Resume + non-interactive prompt
gemini -r 3                               # Resume session by index number
gemini -r abc123 "next step"             # Resume by ID with new prompt
gemini --delete-session 3                 # Delete session by index
```
