from socket import *
import select

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

    def close(self):
        self.clientFd.close()
if __name__ == "__main__":
    client = Client("127.0.0.1",6666)
    client.send("123")
    client.recv()
    client.close()
