---
name: github-sync
description: Sync opencode skills and agents to the GitHub repository dimon-ton/opencode-skills. Trigger when user wants to push, upload, sync, or update skills/agents to GitHub. Also trigger on phrases like "push skills to github", "sync skills", "upload agents", "update opencode-skills repo", "push to github".
---

# github-sync: Sync OpenCode Skills & Agents to GitHub

## When to Use

Use this skill when the user wants to:
- Push new or updated skills to the GitHub repo
- Push new or updated agents to the GitHub repo
- Sync all opencode config changes to GitHub
- Create a new skill and push it to GitHub

## Configuration

- **GitHub repo**: `dimon-ton/opencode-skills`
- **Local clone**: `C:\Users\saich\AppData\Local\Temp\opencode-skills`
- **Source skills**: `C:\Users\saich\.config\opencode\skills\`
- **Source agents**: `C:\Users\saich\.config\opencode\agents\`

## Workflow

### Step 1: Detect what changed

Compare source files with the local clone to find changes:

```bash
# Run from the local clone directory
# Compare skills
diff -r "C:\Users\saich\.config\opencode\skills" "C:\Users\saich\AppData\Local\Temp\opencode-skills\skills"

# Compare agents
diff -r "C:\Users\saich\.config\opencode\agents" "C:\Users\saich\AppData\Local\Temp\opencode-skills\agents"
```

### Step 2: Copy changed files to local clone

```powershell
# Copy all skills (preserves structure)
Copy-Item -Path "C:\Users\saich\.config\opencode\skills\*" -Destination "C:\Users\saich\AppData\Local\Temp\opencode-skills\skills\" -Recurse -Force

# Copy all agents
Copy-Item -Path "C:\Users\saich\.config\opencode\agents\*" -Destination "C:\Users\saich\AppData\Local\Temp\opencode-skills\agents\" -Recurse -Force
```

Or copy individual files if only one skill/agent changed:

```powershell
# Single skill
Copy-Item -Path "C:\Users\saich\.config\opencode\skills\<skill-name>\SKILL.md" -Destination "C:\Users\saich\AppData\Local\Temp\opencode-skills\skills\<skill-name>\SKILL.md" -Force

# Single agent
Copy-Item -Path "C:\Users\saich\.config\opencode\agents\<agent-name>.md" -Destination "C:\Users\saich\AppData\Local\Temp\opencode-skills\agents\<agent-name>.md" -Force
```

### Step 3: Commit and push

```powershell
# Stage, commit, and push (run from local clone directory)
git add -A
git status  # review what changed
git commit -m "Update skills/agents: <describe changes>"
git push origin main
```

### Step 4: Update README if new skill/agent added

When a NEW skill or agent is added, update the README tables:

```
## Skills
| Skill | Description |
|-------|-------------|
| [skill-name](skills/skill-name/SKILL.md) | <description> |

## Agents
| Agent | Description |
|-------|-------------|
| [agent-name](agents/agent-name.md) | <description> |
```

## Full Sync (one-liner)

To sync everything at once:

```powershell
# All-in-one sync command
$repo = "C:\Users\saich\AppData\Local\Temp\opencode-skills"
Copy-Item -Path "C:\Users\saich\.config\opencode\skills\*" -Destination "$repo\skills\" -Recurse -Force
Copy-Item -Path "C:\Users\saich\.config\opencode\agents\*" -Destination "$repo\agents\" -Recurse -Force
Set-Location $repo; git add -A; git status
```

Then review and commit:

```powershell
git commit -m "Sync: <message>"; git push origin main
```

## Creating a New Skill

If the user asks to create a new skill AND push it:

1. Create the skill folder under `C:\Users\saich\.config\opencode\skills\<name>\SKILL.md`
2. Follow the SKILL.md format with frontmatter (name, description)
3. Then follow the sync workflow above

## Safety Rules

1. **Never force push** (`--force`) unless the user explicitly asks
2. **Always run `git status`** before committing to review changes
3. **Never commit secrets** - check for API keys, tokens, passwords in files
4. **Always use descriptive commit messages** that mention what skill/agent changed
5. **Pull before push** if working from multiple machines: `git pull origin main`
