from kafka import KafkaConsumer
from kafka import KafkaProducer
from backend.operation import NetScan,NetAttack,PcapSniff
# import NetScan
# import NetAttack
import time
import json
# import PcapSniff
from threading import Thread


class AttackNode():
    def __init__(self, commandTopic="command", dataTopic='data'):
        self.type = ''
        self.ipAddr = ''
        self.port = None
        self.command = ""
        self.attacktype = ""
        self.commandTopic = commandTopic
        self.dataTopic = dataTopic
        self.dataDir = ''


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
        sniff = PcapSniff.PcapSniff()
        command = self.command.strip()
        sniff.StartSniff()
        if command[0] == 's':
            ns = NetScan.NmapScan()
            self.attacktype = ns.AnalyseCommand(command)
            ns.StartScan()
            ns.PrintScan()
            self.dataDir = ns.WriteJson()
        elif command[0] == 'a':
            sa = NetAttack.ScapyAttack()
            self.attacktype = sa.AnalyseCommand(command)
        sniff.EndSniff()
        sniffname = "../Data/All" + self.attacktype + ".pcap"
        sniff.WritePcap(sniffname)
        # else:
        #     raise ValueError("Error Command!!!")


def AttackNodeTest():
    attacknode = AttackNode()
    attacknode.ConsumeCommand()


if __name__ == "__main__":
    AttackNodeTest()
