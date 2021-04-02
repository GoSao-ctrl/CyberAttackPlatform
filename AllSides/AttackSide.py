from ToolMod.PerformanceMod import Performance
from ToolMod.SqlOperationMod import SqlOperation
import socket
def AttackSide():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(ip)
    performance = Performance()
    performance.GetCPU()
    performance.GetMemory()
    performance.GetTime()


if __name__ == "__main__":
    AttackSide()


