#!/bin/bash
echo "Starting loggers on all remote machines."
parallel-ssh -h ./phosts './scripts/resource_logger/log_sys_resource.sh >/dev/null 2>&1'
