#!/bin/bash

# run log_pid_resource.sh in script

echo "sorting 1g"

#.#.#.#.#.#.#.#.#.#.#.#.#.
# RUN YOUR WORKLOAD HERE
sort /hdd/data/file-1GB.txt > /hdd/data/file-1GB.txt.sorted &
#.#.#.#.#.#.#.#.#.#.#.#.#.

c_pid=$!
./log_sys_resource.sh

wait $c_pid # wait for the sorting program return

sleep 10 # << sleep for an extra 10s until we stop the logger
kill $(cat sar_pids)
rm sar_pids

echo "done."

