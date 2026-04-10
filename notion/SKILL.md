---
name: notion
description: Manage Notion pages, databases, and content via the `notion-cli`. Use this skill when you need to search for content, query/update databases, create pages, or read/append content (with Markdown support) in a Notion workspace.
---

# Notion CLI Skill

This skill provides a structured way to interact with the Notion API using the `notion-cli` tool. It enables seamless management of pages, databases, and blocks directly from the command line.

## Overview

The `notion` skill empowers Gemini CLI to perform complex operations in Notion, such as querying databases with human-friendly filters, reading page content as Markdown, and automating property updates.

## Core Capabilities

1. **Search & Discovery**: Find pages and databases across the workspace.
2. **Database Management**: Query entries with human-friendly syntax, add single or bulk entries, and create new databases.
3. **Page Operations**: Create, view, update, move, or delete pages.
4. **Content Manipulation**: Read content recursively as Markdown (`--md`) and append new content from strings or files.
5. **Workspace Management**: Manage users, comments, and file uploads.
6. **Raw API Access**: Direct access to any Notion API endpoint via the `api` command.

## Workflow Patterns

### 1. Reading and Analyzing Content
When asked to summarize or analyze a Notion page:
1. Use `notion search <query>` to find the page if the ID is unknown.
2. Use `notion block list <page-id> --md --all` to fetch the full content.
3. Process the Markdown content as requested.

### 2. Updating Databases
When asked to update a task or database entry:
1. Use `notion db query <db-id> --filter 'Name=Target'` to find the entry.
2. Use `notion page set <page-id> "Status=Done"` to update properties.

### 3. Creating Content
When asked to create a new report or entry:
1. Use `notion page create <parent-id>` or `notion db add <db-id>`.
2. Use `notion block append <page-id> --md "..."` to add content blocks.

## Command Reference

For a full list of commands and options, see [references/commands.md](references/commands.md).

## Usage Examples

For practical usage patterns and code snippets, see [references/examples.md](references/examples.md).

## Troubleshooting

- **Auth Issues**: Run `notion auth doctor` to check the connection.
- **Missing Token**: Ensure the `NOTION_TOKEN` environment variable is set or use `notion auth login`.
- **API Errors**: Use `notion api` for direct endpoint debugging if a high-level command fails.
