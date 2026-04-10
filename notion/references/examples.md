# Notion CLI Usage Examples

This guide provides practical examples of how to use `notion-cli` for common tasks.

## Searching for Content

Find pages or databases by name.

```bash
# Search for "Meeting Notes"
notion search "Meeting Notes"
```

## Working with Databases

### Listing Databases
```bash
notion db list
```

### Querying with Filters
```bash
# Find tasks with status "Done" sorted by date
notion db query <db-id> --filter "Status=Done" --sort "Date:desc"

# Complex filter using JSON
notion db query <db-id> --filter-json '{"and": [{"property": "Priority", "select": {"equals": "High"}}, {"property": "Status", "status": {"does_not_equal": "Done"}}]}'
```

### Adding Entries
```bash
# Add a new task
notion db add <db-id> "Name=Review PR" "Priority=High" "Status=In Progress"
```

## Working with Pages

### Creating a Page
```bash
# Create a page in a database
notion page create <db-id> --db "Name=New Feature" "Status=Backlog"
```

### Updating Properties
```bash
# Update a task status
notion page set <page-id> "Status=Done"
```

## Reading and Writing Content

### Reading Content as Markdown
```bash
# Read page content as Markdown (recursive)
notion block list <page-id> --md --all
```

### Appending Content
```bash
# Append a bullet list
notion block append <page-id> --md "- Task 1\n- Task 2"

# Append from a file
notion block append <page-id> --file notes.md
```

## Workspace Management

### List Members
```bash
notion user list
```

### Upload a File
```bash
notion file upload ./report.pdf
```
