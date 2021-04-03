from socket import *
import json

class Client:
    def __init__(self, serverIp="127.0.0.1", serverPort=6666):
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.clientFd = socket(AF_INET, SOCK_STREAM)
        self.connect()

    def connect(self):
        self.clientFd.connect((self.serverIp,self.serverPort))

    def send(self,sendData):
        print("Client Send:", sendData)
        self.clientFd.send(sendData.encode("gbk"))

    def recv(self):
        recvData = self.clientFd.recv(1024)
        print("Client Recv:", recvData.decode("gbk"))
        return recvData.decode("gbk")

    def close(self):
        self.clientFd.close()

def testAttack():
    attackCommandDict = {}
    attackCommandDict["TaskType"] = "Attack"
    attackCommandDict["AttackType"] = "DDoS"
    attackCommandDict["DstIP"] = "192.168.2.211"
    attackCommandDict["DstPort"] = 80
    attackCommandDict["Intensity"] = 1
    attackCommandDict["LastTime"] = 3600
    attackCommandDict["TaskNode"] = 3
    attackCommand = json.dumps(attackCommandDict)

    scanCommandDict = {}
    scanCommandDict["TaskType"] = "Scan"
    scanCommandDict["ScanType"] = "OS"
    scanCommandDict["DstIP"] = "192.168.2.211"
    scanCommandDict["DstPort"] = 80
    scanCommand = json.dumps(scanCommandDict)

    client = Client("127.0.0.1", 6666)
    client.send(scanCommand)
    client.recv()

    client.close()

if __name__ == "__main__":
    testAttack()