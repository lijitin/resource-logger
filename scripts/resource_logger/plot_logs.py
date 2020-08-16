#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:05:51 2020

@author: justin
"""

# given a specific resource log directory, and number of active host, generate plot

import argparse
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

def parse_log(filepath):
    df = pd.read_csv(filepath, sep='\s+', skiprows=2)
    df = df.rename(columns={df.columns[0]:"timestamp"})
    return df

def plot_logs(dirpath, nhosts):
    logtypes = ["cpu.log", "mem.log", "disk.log"]
    cpu_dfs = []
    mem_dfs = []
    disk_dfs = []
    for hostid in range(1, nhosts+1):
        for logtype in logtypes:
            filepath = os.path.join(dirpath, "pi"+str(hostid), "resourcelogs", logtype)
            if not os.path.exists(filepath):
                sys.exit("File does not exist - filepath=\"" + filepath + "\"")
            df = parse_log(filepath)
            if logtype == logtypes[0]: # cpu log
                cpu_dfs.append(df)
            elif logtype == logtypes[1]: # mem log
                mem_dfs.append(df)
            elif logtype == logtypes[2]: # disk log
                disk_dfs.append(df)
            else:
                sys.exit("Invalid logtype.")

    # create a new df and calculate the average statistics.
    df_plot = pd.DataFrame(cpu_dfs[0]['timestamp'])
    # calculate the average cpu usage from all the hosts
    df_plot['average_cpu_%used'] = cpu_dfs[0]['%idle']
    for cpu_df in cpu_dfs[1:]:
        df_plot['average_cpu_%used'] = df_plot['average_cpu_%used'] + cpu_df['%idle']
    df_plot['average_cpu_%used'] = (df_plot['average_cpu_%used']/nhosts - 100)*-1
    
    # average mem usage
    df_plot['average_mem_%used'] = mem_dfs[0]['%memused']
    for mem_df in mem_dfs[1:]:
        df_plot['average_mem_%used'] = df_plot['average_mem_%used'] + mem_df['%memused']
    df_plot['average_mem_%used'] = df_plot['average_mem_%used']/nhosts
    # disk usage, bread/s and bwrtn/s
    df_plot['average_bread/s'] = disk_dfs[0]['bread/s']
    df_plot['average_bwrtn/s'] = disk_dfs[0]['bwrtn/s']
    for disk_df in disk_dfs[1:]:
        df_plot['average_bread/s'] = df_plot['average_bread/s'] + disk_df['bread/s']
        df_plot['average_bwrtn/s'] = df_plot['average_bwrtn/s'] + disk_df['bwrtn/s']
    df_plot['average_bread/s'] = df_plot['average_bread/s']/nhosts
    df_plot['average_bwrtn/s'] = df_plot['average_bwrtn/s']/nhosts
    # plot and save the figs
    fig, ax = plt.subplots()
    cpumem = ax.twinx()
    diskrw = ax.twinx()
    # PLOT DATA #
    cpu_line, = cpumem.plot(df_plot['timestamp'], df_plot['average_cpu_%used'], "g-", label="CPU")
    mem_line, = cpumem.plot(df_plot['timestamp'], df_plot['average_mem_%used'], "y-", label="MEM")
    disk_r_line, = diskrw.plot(df_plot['timestamp'], df_plot['average_bread/s'], "r-", label="AVG_READ")
    disk_w_line, = diskrw.plot(df_plot['timestamp'], df_plot['average_bwrtn/s'], "b-", label="AVG_WRITE")
    
    # LABELS #
    ax.set_xlabel("timestamps hr:m:s")
    cpumem.set_ylabel("%")
    diskrw.set_ylabel('bytes/s')
    
    # AXES #
    cpumem.set_ylim(0,100) # percentage 0-100
    # diskrw.set_ylim(0,???) # set a hard range
    # x tick freqency
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    ax.set_xticklabels(df_plot['timestamp'], rotation=40) # rotate xtick labels
    # y-axis positions
    ax.get_yaxis().set_visible(False) # set invisible
    cpumem.yaxis.tick_left()
    cpumem.yaxis.set_label_position("left")
    diskrw.yaxis.tick_right()
    # diskrw.spines["right"].set_position(("axes", 1.2)) # move spine to more right
    
    lines = [cpu_line, mem_line, disk_r_line, disk_w_line]
    ax.legend(lines, [l.get_label() for l in lines])
    
    ax.set_title("CPU, memory and disk usage plot", pad=10)
    plt.subplots_adjust(bottom=0.25)
    
    plt.savefig("resource_plot_n:" + str(nhosts)+".png")
    return
      
'''
nhosts = 1

cpu_dfs, mem_dfs, disk_dfs = plot_logs("/home/justin/sp/pi/all_resource_logs", nhosts)      

df_plot = pd.DataFrame(cpu_dfs[0]['timestamp'])
# calculate the average cpu usage from all the hosts
df_plot[''average_cpu_%used'] = cpu_dfs[0]['%idle']
for cpu_df in cpu_dfs[1:]:
    df_plot['average_cpu_%used'] = df_plot['average_cpu_%used'] + cpu_df['%idle']
df_plot['average_cpu_%used'] = (df_plot['average_cpu_%used']/nhosts - 100)*-1

# average mem usage
df_plot['average_mem_%used'] = mem_dfs[0]['%memused']
for mem_df in mem_dfs[1:]:
    df_plot['average_mem_%used'] = df_plot['average_mem_%used'] + mem_df['%memused']
df_plot['average_mem_%used'] = df_plot['average_mem_%used']/nhosts
# disk usage, bread/s and bwrtn/s
df_plot['average_bread/s'] = disk_dfs[0]['bread/s']
df_plot['average_bwrtn/s'] = disk_dfs[0]['bwrtn/s']
for disk_df in disk_dfs[1:]:
    df_plot['average_bread/s'] = df_plot['average_bread/s'] + disk_df['bread/s']
    df_plot['average_bwrtn/s'] = df_plot['average_bwrtn/s'] + disk_df['bwrtn/s']
df_plot['average_bread/s'] = df_plot['average_bread/s']/nhosts
df_plot['average_bwrtn/s'] = df_plot['average_bwrtn/s']/nhosts

fig, ax = plt.subplots()
cpumem = ax.twinx()
diskrw = ax.twinx()
# PLOT DATA #
cpu_line, = cpumem.plot(df_plot['timestamp'], df_plot['average_cpu_%used'], "g-", label="CPU")
mem_line, = cpumem.plot(df_plot['timestamp'], df_plot['average_mem_%used'], "y-", label="MEM")
disk_r_line, = diskrw.plot(df_plot['timestamp'], df_plot['average_bread/s'], "r-", label="AVG_READ")
disk_w_line, = diskrw.plot(df_plot['timestamp'], df_plot['average_bwrtn/s'], "b-", label="AVG_WRITE")

# LABELS #
ax.set_xlabel("timestamps hr:m:s")
cpumem.set_ylabel("%")
diskrw.set_ylabel('bytes/s')

# AXES #
cpumem.set_ylim(0,100) # percentage 0-100
# diskrw.set_ylim(0,???) # set a hard range
# x tick freqency
ax.xaxis.set_major_locator(plt.MaxNLocator(4))
ax.set_xticklabels(df_plot['timestamp'], rotation=40) # rotate xtick labels
# y-axis positions
ax.get_yaxis().set_visible(False) # set invisible
cpumem.yaxis.tick_left()
cpumem.yaxis.set_label_position("left")
diskrw.yaxis.tick_right()
# diskrw.spines["right"].set_position(("axes", 1.2)) # move spine to more right

lines = [cpu_line, mem_line, disk_r_line, disk_w_line]
ax.legend(lines, [l.get_label() for l in lines])

ax.set_title("CPU, memory and disk usage plot", pad=10)
plt.subplots_adjust(top=0.6)

'''




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate plots of the given log files')
    parser.add_argument('dirpath', metavar='i', type=str, 
                    help='path to the all_resource_logs directory')
    parser.add_argument('nhosts', metavar='n', type=int,
                    help='number of active hosts')
    args = parser.parse_args()
    
    plot_logs(args.dirpath, args.nhosts)
    print('Done.')
    