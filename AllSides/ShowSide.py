from TransferMod.ClientMod import Client
from GlobalSetting import *

if __name__ =="__main__":
    client = Client(ServerSideIpAddr,ServerPort)
    client.send("123456")