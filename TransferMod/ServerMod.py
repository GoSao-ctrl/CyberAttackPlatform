from socket import *
import select
import json
import queue
from time import sleep
from ToolMod.SqlOperationMod import SqlOperation
import GlobalSetting
class Server:
    def __init__(self, serverPort=6666):
        self.serverPort = serverPort
        self.serverFd = socket(AF_INET, SOCK_STREAM)
        address = ('', serverPort)
        self.serverFd.bind(address)
        self.serverFd.listen(100)
        self.inputs = [self.serverFd]
        self.outputs = []

    def Accept(self):
        print("Common Accept...")
        conn, connAddr = self.serverFd.accept()
        return conn
    def SelectAccept(self):
        print("Select Accept...")
        self.serverFd.setblocking(False)
        num = 0
        while True:
            readable,writeable,errormsg = select.select(self.inputs,self.outputs,[],10)
            num += 1
            print("count:", num)
            for fd in readable:
                if fd == self.serverFd:
                    conn, addr = fd.accept()
                    conn.setblocking(False)
                    self.inputs.append(conn)
                else:
                    recvData = self.Recv(fd)
                    if len(recvData) != 0:
                        sendData = self.Analyze(recvData)
                        self.Send(sendData, fd)
                    else:
                        print("Closing...")
                        self.inputs.remove(fd)
                        fd.close()

    def NodeAllocation(self):
        taskDict={}
        taskDict["TaskID"] = GlobalSetting.TaskID
        taskDict["AssignNode"] = "192.168.2.15"
        taskDict["Status"] = GlobalSetting.TaskStatus[0]
        sql = SqlOperation()
        sql.Connect()
        sql.Insert("task", taskDict)
    def Analyze(self, data):
        print("Analyze")
        dataDict = json.loads(data)
        if(dataDict["TaskType"] == "Attack"):
            GlobalSetting.TaskID += 1
            dataDict["TaskID"] = GlobalSetting.TaskID
            sql = SqlOperation()
            sql.Connect()
            sql.Insert("attacktask", dataDict)
            self.NodeAllocation()
        elif(dataDict["TaskType"] == "Scan"):
            GlobalSetting.TaskID += 1
            dataDict["TaskID"] = GlobalSetting.TaskID
            sql = SqlOperation()
            sql.Connect()
            sql.Insert("scantask", dataDict)
            self.NodeAllocation()
        else:
            print("Error Type")
        return data


    def Recv(self, connectFd):
        recvData = connectFd.recv(1024)
        print("Server Recv:", recvData.decode("gbk"))
        return recvData.decode("gbk")

    def Send(self,sendData,connectFd):
        print("Server Send:",sendData)
        connectFd.send(sendData.encode("gbk"))

    def close(self):
        self.serverFd.close()


def serverTest():
    server = Server()
    type = 1
    if(type):
        server.SelectAccept()
    else:
        conn = server.Accept()
        server.Recv(conn)
        server.Send("test server data", conn)
        server.close()
if __name__ == "__main__":
    serverTest()



