import nmap

import json
from enum import Enum
import os


class NetScanType():
    HostScan = 's1'
    PortScan = 's2'
    VersionScan = 's3'
    OSScan = 's4'


class NmapScan:
    def __init__(self):
        self.ipAddr = ''
        self.port = ''
        self.nm = nmap.PortScanner()
        self.info = {}
        self.type = ''
        self.analyse = {}
        self.attacktype = ''

    def __CheckPort(self):
        if self.port == "":
            return 0
        else:
            return 1

    def __CheckType(self):
        if self.type == "":
            return 0
        else:
            return 1

    def __SetPort(self, port):
        self.port = port

    def __SetIPAddr(self, ipAddr):
        self.ipAddr = ipAddr

    def AddType(self, type):
        self.type += type
        self.type += ' '

    # 根据IP地址，端口号，扫描类型发起扫描（端口号和扫描类型为可选项，所以需要判断是否有输入）
    def StartScan(self):
        if self.__CheckPort() == 0 and self.__CheckType() == 0:
            self.info = self.nm.scan(self.ipAddr).copy()
        elif self.__CheckPort() == 1 and self.__CheckType() == 0:
            self.info = self.nm.scan(self.ipAddr, self.port).copy()
        elif self.__CheckPort() == 0 and self.__CheckType() == 1:
            self.info = self.nm.scan(self.ipAddr, arguments=self.type).copy()
        elif self.__CheckPort() == 1 and self.__CheckType() == 1:
            self.info = self.nm.scan(self.ipAddr, self.port, self.type).copy()
        else:
            raise ValueError("Port not set!!")

    # 解析指令，根据s1-s4区分不同的指令，给nmap端发送不同的类型指令
    def AnalyseCommand(self, command):
        # 指令的拆分解析
        listcommand = command.split(' ')
        if len(listcommand) == 0:
            raise ValueError("Empty command!!!")
        elif len(listcommand) == 1:
            raise ValueError("IP not set!!!")
        else:
            type = listcommand[0]
            ip = listcommand[1]
        port = ''
        netattacktype = NetScanType()
        self.type = ''
        if len(listcommand) == 3:
            port = listcommand[2]
        if (type == netattacktype.HostScan):
            self.ipAddr = ip
            self.AddType("-sn")
            self.attacktype = "HostScan"
        elif (type == netattacktype.PortScan):
            self.ipAddr = ip
            self.AddType("-sS")
            self.AddType("-sU")
            self.attacktype = "PortScan"
            if (port == ''):
                self.AddType("-F")
            else:
                self.port = port
        elif (type == netattacktype.VersionScan):
            self.ipAddr = ip
            self.AddType("-sV")
            self.attacktype = "VersionScan"
            if (port != ''):
                self.port = port
        elif (type == netattacktype.OSScan):
            self.ipAddr = ip
            self.AddType("-O")
            self.attacktype = "OSScan"
            if (port != ''):
                self.port = port
        else:
            raise ValueError("Unknown instruction!!!")

        return self.attacktype

    def ManualSet(self):
        self.AddType('-O')
        self.AddType('-F')
        self.__SetPort('')
        self.__SetIPAddr("192.168.1.203")
        self.StartScan()

    def AnalyseScanInfo(self):
        self.analyse['scan'] = self.info["scan"]
        print(json.dumps(self.analyse, indent=4, ensure_ascii=False))

    def PrintScan(self):
        print(json.dumps(self.info, indent=4, ensure_ascii=False))

    def WriteJson(self):
        jsonName = "../Data/" + self.attacktype + "_1"
        jsonName += ".json"
        order = 1
        while (os.path.isfile(jsonName)):
            jsonName = jsonName.split('_')[0]
            order += 1
            jsonName += '_' + str(order)
            jsonName += ".json"
        with open(jsonName, "w") as f:
            json.dump(self.info, f, indent=4)
            print("Write Json Success!")
        return jsonName


def NmapScanTest():
    ns = NmapScan()
    ns.AnalyseCommand("s2 192.168.2.1")
    ns.StartScan()
    ns.PrintScan()
    ns.WriteJson()


if __name__ == "__main__":
    NmapScanTest()
