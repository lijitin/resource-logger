# README.TXT for resource_logger
# Create system resource usage log files.
# sar is required. install with sudo apt sysstat

# to run the logger locally, do
./resource_logger
# and stop with
kill $(cat sar_pid)

# to run loggers remotely, needs parallel-ssh and parallel-slurp
# prepare a phost file with the remote machine hostnames. Make sure you can ssh to the machines.
./start_loggers.sh
# run your tests/benchmarks, and then stop the logger with
./stop_loggers.sh

# the log files will be ssh-copied to this local machine.
# in /exports/all_resource_logs

# plotting tool is included. Requires python, matplotlib, pandas

# then run
python plot_logs.py [path-to-all_resource_logs-dir] [number-of-active-hosts]
# e.g. python plot_logs ~/all_resource_logs 4 # for experiment ran with only 4 machiens.

# -- Let me know if anything goes wrong when running these scripts. ~justin Apr 23rd 2020
