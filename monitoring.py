#!/usr/bin/env python3

import psutil
import socket
import datetime as dt
import os
import sys

CPU_PROBE_INTERVAL = 1
DEVICE_PATH = "/dev/sda2"
LOG_PATH = "/var/log/affluences"
RETENTION_DAYS = 14

def get_report(cpu_probe_interval: int, device_disk_path: str):
    date = dt.datetime.now().astimezone().isoformat(timespec='seconds')
    hostname = socket.gethostname()
    cpu = psutil.cpu_percent(cpu_probe_interval)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage(device_disk_path).percent
    return (f"[{date}] {hostname} - {cpu};{ram};{disk}")


def retention_policy(folder: str):
  for filename in os.listdir(folder):
    fullpath = os.path.join(folder, filename)
    if os.stat(fullpath).st_mtime <= dt.time() - (RETENTION_DAYS * 24 * 60 * 60):
      try:
        os.remove(fullpath)
      except:
        sys.stderr.write("Could not remove :", filename)


def main():
    date = dt.datetime.now().date()
    with open(f"{LOG_PATH}/{date}", "a") as logfile:
        logfile.write(get_report(CPU_PROBE_INTERVAL, DEVICE_PATH)+ '\n')


if __name__ == "__main__":
    main()
