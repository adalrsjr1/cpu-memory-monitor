import os
import sys
import psutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
import time
from collections import deque
import multiprocessing

def init():
    cpu_line.set_data([],[])
    mem_line.set_data([],[])
    return cpu_line, mem_line

def toKilo(size_bytes):
    return size_bytes / 1024

def toMega(size_bytes):
    return toKilo(size_bytes) / 1024

def toGiga(size_bytes):
    return toMega(size_bytes) / 1024

def change_base(notation, size_bytes):
    """
        convert memory in bytes to:
            kilo == k or K
            mega == m or M
            giga == g or G
    """
    if "k" == notation or "K" == notation:
        return toKilo(size_bytes)
    if "m" == notation or "M" == notation:
        return toMega(size_bytes)
    if "g" == notation or "G" == notation:
        return toGiga(size_bytes)
    return size_bytes

def animate(i):
    cpu_y_list.pop()
    mem_y_list.pop()

    cpu_percent = process.cpu_percent(.01)
    mem_percent = process.memory_percent()
    total_mem = psutil.virtual_memory().total

    mem_used = change_base(memory_base, mem_percent * total_mem) / 100

    cpu_y_list.appendleft(cpu_percent)
    mem_y_list.appendleft(mem_used)

    print("{} {} ".format(cpu_percent, mem_used) )

    cpu_line.set_data(x_list,cpu_y_list)
    mem_line.set_data(x_list,mem_y_list)

    return cpu_line, mem_line

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("\nusage: python monitor.py <memory_notation B K M G> <pid_file>\n")
        sys.exit(1)

    memory_base = sys.argv[1]
    pid_filename = sys.argv[2]

    fig = plt.figure()

    ax = plt.axes()
    ax.set_ylim(0,100 * multiprocessing.cpu_count())
    ax.set_xlim(0,60)
    ax.set_xlabel('last 60 seconds')
    ax.set_ylabel('CPU (%)', color='red')

    ax2 = ax.twinx() # copy of plot area
    ax2.set_ylim(0,change_base(memory_base, psutil.virtual_memory().total)/1000)
    ax2.set_xlim(0,60)

    ax2.set_ylabel('Memory ({}B)'.format('' if memory_base == 'b' or memory_base == 'B' else memory_base), color='blue')

    cpu_line, = ax.plot([],[], color="red")
    mem_line, = ax2.plot([],[], color="blue")

    time_window = 450

    cpu_y_list = deque([-1]*time_window)
    mem_y_list = deque([-1]*time_window)
    x_list = deque(np.linspace(0,60,num=time_window)) # dynamic x-axis

    process = None

    while not os.path.exists(pid_filename):
        time.sleep(.1) # wait 100 milliseconds

    with open(pid_filename) as pid_file:
        pid = int(pid_file.readlines()[0])
        process = psutil.Process(pid)

        anim = animation.FuncAnimation(fig, animate, init_func=init,
            frames=200, interval=100, blit=True)

    plt.show()
