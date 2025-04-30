import time
import os
import sys
import argparse
import subprocess
import redis
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.influxdb_interface import *

host = "127.0.0.1"
port = 6379
db = 0
channel = "energy_ac"

r = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe(channel)

energy_dict = {
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

def last_ac_energy_sentence():
    sentence = """from(bucket: "living_lab")
        |> range(start: -2d)
        |> filter(fn: (r) => r["_measurement"] == "ac")
        |> filter(fn: (r) => r["_field"] == "engy")
        |> filter(fn: (r) => r["channel"] == "AC-1" or r["channel"] == "AC-2" or r["channel"] == "AC-3" or r["channel"] == "AC-4" or r["channel"] == "AC-5" or r["channel"] == "AC-6")
        |> filter(fn: (r) => r["location"] == "smp_it_wasilah_garut")
        |> last()
    """
    return sentence

def get_last_ac_energy(sentence):
    dict_energy = {}
    tables = query_data(sentence)
    for table in tables:
        for record in table.records:
            dict_energy[record["channel"]] = float(record["_value"])
    print(dict_energy)
    return dict_energy

print("Listening for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received message: {message['data']}")
        ac_channel = message['data'].split(":")[0]
        status = message['data'].split(":")[1]

        if ac_channel in energy_dict and int(status) == True:
            energy_dict[ac_channel] = True
        
        if all(energy_dict.values()):
            print("All AC value is TRUE, time to do math operation")
            dict_ac_energy = get_last_ac_energy(last_ac_energy_sentence())

            total_energy = dict_ac_energy["AC-4"] + dict_ac_energy["AC-3"] + dict_ac_energy["AC-2"] - dict_ac_energy["AC-1"]
            print(total_energy)
            ask_write_influx(f"EAC-1,{total_energy}")

            time.sleep(1)
            energy_dict = {key: False for key in energy_dict}
