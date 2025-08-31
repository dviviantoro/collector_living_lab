import json
import os

file_path = '/home/pi5/collector_living_lab/temp.json'

# Check if the file exists and is not empty
if os.path.getsize(file_path) > 0:
    with open(file_path, 'r') as json_file:
        try:
            data_dict = json.load(json_file)
            print("Successfully loaded JSON data.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
else:
    print("The JSON file is empty.")