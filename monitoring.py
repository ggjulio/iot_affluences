#!/usr/bin/env python3

import psutil
import socket
import datetime as dt

CPU_PROBE_INTERVAL=1
DEVICE_PATH="/dev/sda1"

def get_report(cpu_probe_interval: int, device_disk_path: str):
	date=dt.datetime.now().astimezone().isoformat(timespec='seconds')
	hostname=socket.gethostname()
	cpu=psutil.cpu_percent(1)
	ram=psutil.virtual_memory().percent
	disk=psutil.disk_usage('/dev/sda1').percent
	return (f"[{date}] {hostname} - {cpu};{ram};{disk}")

def main():
	print(get_report(CPU_PROBE_INTERVAL, DEVICE_PATH))

if __name__ == "__main__":
	main()
