#!/bin/bash

## To start logging the system resource usage, run 
# ./log_resource.sh
## stop the logger with
# kill $(cat sar_pid)

# log the cpu, memory and io to 3 separate files
mkdir resourcelogs
CPU_LOG_FILE="resourcelogs/cpu.log"
MEM_LOG_FILE="resourcelogs/mem.log"
DISK_LOG_FILE="resourcelogs/disk.log"

# use sar
sar -u 5 > $CPU_LOG_FILE & disown
sar_cpu_pid=$!
sar -r 5 > $MEM_LOG_FILE & disown
sar_mem_pid=$!
sar -b 5 > $DISK_LOG_FILE & disown
sar_disk_pid=$!
exit
