import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
load_dotenv()

cwd = os.getenv('CWD')
url = os.getenv("INFLUX_URL")
org = os.getenv("INFLUX_ORG")
bucket = os.getenv("INFLUX_BUCKET")
location = os.getenv("DEVICE_LOCATION")
token = os.getenv("INFLUX_TOKEN")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def query_data(sentence):
    try:
        return query_api.query(query=sentence, org=org)
    except Exception as e:
        print(e)
        return False

def push_data(dictionary):
    try:
        write_api.write(bucket=bucket, org=org, record=dictionary)
        print(f"Success write: {dictionary}")
    except Exception as e:
        print(e)