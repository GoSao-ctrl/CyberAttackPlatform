import nmap

import json
from enum import Enum
import os
from backend.handler import DB_OP

class NetScanType():
    HostScan = 's1'
    PortScan = 's2'
    VersionScan = 's3'
    OSScan = 's4'
    VulScan = 's5'


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

    # handle vul data
    def HandleVulData(self):
        if self.attacktype == "VulScan":
            scan_data = self.info["scan"]
            res = {"attacktype": self.attacktype}
            res["vul_data"] = []
            for ip in scan_data.keys():
                ip_data = scan_data[ip]

            if "tcp" in ip_data:
                tcp_data = ip_data["tcp"]
                for port in tcp_data.keys():
                    port_data = tcp_data[port]
                    if "script" not in port_data:
                        continue
                    if "vulners" not in port_data["script"]:
                        continue
                    vul_data = port_data["script"]["vulners"]
                    vul_list = vul_data.split("\n")
                    for i in range(2, len(vul_list)):
                        cve_list = vul_list[i].split("\t")
                        if len(cve_list) == 5:
                            res["vul_data"].append([port, cve_list[1], cve_list[2], cve_list[3], cve_list[4]])
                        elif len(cve_list) == 4:
                            res["vul_data"].append([port, cve_list[1], cve_list[2], cve_list[3]])

            if "udp" in ip_data:
                tcp_data = ip_data["udp"]
                for port in tcp_data.keys():
                    port_data = tcp_data[port]
                    if "script" not in port_data:
                        continue
                    vul_data = port_data["script"]["vulners"]
                    vul_list = vul_data.split("\n")
                    cve_list = vul_list[i].split("\t")
                    if len(cve_list) == 5:
                        res["vul_data"].append([port, cve_list[1], cve_list[2], cve_list[3], cve_list[4]])
                    elif len(cve_list) == 4:
                        res["vul_data"].append([port, cve_list[1], cve_list[2], cve_list[3]])
            self.info = res

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
        self.HandleVulData()

    # 解析指令，根据s1-s4区分不同的指令，给nmap端发送不同的类型指令
    def AnalyseCommand(self, AttackParam):
        # 指令的拆分解析
        # listcommand = command.split(' ')
        ipAddr = AttackParam["ip"]
        port = AttackParam["port"]
        # self.command = command
        type = AttackParam["type"]
        # self.commandTopic = commandTopic
        # self.dataTopic = dataTopic
        # self.dataDir = ''
        intensity = AttackParam["intensity"]
        lasttime = AttackParam["lasttime"]
        if type == "":
            raise ValueError("Empty command!!!")
        elif ipAddr == "":
            raise ValueError("IP not set!!!")

        netattacktype = NetScanType()

        if (type == netattacktype.HostScan):
            self.ipAddr = ipAddr
            self.AddType("-sn")
            self.attacktype = "HostScan"
            DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "start HostScan", "success", "none")
        elif (type == netattacktype.PortScan):
            self.ipAddr = ipAddr
            self.AddType("-sS")
            self.AddType("-sU")
            self.attacktype = "PortScan"
            if (port == ''):
                self.AddType("-F")
            else:
                self.port = port
            DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "start PortScan", "success", "none")
        elif (type == netattacktype.VersionScan):
            self.ipAddr = ipAddr
            self.AddType("-sV")
            self.attacktype = "VersionScan"
            if (port != ''):
                self.port = port
            DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "start VersionScan", "success", "none")
        elif (type == netattacktype.OSScan):
            self.ipAddr = ipAddr
            self.AddType("-O")
            self.attacktype = "OSScan"
            if (port != ''):
                self.port = port
            DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "start OSScan", "success", "none")
        elif (type == netattacktype.VulScan):
            self.ipAddr = ipAddr
            self.AddType("-sV")
            self.attacktype = "VulScan"
            self.AddType("--script vulners")
            if (port != ''):
                self.port = port
            DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "start VulScan", "success", "none")
        else:
            DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "start scan", "fail", "Unknown instruction")
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
    ns.AnalyseCommand("s5 192.168.2.169")
    ns.StartScan()
    ns.PrintScan()
    # ns.WriteJson()


if __name__ == "__main__":
    NmapScanTest()
