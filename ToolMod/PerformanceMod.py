import psutil
import os
import time

class Performance():
    def __init__(self):
        pass

    def GetCPU(self):
        cpu = psutil.cpu_percent(interval=1.0)
        # print("CPU:", cpu)
        return cpu

    def GetMemory(self):
        memory = psutil.virtual_memory().percent
        # print("Memory:", memory)
        return memory

    def GetTime(self):
        nowTime = time.strftime("%H:%M:%S", time.localtime())
        # print("NowTime:", nowTime)
        return nowTime
    def GetIP(self):
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                if item[0] == 2 and item[1][0:10] == '192.168.2.':
                    # print("Current IP:",item[1])
                    return item[1]


if __name__ == "__main__":
    performance = Performance()
    performance.GetCPU()
    performance.GetMemory()
    performance.GetTime()
    performance.GetIP()