import matplotlib.pyplot as plt

heart_rate = [60]
times = [0]

import time
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
            times.append(times[-1] + 1)
            plt.clf()
            print("plotting")
            print(heart_rate)
            plt.plot(times, heart_rate)
            plt.draw()
            plt.pause(0.0001)

