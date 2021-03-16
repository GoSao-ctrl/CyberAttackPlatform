from kafka import KafkaConsumer
from kafka import KafkaProducer
import json

class ControlNode():
    def __init__(self, commandTopic='command', dataTopic='data'):
        self.type = ''
        self.ipAddr = ''
        self.port = None
        self.command = ''
        self.data =''
        self.commandTopic = commandTopic
        self.dataTopic = dataTopic

    def GenCommand(self, type, ipAddr, port=None):
        self.type = type
        self.ipAddr = ipAddr
        self.port = port
        if port != None:
            self.command = str(type) + " " + str(ipAddr) + " " + str(port)
        else:
            self.command = str(type) + " " + str(ipAddr)
        print(self.command)

    def ProduceCommand(self):
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        if (self.command == ''):
            raise ValueError("No command!!!")
        future = producer.send(self.commandTopic, key=b'command', value=bytes(self.command, encoding="utf-8"), partition=0)
        result = future.get(timeout=10)
        print(result)

    def ConsumeData(self):
        consumer = KafkaConsumer(self.dataTopic,bootstrap_servers=['localhost:9092'])
        while True:
            msg = consumer.poll(timeout_ms=10, max_records=1)
            for key in msg:
                self.data = str(msg[key][0].value, encoding="utf-8")
                data = eval(self.data)
                return json.dumps(data, indent=4, ensure_ascii=False)
                # return


def ControlNodeTest():
    controlnode = ControlNode("command", "data")
    controlnode.GenCommand("s2", "192.168.1.105")
    controlnode.ProduceCommand()
    controlnode.ConsumeData()

def ControlNodeHandle(type,ip,port=None):
    controlnode = ControlNode("command", "data")
    controlnode.GenCommand(type, ip,port)
    controlnode.ProduceCommand()
    return controlnode.ConsumeData()
if __name__ == "__main__":
    ControlNodeTest()
