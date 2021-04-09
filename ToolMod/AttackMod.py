#-*- coding:utf-8 –*-
from ToolMod.PerformanceMod import Performance
from ToolMod.SqlOperationMod import SqlOperation
import GlobalSetting
import socket
from threading import Thread
import threading
import json
from time import sleep

#攻击节点
class AttackSide:
    def __init__(self):
        self.ip = '127.0.0.1'
        self.sql = SqlOperation()
        self.sql.Connect()

    def UpdatePerformance(self):
        '''
        将自身已用资源情况进行存库，
        通过定时器，5秒上传一次
        @return:
        '''
        resource = {}
        performance = Performance()
        resource["NodeIP"] = performance.GetIP()
        resource["CPU"] = performance.GetCPU()
        resource["Memory"] = performance.GetMemory()
        resource["Time"] = performance.GetTime()
        self.ip = resource["NodeIP"]
        sql = SqlOperation()
        sql.Connect()
        #根据自身IP对数据库资源信息进行查询
        query = "SELECT * FROM resource where NodeIP={}".format("'" + resource["NodeIP"] + "'")
        searchResult = sql.SqlQueryOne(query)
        #如果存在表项则更新，不存在则创建
        if searchResult:
            sql.Update("resource", resource)
        else:
            sql.Insert("resource", resource)
        sql.Close()
        self.performanceTimer = threading.Timer(5, self.UpdatePerformance)
        self.performanceTimer.start()

    def CheckTask(self):
        '''
        检查是否有需要执行的任务
        每5秒检查一次
        @return:无
        '''
        query = "SELECT TaskID,TaskType,AssignNode FROM task WHERE Status='Waiting'"
        searchResult = self.sql.SqlQuery(query)
        for eachtuple in searchResult:
            TaskID = eachtuple[0]
            TaskType = eachtuple[1]
            listIP = eachtuple[2].split(',')
            for eachIP in listIP:
                if(self.ip == eachIP):
                    self.AnalyzeAttack(TaskID, TaskType)
        self.taskTimer = threading.Timer(5, self.CheckTask)
        self.taskTimer.start()

    def AnalyzeAttack(self, TaskID, TaskType):
        '''
        从数据库中拿出攻击指令进行执行
        @param TaskID: 需要执行的任务序号
        @param TaskType: 任务类型
        @return: 无
        '''
        print("Start Attack ID:", TaskID, " Type:", TaskType)
        if(TaskType == "Attack"):
            attackDict = {}
            query = "SELECT AttackType,DstIP,DstPort,Intensity,LastTime FROM attacktask WHERE TaskID={}".format(TaskID)
            searchResult = self.sql.SqlQueryOne(query)
            if searchResult:
                attackDict["AttackType"] = searchResult[0]
                attackDict["DstIP"] = searchResult[1]
                attackDict["DstPort"] = searchResult[2]
                attackDict["Intensity"] = searchResult[3]
                attackDict["LastTime"] = searchResult[4]
            attackJson = json.dumps(attackDict)
            self.StartAttack(attackJson)
        elif(TaskType == "Scan"):
            scanDict = {}
            query = "SELECT ScanType,DstIP,DstPort FROM scantask WHERE TaskID={}".format(TaskID)
            searchResult = self.sql.SqlQueryOne(query)
            if searchResult:
                scanDict["ScanType"] = searchResult[0]
                scanDict["DstIP"] = searchResult[1]
                scanDict["DstPort"] = searchResult[2]
            scanJson = json.dumps(scanDict)
            self.StartScan(scanJson)
        else:
            print("Error Type")
        UpdateStatus = {}
        UpdateStatus["TaskID"] = TaskID
        UpdateStatus["Status"] = GlobalSetting.TaskStatus[1]
        self.sql.Update("task", UpdateStatus)
        print("Attack Success")


    def StartAttack(self, attackJson):
        '''
        发起攻击
        @param attackJson: 攻击所需的字段
        @return: 无
        '''
        dataDict = json.loads(attackJson)



    def StartScan(self, scanJson):
        '''
        发起扫描
        @param scanJson:扫描所需字段
        @return: 无
        '''
        dataDict = json.loads(scanJson)

    def StartAttackSide(self):
        '''
        开启攻击节点功能，更新状态，执行任务
        @return:
        '''
        myThread1 = Thread(target=self.UpdatePerformance)
        myThread1.start()
        sleep(1)
        myThread2 = Thread(target=self.CheckTask)
        myThread2.start()

    def Close(self):
        '''
        关闭攻击节点功能
        @return: 无
        '''
        self.performanceTimer.cancel()
        self.taskTimer.cancel()
        self.sql.Close()

if __name__ == "__main__":
    attckSide = AttackSide()
    attckSide.StartAttackSide()
    sleep(20)
    # attckSide.Close()



