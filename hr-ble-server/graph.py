import matplotlib.pyplot as plt
import numpy as np

heart_rate = [60]
times = [0]

timeFactor = 5

stage0 = int(0/timeFactor)
stage1 = int(40/timeFactor)
stage2 = int(300/timeFactor)
stage3 = int(450/timeFactor)
stageEnd = 500

import time

# x = np.linspace(0, 100)
#
#
# plt.style.use('dark_background')
# plt.plot(x, np.sin(x))
#
# plt.ylabel('Heart Rate (bpm)', fontsize=30)
# plt.xlabel('Game duration (secs)', fontsize=25)
# plt.title('The Scare Report', fontsize=25)
# plt.show()


def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open("test.txt","r")
    loglines = follow(logfile)
    for line in loglines:
        if not line == '\n':
            heart_rate.append(int(line))
            times.append(times[-1] + timeFactor)
            plt.clf()

            print("plotting")
            print(heart_rate)

            # plt.style.use('dark_background')

            # if (len(times) > 10):
            plt.plot(times[stage0:stage1+1], heart_rate[stage0:stage1+1], color = 'limegreen', label= 'Stage 0', linewidth=2.0)
            plt.plot(times[stage1:stage2+1], heart_rate[stage1:stage2+1], color = 'gold', label = 'Stage 1', linewidth=2.0)
            plt.plot(times[stage2:stage3+1], heart_rate[stage2:stage3+1], color = 'orange', label = 'Stage2', linewidth=2.0)
            plt.plot(times[stage3:stageEnd], heart_rate[stage3:stageEnd+1], color = 'red', label = 'Stage 3', linewidth=2.0)


            plt.ylabel('Heart Rate (bpm)', fontsize=30)
            plt.xlabel('Game duration (secs)', fontsize=25)
            plt.title('The Scare Report', fontsize=25)
            plt.legend(fontsize=18)

            # plt.setp(ax.spines.values(), linewidth=5)
            plt.draw()
            plt.pause(0.0001)
