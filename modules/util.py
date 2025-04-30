import os
from dotenv import load_dotenv
load_dotenv()

cwd = os.getenv("CWD")
location = os.getenv("DEVICE_LOCATION")

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
            "bat": float(data[1]),
            "temp": float(data[2]),
            "hum": int(data[3]),
            "lux": int(data[4]),
            "rain": float(data[5])
        }
        dictionary = generate_dict("ambient", data[0], dict_fields)
    elif channel == "SUR":
        dict_fields = {
            "bat": float(data[1]),
            "temp_top": float(data[2]),
            "temp_bot": float(data[3])
        }
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
    elif channel == "DC":
        dict_fields = {
            "vol": float(data[1]),
            "cur": float(data[2])
        }
        dictionary = generate_dict("dc", data[0], dict_fields)
    elif channel == "IRR":
        dict_fields = {
            "irr": float(data[1]),
            "temp": float(data[2]),
            "hum": int(data[3])
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