#!/bin/bash

## run logger interactively with screen:
# screen -S reslogger ./log_resource.sh [command_pid]

## or in a shell/script, call by
# ./log_resource.sh [command_pid] &
# logger_pid=$!
## wait for the command to return
# wait $[command_pid]

c_pid=$1

echo "Starting resource logger. "
# log the cpu, memory and io to 3 separate files
mkdir resourcelogs
CPU_LOG_FILE="resourcelogs/cpu.log"
MEM_LOG_FILE="resourcelogs/mem.log"
DISK_LOG_FILE="resourcelogs/disk.log"

headline=$(pidstat | sed -n "1,+p")
for filename in $CPU_LOG_FILE $MEM_LOG_FILE $DISK_LOG_FILE
do
	echo $headline >> $filename
done
# headers
echo "Time          UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Commandi" >> $CPU_LOG_FILE
echo "Time          UID       PID  minflt/s  majflt/s     VSZ     RSS   %MEM  Command" >> $MEM_LOG_FILE
echo "Time          UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command" >> $DISK_LOG_FILE


while true
do
	pidstat -u -p $c_pid | sed -n "4,+p" >> $CPU_LOG_FILE	
	pidstat -r -p $c_pid | sed -n "4,+p" >> $MEM_LOG_FILE
	pidstat -d -p $c_pid | sed -n "4,+p" >> $DISK_LOG_FILE
	sleep 5
done

