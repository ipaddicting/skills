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

### 4. Hiking Analysis

A dedicated script for hiking enthusiasts to correlate trail performance with health and environmental data.

**Command:**
```bash
python3 scripts/analyze_hiking.py output_dir/
```

This will:
1. **Time Tracking:** Calculate `work_time_s` (active duration) vs `elapsed_time_s`.
2. **Terrain Analysis:** Compute cumulative `elevation_gain_m` and `elevation_descented_m` from GPX route files.
3. **Heart Rate Correlation:** Capture `avg_hr` and `max_hr` specifically for the hike duration.
4. **Effort Mapping:** Categorize intensity based on METs (Light < 3.0, Moderate 3.0-6.0, Vigorous > 6.0).
5. **Weather Context:** Include temperature and humidity metadata from the workout.
6. **Consolidated Report:** Generate `workouts-Hiking-analysis.csv` in the output directory.

### 5. Report Generation

Present findings as a structured markdown report covering summaries, key metrics, and data-driven insights.

## References

- **[xml_schema.md](references/xml_schema.md):** Detailed structure of Apple Health XML records.
- **[benchmarks.md](references/benchmarks.md):** Standard health ranges and targets for comparison.

## Resources

### scripts/
- **`parse_health_data.py`**: A script to extract ZIP archives and parse health data.
- **`analyze_hiking.py`**: A script to perform detailed hiking performance and health correlation.
