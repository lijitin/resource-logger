#!/bin/bash

# run log_pid_resource.sh in script

echo "sorting 1g"
sort /hdd/data/file-1GB.txt > /hdd/data/file-1GB.txt.sorted &
c_pid=$!
./log_pid_resource.sh $c_pid &
logger_pid=$!

wait $c_pid

sleep 1m # wait for disk io/ operations to complete
kill $logger_pid

echo "done."

