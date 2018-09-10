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

fig = plt.figure()
ax = plt.axes()
ax.set_ylim(0,100*multiprocessing.cpu_count())
ax.set_xlim(0,200)
ax2 = ax.twinx()
ax2.set_ylim(0,psutil.virtual_memory().total / 1024/1024/1024)
ax2.set_xlim(0,200)
cpu_line, = ax.plot([],[], color="red")
mem_line, = ax2.plot([],[], color="blue")

cpu_y_list = deque([-1]*400)
mem_y_list = deque([-1]*400)
x_list = deque(np.linspace(200,0,num=400))

process = None

def init():
    cpu_line.set_data([],[])
    mem_line.set_data([],[])
    return cpu_line, mem_line


def animate(i):
    cpu_y_list.pop()
    mem_y_list.pop()
    cpu_y_list.appendleft(process.cpu_percent())
    print("{} {} ".format(process.cpu_percent(.01), process.memory_percent() * psutil.virtual_memory().total/100/1024/1024/1024) )
    mem_y_list.appendleft(process.memory_percent() * psutil.virtual_memory().total / 100/1024/1024/1024)
    cpu_line.set_data(x_list,cpu_y_list)
    mem_line.set_data(x_list,mem_y_list)
    return cpu_line, mem_line

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("\nusage: python monitor.py <pid_file>\n")
        sys.exit(1)

    pid_filename = sys.argv[1]
    while not os.path.exists(pid_filename):
        time.sleep(.1) # wait 100 milliseconds

    with open(pid_filename) as pid_file:
        pid = int(pid_file.readlines()[0])
        process = psutil.Process(pid)

        anim = animation.FuncAnimation(fig, animate, init_func=init,
            frames=200, interval=100, blit=True)


    plt.show()
