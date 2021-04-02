from GlobalSetting import *
from TransferMod.ServerMod import Server
from TransferMod.MsgQueue import Consumer

if __name__ == "__main__":
    server = Server(serverPort=ServerPort)
    server.SelectAccept()