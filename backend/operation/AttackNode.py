# from kafka import KafkaConsumer
# from kafka import KafkaProducer
from backend.operation import NetScan, NetAttack, PcapSniff
from backend.operation.TrafficSimulation import ResolveModule
# import NetScan
# import NetAttack
import time
import json
# import PcapSniff
from threading import Thread
from backend.handler import DB_OP


class AttackNode():
    def __init__(self, AttackParam):
        self.type = AttackParam["type"][0]
        self.ipAddr = AttackParam["ip"]
        self.port = AttackParam["port"]
        # self.command = command
        self.attacktype = AttackParam["type"]
        # self.commandTopic = commandTopic
        # self.dataTopic = dataTopic
        # self.dataDir = ''
        self.intensity = AttackParam["intensity"]
        self.lasttime = AttackParam["lasttime"]
        self.AttackParam = AttackParam

    def ConsumeCommand(self):
        consumer = KafkaConsumer(self.commandTopic, bootstrap_servers=['localhost:9092'])
        while True:
            msg = consumer.poll(timeout_ms=10, max_records=1)
            for key in msg:
                self.command = str(msg[key][0].value, encoding="utf-8")
                print(self.command)
                self.AnalyzeCommand()
                self.thread = Thread(target=self.ProduceData)
                self.thread.start()
                self.thread.join()
            time.sleep(2)

    def ProduceData(self):
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        try:
            if self.dataDir == '':
                raise ValueError("No data!!!")

            f = open(self.dataDir)
            data = json.load(f)
            print(data)
            f.close()
            future = producer.send(self.dataTopic, key=b'data', value=bytes(str(data), encoding="utf-8"),
                                   partition=0)
            result = future.get(timeout=10)
            print(result)
        except:
            pass

    # 集中的指令解析函数，解析后再调用两个不同的函数
    def AnalyzeCommand(self):
        # sniff = PcapSniff.PcapSniff()
        # command = self.command.strip()
        # sniff.StartSniff()
        if self.type == 's':
            ns = NetScan.NmapScan()
            self.attacktype = ns.AnalyseCommand(self.AttackParam)
            ns.StartScan()
            # ns.PrintScan()
            # self.dataDir = ns.WriteJson()
            return ns.info
        elif self.type == 'a':
            sa = NetAttack.ScapyAttack()
            self.attacktype = sa.AnalyseCommand(self.AttackParam)
        elif self.type == "T":
            DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "traffic simulation", "success", "none")
            # conlist = command.split(" ")
            TClass = self.attacktype
            TDic = {
                "T1": "C:\PD\Project\CyberAttackPlatform/backend/operation/TrafficSimulation/snort-script/trojan-activity115.json",
                "T2": "C:\PD\Project\CyberAttackPlatform/backend/operation/TrafficSimulation/snort-script/web-application-attack509.json",
                "T3": "C:\PD\Project\CyberAttackPlatform/backend/operation/TrafficSimulation/snort-script/shellcode-detect1327.json",
            }
            fp = open(TDic[TClass], "r")
            pkt_param = json.load(fp)
            task = {
                "LastTime": 10,
                "Count":1
            }
            if self.lasttime:
                task["LastTime"] = int(self.lasttime)
            if self.intensity:
                task["Count"] = int(self.intensity)
            TSa = ResolveModule.ResolveScript(pkt_param, task, dst=self.ipAddr)
            return TSa.SendPacket()
        return True
        # sniff.EndSniff()
        # sniffname = "../Data/All" + self.attacktype + ".pcap"
        # sniff.WritePcap(sniffname)
        # else:
        #     raise ValueError("Error Command!!!")


def AttackNodeTest():
    attacknode = AttackNode()
    attacknode.ConsumeCommand()


if __name__ == "__main__":
    AttackNodeTest()
