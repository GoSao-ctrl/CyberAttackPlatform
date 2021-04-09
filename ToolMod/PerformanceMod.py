#-*- coding:utf-8 –*-
import psutil
import os
import time
import datetime

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
        now = datetime.datetime.now()
        nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
        # print("NowTime:", nowTime)
        return nowTime

    def GetIP(self):
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                #根据192.168.2.这个前缀进行的IP筛选，如果更换网段，则需要进行修改
                if item[0] == 2 and item[1][0:10] == '192.168.2.':
                    # print("Current IP:",item[1])
                    return item[1]


def test():
    performance = Performance()
    performance.GetCPU()
    performance.GetMemory()
    performance.GetTime()
    performance.GetIP()

if __name__ == "__main__":
    test()