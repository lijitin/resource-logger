#!/bin/bash
echo "Stopping loggers on all the pis."
parallel-ssh -h phosts 'killall -9 sar'

# slurp all logs back to here
parallel-slurp -r -h phosts -L ./all_resource_logs /home/ubuntu/resourcelogs .

echo "All resource logs slurped. (located in /exports/all_resource_logs)"
