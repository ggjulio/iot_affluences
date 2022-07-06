#!/usr/bin/env python3

import psutil
import socket
import datetime as dt

DEVICE_PATH="/dev/sda2"

def get_report(device_disk_path: str = DEVICE_PATH):
	date=dt.datetime.now().isoformat()
	hostname=socket.gethostname()
	cpu=psutil.cpu_percent(2)
	ram=psutil.virtual_memory().percent
	disk=psutil.disk_usage(device_disk_path).percent
	return (f"[{date}] {hostname} - {cpu};{ram};{disk}")

def main():
	print(get_report('/dev/sda2'))

if __name__ == "__main__":
	main()
