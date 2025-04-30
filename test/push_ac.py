import os
from dotenv import load_dotenv
import subprocess
import random
import time

load_dotenv()
cwd = os.getenv('CWD')

sum_energy0 = []
sum_energy1 = []
sum_energy2 = []
sum_energy3 = []
sum_energy4 = []
sum_energy5 = []
sum_energy6 = []

sum_energy = [sum_energy0, sum_energy1, sum_energy2, sum_energy3, sum_energy4, sum_energy5, sum_energy6]

while True:
    for i in range(1, 7):
        # time.sleep(200/1000)
        random_vol = random.uniform(210, 230)
        random_cur = random.uniform(1, 10)
        random_pow = random_vol * random_cur
        random_engy = (random_pow * 10) / (1000 * 3600)
        random_freq = random.uniform(48, 51)
        random_pf = random.uniform(0, 1)
        
        sum_energy[i].append(random_engy)
        energy = sum(sum_energy[i])

        data = f"AC-{i},"
        data += f"{float(random_vol)},"
        data += f"{float(random_cur)},"
        data += f"{float(random_pow)},"
        data += f"{energy},"
        data += f"{float(random_freq)},"
        data += f"{float(random_pf)}"

        print(data)

        command = [
            f"{cwd}/.venv/bin/python",
            f"{cwd}/src/parse_and_write.py",
            "-d", data
        ]
        subprocess.Popen(command)
    time.sleep(10)