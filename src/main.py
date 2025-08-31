import os
import asyncio
import aioserial
from dotenv import load_dotenv
import subprocess
load_dotenv()

cwd = os.getenv('CWD')
usb_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"]

def check_available_port():
    available_ports = []
    for port in usb_ports:
        if os.path.exists(port):
            print(f"Device {port} is available")
            available_ports.append(port)
    
    print(available_ports)
    return available_ports


class App:
    async def read_serial(self, aioserial_instance: aioserial.AioSerial):
        last_device_id = ""
        while True:
            try:
                data: bytes = (await aioserial_instance.readline_async()).decode().strip()
                received_data = data.split(",")
                print(f"received_data now: {received_data}")

                current_device_id = received_data[0]
                device = current_device_id.split("-")[0]

                if current_device_id != last_device_id and device != "DC":
                    if len(received_data) > 1:
                        command = [
                            f"{cwd}/.venv/bin/python",
                            f"{cwd}/src/parse_and_write.py",
                            "-d", data
                        ]
                        subprocess.Popen(command)
                last_device_id = current_device_id
            except Exception as e:
                print(e)

def run_energy_watcher():
    command = [
        f"{cwd}/.venv/bin/python",
        f"{cwd}/src/watch_energy.py"
    ]
    subprocess.Popen(command)

def run_ac_energy_watcher():
    command = [
        f"{cwd}/.venv/bin/python",
        f"{cwd}/src/do_math_energy.py"
    ]
    subprocess.Popen(command)

def run_dummy_dc():
    command = [
        f"{cwd}/.venv/bin/python",
        f"{cwd}/test/push_dc.py"
    ]
    subprocess.Popen(command)

def run_dummy_ac():
    command = [
        f"{cwd}/.venv/bin/python",
        f"{cwd}/test/push_ac.py"
    ]
    subprocess.Popen(command)
    
async def main():
    available_ports = check_available_port()
    if available_ports:
        tasks = []
        for port in available_ports:
            app = App()
            serial_instance = aioserial.AioSerial(port=port, baudrate=115200)
            tasks.append(app.read_serial(serial_instance))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    run_ac_energy_watcher()
    # run_dummy_ac()
    # run_dummy_dc()
    asyncio.run(main())


    """
    port = check_available_port()
    if port:
        app = App()
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(app.read_serial(aioserial.AioSerial(port=port[0], baudrate=115200)))
        loop.run_forever()
    """
