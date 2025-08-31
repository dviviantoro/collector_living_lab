import os
import sys
import time
import random
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.influxdb_interface import push_data
from modules.redis_interface import publish_redis
from modules.util import parse_data
from dotenv import load_dotenv
import subprocess
load_dotenv()
cwd = os.getenv('CWD')

def parser_init():
    parser = argparse.ArgumentParser(description="Agregating face atribute interface")
    parser.add_argument(
        "-d",
        "--rawdata",
        help="Transmitted raw data that want to write into influxDB"
    )
    parser.add_argument(
        "-t",
        "--timestamp",
        help="Define custom timestamp for influxDB write"
    )
    return parser

def parse_and_write(raw_data):
    dictionary = parse_data(raw_data)
    try:
        push_data(dictionary)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    args = parser_init().parse_args()
    random_sleep = random.randint(100, 3000)

    # not use anymore
    # special for DC
    # if (args.rawdata).split("-")[0] == "DC": 
    #     channel = (args.rawdata).split(",")[0]
    #     command = [
    #         f"{cwd}/.venv/bin/python",
    #         f"{cwd}/src/calculate_energy.py",
    #         "-c", channel
    #     ]
    #     subprocess.Popen(command)

    time.sleep(random_sleep/1000)
    parse_and_write(args.rawdata)
    
    # if (args.rawdata).split("-")[0] == "AC": 
    #     channel_redis = "energy_ac"
    #     channel_ac = (args.rawdata).split(",")[0]
    #     publish_redis(channel_redis, f"{channel_ac}:1")