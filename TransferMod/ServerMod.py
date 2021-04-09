#-*- coding:utf-8 –*-
from socket import *
import select
import json
import queue
from time import sleep
from threading import Thread
from ToolMod.SqlOperationMod import SqlOperation
import GlobalSetting
from threading import Timer


class Server:
    def __init__(self, serverPort=6666, attackNum=1):
        '''
        @param serverPort: 服务端口
        @param attackNum: 攻击节点数目
        '''
        self.attackNum = attackNum
        self.data = []
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

    #通过select来完成对于多个攻击端数据的接受
    def SelectAccept(self):
        print("Select Accept...")
        self.serverFd.setblocking(False)
        num = 0
        recvBool = False
        while True:
            num += 1
            print("count:", num)
            #如果收到了至少一份数据并且超时，直接上传数据
            if (recvBool and num > 20):
                self.UploadData()
                break
            readable,writeable,errormsg = select.select(self.inputs,self.outputs,[],10)
            for fd in readable:
                # 攻击端建立的连接
                if fd == self.serverFd:
                    conn, addr = fd.accept()
                    conn.setblocking(False)
                    self.inputs.append(conn)
                else:
                    #攻击端发回的数据
                    recvData = self.Recv(fd)
                    if len(recvData) != 0:
                        if(self.attackNum>1):
                            self.GetData(recvData)
                            self.attackNum -= 1
                            recvBool = True
                        else:
                            #收到所有主机的数据，直接上传
                            self.GetData(recvData)
                            self.UploadData()
                            return
                    else:
                        print("Closing...")
                        self.inputs.remove(fd)
                        fd.close()



    def GetData(self, recvData):
        '''
        攻击数据的收集
        @param recvData: 收到一个攻击端的数据
        '''
        self.data.append(recvData)

    def UploadData(self):
        '''
        上传所收到的攻击数据
        @return: 无
        '''
        print("Upload Data")
        for data in self.data:
            print(data)

    def Recv(self, connectFd):
        '''
        @param connectFd: 监听的套接字
        @return: 解码后的接受数据
        '''
        recvData = connectFd.recv(1024)
        print("Server Recv:", recvData.decode("gbk"))
        return recvData.decode("gbk")

    def Send(self,sendData,connectFd):
        print("Server Send:",sendData)
        connectFd.send(sendData.encode("gbk"))

    def Close(self):
        self.serverFd.close()


def serverTest():
    server = Server(6666,3)
    type = 1
    if(type):
        server.SelectAccept()
    else:
        conn = server.Accept()
        server.Recv(conn)
        server.Send("test server data", conn)
        server.Close()

if __name__ == "__main__":
    serverTest()



