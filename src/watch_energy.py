import os
import sys
import argparse
import subprocess
import redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

print("Listening for messages...")
for message in pubsub.listen():

    if message['type'] == 'message':
        print(f"Received message: {message['data']}")
        dc_channel = message['data'].decode().split(":")[0]
        status = message['data'].decode().split(":")[1]

        if dc_channel in energy_dict and int(status) == True:
            energy_dict[dc_channel] = True
        
        if all(energy_dict.values()):
            print("all value is true")
            energy_dict = {key: False for key in energy_dict}
