# Skills

Nothing but skills.

These skills follow the [Agent Skills](https://agentskills.io) open standard, ensuring portability and compatibility across AI agent clients that support the standard.

## Installation

### Local
Install a packaged `.skill` file:
```bash
gemini skills install path/to/skill-name.skill --scope user
```

### Remote
Install directly from GitHub:
```bash
gemini skills install https://github.com/ipaddicting/skills.git --path skill-folder-name
```

*Note: For Gemini CLI, run `/skills reload` after installation to activate changes.*

## Available Skills

### [Apple Health Analyst](./apple-health-analyst)
Parse and analyze Apple Health export ZIP archives. Transforms raw `export.xml` and auxiliary data into structured CSV summaries (`records.csv`, `workouts.csv`, `activity_summaries.csv`, `user.csv`) and generates markdown-formatted health reports.

### [Notion](./notion)
Manage Notion pages, databases, and content via the `notion-cli`. Support for searching, querying, updating, and creating content with Markdown support.
