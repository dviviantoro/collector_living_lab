import os
import sys
import argparse
import subprocess
import redis
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.influxdb_interface import query_data

host = "127.0.0.1"
port = 6379
db = 0
channel = "energy_watcher"

r = redis.StrictRedis(host=host, port=port, db=db)
pubsub = r.pubsub()
pubsub.subscribe(channel)

energy_dict = {
    "EDC-1": False,
    "EDC-2": False,
    "EDC-3": False,
    "EDC-4": False,
}

def last_parital_energy_sentence():
    sentence = """from(bucket: "living_lab")
        |> range(start: -2d)
        |> filter(fn: (r) => r["_measurement"] == "energy_dc")
        |> filter(fn: (r) => r["_field"] == "energy")
        |> filter(fn: (r) => r["channel"] == "EDC-1" or r["channel"] == "EDC-2" or r["channel"] == "EDC-3" or r["channel"] == "EDC-4")
        |> filter(fn: (r) => r["location"] == "smp_it_wasilah_garut")
        |> last()
    """
    return sentence

def last_total_energy_sentence():
    sentence = """from(bucket: "living_lab")
        |> range(start: -2d)
        |> filter(fn: (r) => r["_measurement"] == "energy_dc")
        |> filter(fn: (r) => r["_field"] == "energy")
        |> filter(fn: (r) => r["channel"] == "SUM")
        |> filter(fn: (r) => r["location"] == "smp_it_wasilah_garut")
        |> last()
    """
    return sentence

def get_last_parital_energy(sentence):
    list_last_value = []
    tables = query_data(sentence)
    for table in tables:
        for record in table.records:
            list_last_value.append(record["_value"])
    print(list_last_value)
    return list_last_value

def do_math():
    delta = get_delta_seconds(channel)

print("Listening for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received message: {message['data']}")
        dc_channel = message['data'].decode().split(":")[0]
        status = message['data'].decode().split(":")[1]

        if dc_channel in energy_dict and int(status) == True:
            energy_dict[dc_channel] = True
        
        if all(energy_dict.values()):
            print("All EDC value is TRUE, time to make addition")
            energy_now = sum(get_last_data(last_parital_energy_sentence()))
            print(energy_now)

            energy_dict = {key: False for key in energy_dict}
