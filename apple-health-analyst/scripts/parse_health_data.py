import xml.etree.ElementTree as ET
import csv
import argparse
import os
import zipfile
import shutil

def parse_health_data(input_path, output_dir='.'):
    if not zipfile.is_zipfile(input_path):
        print(f"Error: Input must be a zip archive. '{input_path}' is not a valid zip file.")
        return
    
    print(f"Detected zip archive: {input_path}")
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        prefix = ""
        namelist = zip_ref.namelist()
        if namelist and '/' in namelist[0]:
            prefix = namelist[0].split('/')[0] + '/'
        
        print(f"Extracting all contents to {output_dir}...")
        for member in zip_ref.infolist():
            if member.is_dir(): continue
            filename = member.filename
            relative_path = filename[len(prefix):] if prefix and filename.startswith(prefix) else filename
            if not relative_path: continue
            target_path = os.path.join(output_dir, relative_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                shutil.copyfileobj(source, target)
        
        xml_path = os.path.join(output_dir, "export.xml")
        if os.path.exists(xml_path):
            parse_xml(xml_path, output_dir)
        else:
            print("Error: export.xml not found after extraction.")

def parse_xml(xml_path, output_dir):
    print(f"Parsing {xml_path}...")
    context = ET.iterparse(xml_path, events=("start", "end"))
    
    records_by_type = {}
    workouts_by_type = {}
    activity_summaries, user_info = [], []
    current_workout = None
    
    for event, elem in context:
        if event == "start":
            if elem.tag == "Workout":
                current_workout = dict(elem.attrib)
            elif elem.tag == "Me":
                user_info.append(dict(elem.attrib))
            elif elem.tag == "MetadataEntry" and current_workout is not None:
                key, value = elem.attrib.get('key'), elem.attrib.get('value')
                if key and value:
                    if key == "HKWeatherHumidity" and "%" in value:
                        try:
                            num_part = value.split('%')[0].strip()
                            value = f"{float(num_part) / 100.0:g} %"
                        except ValueError: pass
                    elif key == "HKWeatherTemperature" and "degF" in value:
                        try:
                            num_part = value.split('degF')[0].strip()
                            val_c = (float(num_part) - 32) * 5.0 / 9.0
                            value = f"{val_c:.1f} degC"
                        except ValueError: pass
                    current_workout[f"metadata_{key}"] = value
            elif elem.tag == "WorkoutStatistics" and current_workout is not None:
                stat_type = elem.attrib.get('type', '').replace('HKQuantityTypeIdentifier', '')
                sum_val, unit = elem.attrib.get('sum'), elem.attrib.get('unit')
                if stat_type and sum_val:
                    current_workout[f"stat_{stat_type}_sum"] = sum_val
                    current_workout[f"stat_{stat_type}_unit"] = unit
            elif elem.tag == "FileReference" and current_workout is not None:
                path = elem.attrib.get('path', '')
                current_workout["route_file"] = path[1:] if path.startswith('/') else path
                
        elif event == "end":
            if elem.tag == "Workout":
                w_type = current_workout.get('workoutActivityType', 'Unknown').replace('HKWorkoutActivityType', '')
                if w_type not in workouts_by_type: workouts_by_type[w_type] = []
                workouts_by_type[w_type].append(current_workout)
                current_workout = None
                elem.clear()
            elif elem.tag == "Record":
                r_type = elem.attrib.get('type', 'Unknown').replace('HKQuantityTypeIdentifier', '').replace('HKCategoryTypeIdentifier', '').replace('HKCharacteristicTypeIdentifier', '')
                if r_type not in records_by_type: records_by_type[r_type] = []
                records_by_type[r_type].append(elem.attrib)
                elem.clear()
            elif elem.tag in ["ActivitySummary", "Me"]:
                if elem.tag == "ActivitySummary": activity_summaries.append(elem.attrib)
                elem.clear()
    
    save_to_csv(user_info, "user.csv", output_dir)
    save_to_csv(activity_summaries, "activity_summaries.csv", output_dir)
    
    for r_type, r_data in records_by_type.items():
        save_to_csv(r_data, f"records-{r_type}.csv", output_dir)
    for w_type, w_data in workouts_by_type.items():
        save_to_csv(w_data, f"workouts-{w_type}.csv", output_dir)

def save_to_csv(data, filename, output_dir):
    if not data: return
    path = os.path.join(output_dir, filename)
    all_keys = set()
    for row in data: all_keys.update(row.keys())
    keys = sorted(list(all_keys))
    with open(path, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Saved to {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse Apple Health export zip to CSV')
    parser.add_argument('input_path', help='Path to export.zip')
    parser.add_argument('--out', default='.', help='Output directory')
    args = parser.parse_args()
    parse_health_data(args.input_path, args.out)
