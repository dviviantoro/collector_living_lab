import os
from dotenv import load_dotenv
import subprocess
import random
import time

load_dotenv()
cwd = os.getenv('CWD')
print(cwd)


while True:
    for i in range(1, 5):
        random_volt = random.randint(45, 55)
        random_current = random.randint(2000, 5000)
        data = f"DC-{i},{float(random_volt)},{float(random_current)}"

        print(data)

        command = [
            f"{cwd}/.venv/bin/python",
            f"{cwd}/src/parse_and_write.py",
            "-d", data
        ]
        subprocess.Popen(command)
    time.sleep(10)