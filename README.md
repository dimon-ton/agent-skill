# Agent Skill Center

Community skills hub for **opencode** and any agent CLI.

## Quick Start

Add to your `opencode.json`:

```json
{
  "skills": {
    "urls": ["https://dimon-ton.github.io/agent-skill/.well-known/skills/"]
  }
}
```

Or load a single skill:

```json
{
  "skills": {
    "urls": ["https://dimon-ton.github.io/agent-skill/skills/<skill-name>/SKILL.md"]
  }
}
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [docx-edit](skills/docx-edit/SKILL.md) | Edit .docx files preserving formatting |
| [excel-vba](skills/excel-vba/SKILL.md) | Read, edit, run VBA macros in Excel |
| [gemini](skills/gemini/SKILL.md) | Interact with Google Gemini CLI |
| [github-sync](skills/github-sync/SKILL.md) | Sync skills & agents to GitHub |
| [meena-ruangthong](skills/meena-ruangthong/SKILL.md) | Create persona-consistent Meena Ruangthong content and image prompts |
| [mcp-locator](skills/mcp-locator/SKILL.md) | Locate and manage MCP servers |
| [phontan-schedule-reader](skills/phontan-schedule-reader/SKILL.md) | Read Phontan school schedules |
| [phontan-swap-subject](skills/phontan-swap-subject/SKILL.md) | Swap subjects in Phontan timetable |
| [phontan-teacher-analysis](skills/phontan-teacher-analysis/SKILL.md) | Analyze teacher workload |
| [ralph-tui-prd](skills/ralph-tui-prd/SKILL.md) | Generate PRDs for ralph-tui |
| [ralph-tui-create-beads](skills/ralph-tui-create-beads/SKILL.md) | Convert PRDs to beads |
| [ralph-tui-create-beads-rust](skills/ralph-tui-create-beads-rust/SKILL.md) | Convert PRDs to beads (Rust) |
| [ralph-tui-create-json](skills/ralph-tui-create-json/SKILL.md) | Convert PRDs to prd.json |

## Adding a New Skill

1. Create a folder under `skills/<skill-name>/SKILL.md`
2. Push to `main` - the index auto-updates via GitHub Actions
3. Enable GitHub Pages (Settings > Pages > main branch)

## Structure

```
agent-skill/
├── .well-known/skills/index.json    # auto-generated skill index
├── .github/workflows/               # auto-update on push
├── skills/
│   ├── docx-edit/SKILL.md
│   ├── excel-vba/SKILL.md
│   └── ...
└── README.md
```
