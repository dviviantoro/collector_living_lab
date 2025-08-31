import os, json
from redis_interface import publish_redis
from dotenv import load_dotenv
load_dotenv()

cwd = os.getenv("CWD")
location = os.getenv("DEVICE_LOCATION")
temp_json = cwd + "/temp.json"

def create_temp_json(data, filename = temp_json):
    channel_redis = "energy_ac"
    channel_ac = data.split(",")[0]
    publish_redis(channel_redis, f"{channel_ac}:1")

    dict_fields = {
        "vol": float(data[1]),
        "cur": float(data[2]),
        "pow": float(data[3]),
        "engy": float(data[4]),
        "freq": float(data[5]),
        "pf": float(data[6])
    }
    dictionary = generate_dict("ac", data[0], dict_fields)
    
    all_data = []
    try:
        if os.path.exists(temp_json):
            with open(temp_json, 'r') as json_file:
                all_data = json.load(json_file)
        
        all_data.append(dictionary)
        with open(temp_json, 'w') as json_file:
            json.dump(all_data, json_file, indent=4)
        print(f"New JSON data appended and successfully written to '{temp_json}'")
        
    except FileNotFoundError:
        print(f"The file '{temp_json}' was not found. A new one will be created.")
        # Create the file with the new data.
        with open(temp_json, 'w') as json_file:
            all_data = [dictionary] # Initialize with new data
            json.dump(all_data, json_file, indent=4)
            print(f"New JSON data successfully written to '{temp_json}'")
            
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file. The file may be corrupt: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def generate_dict(measurement, channel, fields):
    new_dict = {}
    new_dict["measurement"] = measurement 
    new_dict["tags"] = {
        "channel": channel,
        "location": location
    }
    new_dict["fields"] = fields
    return new_dict

def parse_data(raw_data):
    data = raw_data.split(",")
    channel = data[0].split("-")[0]

    if channel == "AMB":
        dict_fields = {
            # "bat": float(data[1]),
            "temp": float(data[1]),
            "hum": int(data[2]),
            "lux": int(data[3]),
            "rain": float(data[4])
        }
        dictionary = generate_dict("ambient", data[0], dict_fields)
    elif channel == "SUR":
        dict_fields = {
            # "bat": float(data[1]),
            "temp_top": float(data[1]),
            "temp_bot": float(data[2])
        }
        if dict_fields["temp_top"] < 0 or dict_fields["temp_bot"] < 0:
            dictionary = False
        elif dict_fields["temp_top"] == 85 or dict_fields["temp_bot"] == 85:
            dictionary = False
        else:
            dictionary = generate_dict("surface", data[0], dict_fields)
    elif channel == "AC":
        dict_fields = {
            "vol": float(data[1]),
            "cur": float(data[2]),
            "pow": float(data[3]),
            "engy": float(data[4]),
            "freq": float(data[5]),
            "pf": float(data[6])
        }
        dictionary = generate_dict("ac", data[0], dict_fields)
    elif channel == "IRR":
        dict_fields = {
            "irr": float(data[1]),
            "temp": float(data[2]),
            "hum": float(data[3])
        }
        dictionary = generate_dict("irradiance", data[0], dict_fields)
    elif channel == "EDC":
        dict_fields = {
            "energy": float(data[1])
        }
        dictionary = generate_dict("energy_dc", data[0], dict_fields)
    elif channel == "EAC":
        dict_fields = {
            "energy": float(data[1])
        }
        dictionary = generate_dict("energy_ac", data[0], dict_fields)

    return dictionary
