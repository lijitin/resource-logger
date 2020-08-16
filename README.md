# resource-logger
Data wrangling shell scripts that logs process resource usage over time with plots.

# required packages
Install the required packages with
```
sudo apt-get install sysstat
```
parallel-ssh and parallel-slurp are needed if you want to run the logger remotely on multiple machines
```
sudo apt-get install pssh
```

# Logging on local machine
To log local system resource usage, run
```
$ ./start_local_logger

# RUN YOUR WORKLOAD HERE

$ ./stop_local_logger
```
The script creates a directory named "resourcelogs" which contains the log files

# Logging on multiple remote machines
parallel-ssh and parallel-slurp are needed if you want to run the logger remotely on multiple machines
```
sudo apt-get install pssh
```

Modify the phost file to include your remote machines. Make sure you can passwordless-ly ssh to the machines.
```
vim ./phosts
```

Log with
```
./start_loggers.sh

# RUN YOUR WORKLOAD ON THE MACHINES

./stop_loggers.sh
```

# Plotting the logs

```
python plot_logs.py [path-to-all_resource_logs-dir] [number-of-active-hosts]
```


