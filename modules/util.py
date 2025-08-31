import os, json
from dotenv import load_dotenv
load_dotenv()

cwd = os.getenv("CWD")
location = os.getenv("DEVICE_LOCATION")
temp_json = cwd + "/temp.json"

def create_temp_json(data, filename = temp_json):
    dict_fields = {
        "vol": float(data[1]),
        "cur": float(data[2]),
        "pow": float(data[3]),
        "engy": float(data[4]),
        "freq": float(data[5]),
        "pf": float(data[6])
    }
    dictionary = generate_dict("ac", data[0], dict_fields)
    
    try:
        with open(filename, 'w') as json_file:
            json.dump([dictionary], json_file, indent=4)
        print(f"Initial data successfully written to {filename}")
    except:
        with open(filename, 'r') as json_file:
            data_list = json.load(json_file)

        if isinstance(data_list, list):
            data_list.append(dictionary)
            with open(filename, 'w') as json_file:
                json.dump(data_list, json_file, indent=4)
            print(f"Successfully appended a new record to {filename}")
        else:
            print("Error: The existing file does not contain a list. Cannot append.")

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
