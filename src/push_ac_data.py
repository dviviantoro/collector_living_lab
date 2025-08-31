import time
import os
import sys
import argparse
import subprocess
import redis
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.influxdb_interface import *
from modules.util import *

host = "127.0.0.1"
port = 6379
db = 0
channel = "energy_ac"

r = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe(channel)

ac_channels = {
    "AC-1": False,
    "AC-2": False,
    "AC-3": False,
    "AC-4": False,
    "AC-5": False,
    "AC-6": False,
}

def ask_write_influx(data):
    command = [
        f"{cwd}/.venv/bin/python",
        f"{cwd}/src/parse_and_write.py",
        "-d", data
    ]
    subprocess.Popen(command)

print("Listening for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        ac_channel = message['data'].split(":")[0]
        status = message['data'].split(":")[1]

        if ac_channel in ac_channels and int(status) == True:
            ac_channels[ac_channel] = True

        
        if all(ac_channels.values()):
            with open(temp_json, 'r') as json_file:
                data_dict = json.load(json_file)
                print(data_dict)
            #     push_data(data_dict)
            # os.remove(temp_json)

            # time.sleep(1)
            # ac_channels = {key: False for key in ac_channels}