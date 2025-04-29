import os
import asyncio
import aioserial
from dotenv import load_dotenv
import subprocess
load_dotenv()

cwd = os.getenv('CWD')
usb_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"]

def check_available_port():
    for port in usb_ports:
        if os.path.exists(port):
            print(f"Device {port} is available")
            return port
        
    print("No device is available, please check your USB dongle")
    return False

class App:
    async def read_serial(self, aioserial_instance: aioserial.AioSerial):
        while True:
            try:
                data: bytes = (await aioserial_instance.readline_async()).decode().strip()
            
                received_data = data.split(",")
                print(received_data)

                if len(received_data) > 1:
                    command = [
                        f"{cwd}/.venv/bin/python",
                        f"{cwd}/src/parse_and_write.py",
                        "-d", data
                    ]
                    subprocess.Popen(command)
            except Exception as e:
                print(e)

def run_energy_watcher():
    command = [
        f"{cwd}/.venv/bin/python",
        f"{cwd}/src/watch_energy.py"
    ]
    subprocess.Popen(command)
    
if __name__ == "__main__":
    run_energy_watcher()

    port = check_available_port()
    if port:
        app = App()
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(app.read_serial(aioserial.AioSerial(port=port,baudrate=115200)))
        loop.run_forever()

