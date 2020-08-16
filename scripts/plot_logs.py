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
from matplotlib.dates import AutoDateLocator, DateFormatter
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

    # plot the single namenode
    nn_df_plot = pd.DataFrame(cpu_dfs[0]['timestamp'])
    nn_df_plot['average_cpu_%used'] = (cpu_dfs[0]['%idle'] - 100)*-1
    nn_df_plot['average_mem_%used'] = mem_dfs[0]['%memused']
    nn_df_plot['average_bread/s'] = disk_dfs[0]['bread/s']
    nn_df_plot['average_bwrtn/s'] = disk_dfs[0]['bwrtn/s']
    
    # Calculate the average statistics for the remaining datanodes
    df_plot = pd.DataFrame(cpu_dfs[0]['timestamp'])
    # calculate the average cpu usage from all the hosts
    df_plot['average_cpu_%used'] = cpu_dfs[1]['%idle']
    for cpu_df in cpu_dfs[2:]:
        df_plot['average_cpu_%used'] = df_plot['average_cpu_%used'] + cpu_df['%idle']
    df_plot['average_cpu_%used'] = (df_plot['average_cpu_%used']/nhosts - 100)*-1
    
    # average mem usage
    df_plot['average_mem_%used'] = mem_dfs[1]['%memused']
    for mem_df in mem_dfs[2:]:
        df_plot['average_mem_%used'] = df_plot['average_mem_%used'] + mem_df['%memused']
    df_plot['average_mem_%used'] = df_plot['average_mem_%used']/nhosts
    # disk usage, bread/s and bwrtn/s
    df_plot['average_bread/s'] = disk_dfs[1]['bread/s']
    df_plot['average_bwrtn/s'] = disk_dfs[1]['bwrtn/s']
    for disk_df in disk_dfs[2:]:
        df_plot['average_bread/s'] = df_plot['average_bread/s'] + disk_df['bread/s']
        df_plot['average_bwrtn/s'] = df_plot['average_bwrtn/s'] + disk_df['bwrtn/s']
    df_plot['average_bread/s'] = df_plot['average_bread/s']/nhosts
    df_plot['average_bwrtn/s'] = df_plot['average_bwrtn/s']/nhosts
    
    if not os.path.exists('resourcelog_plots'):
        os.makedirs('resourcelog_plots')
    
    # convert to datetime datatype
    # nn_df_plot.timestamp = pd.to_datetime(nn_df_plot.timestamp)
    # df_plot.timestamp = pd.to_datetime(df_plot.timestamp)
    
    plot_df(nn_df_plot, os.path.join('resourcelog_plots', 'resource_plot_namenode_n'+str(nhosts)+'.png'))
    plot_df(df_plot, os.path.join('resourcelog_plots', 'resource_plot_datanode_n'+str(nhosts)+'.png'))
    
    return
      

def plot_df(df_plot, filename):
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
    num_times = df_plot.timestamp.size
    numticks = 5
    xtick_labels = []
    skip_factor = num_times//numticks
    for i in range(numticks):
        xtick_labels.append(df_plot.timestamp[i*skip_factor])
    ax.set_xticklabels(xtick_labels, rotation=40)
    from matplotlib.ticker import LinearLocator
    ax.xaxis.set_major_locator(LinearLocator(numticks=numticks))
    # ax.set_xticklabels(df_plot['timestamp'], rotation=40) # rotate xtick labels
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
    
    fig.set_size_inches(8, 5)
    
    plt.savefig(filename)
    return
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate plots of the given log files')
    parser.add_argument('dirpath', metavar='i', type=str, 
                    help='path to the all_resource_logs directory')
    parser.add_argument('nhosts', metavar='n', type=int,
                    help='number of active hosts')
    args = parser.parse_args()
    
    plot_logs(args.dirpath, args.nhosts)
    print('Done.')
    