import os
import sys
import time
import random
import argparse
import subprocess
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.influxdb_interface import *
from modules.redis_interface import publish_redis

def parser_init():
    parser = argparse.ArgumentParser(description="Agregating face atribute interface")
    parser.add_argument(
        "-c",
        "--channel",
        help="Selected DC channel"
    )
    return parser

def get_delta_seconds(channel):
    now = datetime.now(timezone.utc)
    last_timestamp = get_last_data(channel)["time"]
    delta = now - last_timestamp
    return delta.seconds

def ask_write_influx(data):
    command = [
        f"{cwd}/.venv/bin/python",
        f"{cwd}/src/parse_and_write.py",
        "-d", data
    ]
    subprocess.Popen(command)

def last_data_sentence(channel):
    sentence = f"""from(bucket: "living_lab")
        |> range(start: -2d)
        |> filter(fn: (r) => r["_measurement"] == "dc")
        |> filter(fn: (r) => r["_field"] == "cur" or r["_field"] == "vol")
        |> filter(fn: (r) => r["channel"] == "{channel}")
        |> filter(fn: (r) => r["location"] == "smp_it_wasilah_garut")
        |> last()
    """
    return sentence

def get_last_data(channel):
    dict_last_value = {}
    tables = query_data(last_data_sentence(channel))
    for table in tables:
        for record in table.records:
            dict_last_value["time"] = record["_time"]
            if record["_field"] == "vol":
                dict_last_value["vol"] = record["_value"]
            elif record["_field"] == "cur":
                dict_last_value["cur"] = record["_value"]
    return dict_last_value

def calculate_energy(channel):
    delta = get_delta_seconds(channel)
    if delta < 15:
        last_value = get_last_data(channel)
        energy = (last_value["vol"] * last_value["cur"] * delta) / (1000 * 3600)
        ask_write_influx(f"E{channel},{energy}")
        return True
    else:
        print("DC measurement detect lost routine, will count from 0")
        return False

if __name__ == "__main__":
    random_sleep = random.randint(100, 1500)
    args = parser_init().parse_args()
    
    if calculate_energy(args.channel):
        time.sleep(random_sleep/1000)
        channel_redis = "energy_watcher"
        # publish_redis(channel_redis, f"E{args.channel}:1")