# Notion CLI Commands Reference

This reference covers the primary command groups and subcommands available in `notion-cli`.

## Authentication & Configuration

Manage your Notion integration token and check connection status.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `auth login` | `notion auth login --with-token` | Authenticate with a Notion integration token. |
| `auth status` | `notion auth status` | Check current authentication status. |
| `auth switch` | `notion auth switch` | Switch between multiple authenticated accounts. |
| `auth doctor` | `notion auth doctor` | Run diagnostics on the connection. |

## Search

Search for pages and databases in your workspace.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `search` | `notion search <query>` | Search entire workspace for a specific string. |

## Database (db)

Manage databases and their entries.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `db list` | `notion db list` | List all databases accessible to the integration. |
| `db query` | `notion db query <db-id>` | Query a database with filters and sorts. |
| `db create` | `notion db create <page-id>` | Create a new database under a parent page. |
| `db add` | `notion db add <db-id>` | Add a single entry to a database. |
| `db add-bulk`| `notion db add-bulk <db-id>`| Add multiple entries from a CSV or JSON file. |

**Key Options for `db query`:**
- `--filter 'Property=Value'`: Simple human-friendly filter.
- `--filter-json '<json>'`: Complex nested filters using raw Notion API syntax.
- `--sort 'Property:asc|desc'`: Sort results by property.

## Page

Manage individual Notion pages.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `page view` | `notion page view <id\|url>` | View page details and properties. |
| `page list` | `notion page list <db-id>` | List pages within a database. |
| `page create` | `notion page create <parent-id>`| Create a new page. |
| `page delete` | `notion page delete <page-id>` | Move a page to trash. |
| `page restore`| `notion page restore <page-id>`| Restore a page from trash. |
| `page move` | `notion page move <id> <parent>`| Move a page to a new parent. |
| `page set` | `notion page set <id> "Prop=Val"`| Update page properties. |

## Block

Manage content blocks within pages.

| Command | Usage | Description |
| :--- | :--- | :--- |
| `block list` | `notion block list <id>` | List all blocks in a page or block. |
| `block get` | `notion block get <block-id>` | Retrieve a specific block's details. |
| `block append`| `notion block append <id>` | Append new blocks to a page or block. |
| `block insert`| `notion block insert <id>` | Insert blocks at a specific position. |
| `block update`| `notion block update <id>` | Update an existing block's content. |
| `block delete`| `notion block delete <id>` | Delete a specific block. |

**Key Options for `block list`:**
- `--md`: Output content as Markdown.
- `--depth <n>`: Recursively read blocks up to depth `n`.
- `--all`: Read all blocks recursively.

## Users & Comments

| Group | Commands | Description |
| :--- | :--- | :--- |
| `user` | `me`, `list`, `get` | Manage workspace members and integration identity. |
| `comment` | `list`, `add`, `get` | Manage discussion threads on pages. |

## Files

| Command | Usage | Description |
| :--- | :--- | :--- |
| `file list` | `notion file list <page-id>` | List files attached to a page. |
| `file upload`| `notion file upload <path>` | Upload a file to Notion. |

## Raw API Access

Use the `api` command as an escape hatch for any Notion API endpoint.

```sh
notion api <METHOD> <path> [payload]
```
Example: `notion api GET /v1/users/me`
