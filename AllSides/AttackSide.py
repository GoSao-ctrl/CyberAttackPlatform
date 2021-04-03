from ToolMod.PerformanceMod import Performance
from ToolMod.SqlOperationMod import SqlOperation
import socket
import threading
import time


def AttackSide():
    resource = {}
    performance = Performance()
    resource["NodeIP"] = performance.GetIP()
    resource["CPU"] = performance.GetCPU()
    resource["Memory"] = performance.GetMemory()
    resource["Time"] = performance.GetTime()
    sql = SqlOperation()
    sql.Connect()
    query = "SELECT * FROM resource where NodeIP={}".format("'"+resource["NodeIP"]+"'")
    searchResult = sql.SqlQueryOne(query)
    if searchResult:
        sql.Update("resource", resource)
    else:
        sql.Insert("resource", resource)
    sql.Close()
    timer = threading.Timer(5, AttackSide)
    timer.start()

if __name__ == "__main__":
    AttackSide()


