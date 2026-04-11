---
name: apple-health-analyst
description: Parse and analyze Apple Health export ZIP archives. Use when the user wants to extract insights from their health records (records-<Type>.csv, workouts-<Type>.csv, activity_summaries.csv), identify trends, and generate markdown-formatted health reports.
---

# Apple Health Analyst

## Overview

The `apple-health-analyst` skill allows you to transform raw Apple Health `export.zip` archives into actionable insights. It provides a structured workflow for data ingestion (extracting all folders and parsing XML to CSV) and comprehensive analysis (generating trends and markdown reports).

## Workflow

### 1. Data Ingestion

The first step is to parse the raw Apple Health data, provided as a `.zip` archive (e.g., `export.zip`) containing the `apple_health_export/` folder. Use the provided script to extract all contents and generate summaries.

**Command:**
```bash
python3 scripts/parse_health_data.py path/to/export.zip --out output_dir/
```

This will:
1. Extract all sub-folders (e.g., `workout-routes/`, `electrocardiograms/`).
2. Generate `user.csv`: The user's basic health profile (sex, blood type, etc.).
3. Generate `records-<Type>.csv`: Heart rate, steps, etc., split by record type.
4. Generate `workouts-<Type>.csv`: Detailed session data, split by workout type, with relative paths to route files.
5. Generate `activity_summaries.csv`: Daily activity ring data.

### 2. Advanced Data Context

The extracted folders provide deeper context for analysis:
- **`electrocardiograms/*.csv`**: Raw ECG data.
- **`workout-routes/*.gpx`**: GPS data for workouts. Linked in `workouts-<Type>.csv` via the `route_file` column.

### 3. Trend Analysis

Perform analysis based on the extracted data:
- **Activity Trends:** Patterns in steps, distance, and active energy.
- **Vitals Monitoring:** Heart rate, sleep, and other markers.
- **Goal Comparison:** Comparison against benchmarks in `references/benchmarks.md`.

### 4. Report Generation

Present findings as a structured markdown report covering summaries, key metrics, and data-driven insights.

## References

- **[xml_schema.md](references/xml_schema.md):** Detailed structure of Apple Health XML records.
- **[benchmarks.md](references/benchmarks.md):** Standard health ranges and targets for comparison.

## Resources

### scripts/
- **`parse_health_data.py`**: A script to extract ZIP archives and parse health data.
