import csv
import argparse
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone as dt_timezone

def parse_date(date_str):
    if not date_str: return None
    formats = ["%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=dt_timezone.utc)
            return dt
        except ValueError:
            continue
    return None

def get_gpx_metrics(gpx_path):
    """Extracts elevation metrics from a GPX file."""
    metrics = {
        "min_elevation_m": None,
        "max_elevation_m": None,
        "elevation_gain_m": 0.0,
        "elevation_descented_m": 0.0,
    }
    if not os.path.exists(gpx_path): return metrics
    try:
        tree = ET.parse(gpx_path)
        root = tree.getroot()
        ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        elevations = [float(ele.text) for ele in (root.findall('.//gpx:ele', ns) or root.findall('.//ele')) if ele.text]
        if elevations:
            metrics["min_elevation_m"] = round(min(elevations), 2)
            metrics["max_elevation_m"] = round(max(elevations), 2)
            climb = sum(elevations[i] - elevations[i-1] for i in range(1, len(elevations)) if elevations[i] > elevations[i-1])
            descent = sum(abs(elevations[i] - elevations[i-1]) for i in range(1, len(elevations)) if elevations[i] < elevations[i-1])
            metrics["elevation_gain_m"] = round(climb, 2)
            metrics["elevation_descented_m"] = round(descent, 2)
    except Exception: pass
    return metrics

def get_record_stats(record_file, start_dt, end_dt, aggregator='avg'):
    if not os.path.exists(record_file): return None
    values = []
    with open(record_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            record_dt = parse_date(row.get('endDate'))
            if record_dt and start_dt <= record_dt <= end_dt:
                try: values.append(float(row.get('value', 0)))
                except: continue
    if not values: return None
    if aggregator == 'avg': return round(sum(values) / len(values), 2)
    if aggregator == 'max': return round(max(values), 2)
    if aggregator == 'sum': return round(sum(values), 2)
    return None

def get_effort_label(mets):
    if mets <= 0: return "N/A"
    if mets < 3.0: return "light"
    if 3.0 <= mets <= 6.0: return "moderate"
    if mets > 6.0: return "vigorous"
    return "N/A"

def analyze_hiking(data_dir):
    input_file = os.path.join(data_dir, "workouts-Hiking.csv")
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    hr_file = os.path.join(data_dir, "records-HeartRate.csv")
    steps_file = os.path.join(data_dir, "records-StepCount.csv")
    analysis_results = []

    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_dt, end_dt = parse_date(row.get('startDate')), parse_date(row.get('endDate'))
            if not start_dt or not end_dt: continue
            
            print(f"Analyzing hike: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
            work_time_m = float(row.get('duration', 0))
            work_time_s = work_time_m * 60.0
            elapsed_time_s = (end_dt - start_dt).total_seconds()
            distance_km = float(row.get('stat_DistanceWalkingRunning_sum', 0))
            avg_pace = work_time_m / distance_km if distance_km > 0 else 0
            
            ele_asc_raw = row.get('metadata_HKElevationAscended', '0')
            if 'cm' in ele_asc_raw:
                ele_asc_m = float(ele_asc_raw.replace('cm', '').strip()) / 100.0
            else:
                ele_asc_m = float(ele_asc_raw or 0)

            # METs and Effort Level
            mets_raw = row.get('metadata_HKAverageMETs', '0')
            try:
                avg_mets = float(mets_raw.split()[0])
                effort_level = get_effort_label(avg_mets)
            except (ValueError, IndexError):
                avg_mets = 0.0
                effort_level = "N/A"

            hike = {
                "start_time": start_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "timezone": row.get('metadata_HKTimeZone', 'N/A'),
                "work_time_s": round(work_time_s, 2),
                "elapsed_time_s": round(elapsed_time_s, 2),
                "distance_km": round(distance_km, 2),
                "avg_pace": round(avg_pace, 2),
                "avg_mets": round(avg_mets, 2),
                "effort_level": effort_level,
                "calories_kcal": row.get('stat_ActiveEnergyBurned_sum', '0'),
                "humidity": row.get('metadata_HKWeatherHumidity', 'N/A'),
                "temperature": row.get('metadata_HKWeatherTemperature', 'N/A'),
                "elevation_ascended_m": round(ele_asc_m, 2),
            }
            
            route_file = row.get('route_file')
            if route_file: 
                hike.update(get_gpx_metrics(os.path.join(data_dir, route_file)))
            else:
                hike.update({"min_elevation_m": "N/A", "max_elevation_m": "N/A", "elevation_gain_m": "N/A", "elevation_descented_m": "N/A"})
            
            hike["avg_hr"] = get_record_stats(hr_file, start_dt, end_dt, 'avg')
            hike["max_hr"] = get_record_stats(hr_file, start_dt, end_dt, 'max')
            hike["steps"] = get_record_stats(steps_file, start_dt, end_dt, 'sum')
            analysis_results.append(hike)

    if analysis_results:
        output_file = os.path.join(data_dir, "workouts-Hiking-analysis.csv")
        keys = ["start_time", "end_time", "timezone", "work_time_s", "elapsed_time_s", "distance_km", "avg_pace", "avg_mets", "effort_level",
                "elevation_ascended_m", "elevation_gain_m", "elevation_descented_m", "min_elevation_m", "max_elevation_m",
                "avg_hr", "max_hr", "steps", "calories_kcal", "humidity", "temperature"]
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(analysis_results)
        print(f"\nAnalysis complete! Saved to {output_file}")
        print(f"Total hikes processed: {len(analysis_results)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze all hiking records in a directory')
    parser.add_argument('data_dir', help='Directory containing the parsed CSV files')
    args = parser.parse_args()
    analyze_hiking(args.data_dir)
