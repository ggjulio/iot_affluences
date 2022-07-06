#!/usr/bin/env bash

# -e option is important, it ensure the script will exit and return a non zero value
# we could also add -o pipefail, but it is not posix, thus not supported by all shells.
set -eux

# Variables can be overridden at execution. 
# ex: $ DEVICE_DISK=/dev/sdb1 RETENTION_DAYS=7 ./monitoring.sh

# In second (man mpstat)
# Augmenting count probe and an interval higher than 1 sec can helps avoid aberrant values (especially in VMs)
MPSTAT_INTERVAL="${MPSTAT_INTERVAL-1}"
MPSTAT_COUNT="${MPSTAT_COUNT-1}"
DEVICE_DISK="${DEVICE_DISK:-sda1}"
LOG_PATH="${LOG_PATH:-/var/log/affluences/}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"

# If probe count > 1. Do the mean of datapoints, and return the cpu usage in percent
get_cpu_usage(){
	local result
	result="$(mpstat $MPSTAT_INTERVAL $MPSTAT_COUNT -o JSON \
		| jq -r '[.sysstat.hosts[0].statistics[]."cpu-load"[0].usr] | add / length' \
		| awk '{printf "%.1f", $0}')"
	echo "$result"
}

get_ram_usage(){
	echo -n "$(free | grep 'Mem:' | awk '{printf "%.1f", $3/$2*100}')"
}

get_disk_usage(){
	echo -n "$(df /dev/$DEVICE_DISK | tail -n 1 | awk '{printf "%.1f",  $3!=0?$3/($4+$3)*100:0}')"
}

get_report(){
	echo "[$(date -Iseconds)] $(hostname) - $(get_cpu_usage);$(get_ram_usage);$(get_disk_usage)"
}

# Just a simple function to remove all file created >= N days.
# Not really great because it run everytime. It could be run only once a day as a separate script.
# Or I could have used an external tool for rotation, but the retention asked is pretty simple. So I avoided fancy tools.
retention_policy(){
	find "$LOG_PATH" -mindepth 1 -mtime "+$RETENTION_DAYS" -delete
}

main(){
	local report
	mkdir -p "$LOG_PATH"
	retention_policy
	report="$(get_report)"
	echo "$report" >> "${LOG_PATH}/$(date -I)"
}

main "$@"
