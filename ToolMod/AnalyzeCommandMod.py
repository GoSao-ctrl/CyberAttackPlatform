#-*- coding:utf-8 –*-
import GlobalSetting
import json
from ToolMod.SqlOperationMod import SqlOperation

class AnalyzeCommand:
    def __init__(self):
        self.sql = SqlOperation()
        self.sql.Connect()
        self.GetTaskID()

    def GetTaskID(self):
        '''
        获得当前任务ID
        @return: 无
        '''
        query = "SELECT TaskID from task ORDER BY TaskID DESC LIMIT 1"
        result = self.sql.SqlQueryOne(query)
        if result:
            GlobalSetting.TaskID = result[0]

    def NodeAllocation(self, TaskType, NodeNum=1):
        '''
        根据攻击节点状态进行任务分配
        @param TaskType: 任务类型
        @param NodeNum: 参与攻击任务的节点数目
        @return: 无
        '''
        #根据CPU+Memory的值进行排序，找到最小的N个节点
        query = "SELECT NodeIP from resource ORDER BY (CPU+Memory) ASC LIMIT {}".format(NodeNum)
        tupleResults = self.sql.SqlQuery(query)
        results = []
        for row in tupleResults:
            results.append(row[0])
        taskDict = {}
        taskDict["TaskID"] = GlobalSetting.TaskID
        taskDict["TaskType"] = TaskType
        taskDict["AssignNode"] = ",".join(results)
        taskDict["Status"] = GlobalSetting.TaskStatus[0]
        self.sql.Insert("task", taskDict)

    def Analyze(self, data):
        '''
        解析展示端发来的指令，进行解析存库
        @param data: 指令数据
        @return: 无
        '''
        print("Analyze")
        dataDict = json.loads(data)
        if(dataDict["TaskType"] == "Attack"):
            GlobalSetting.TaskID += 1
            dataDict["TaskID"] = GlobalSetting.TaskID
            NodeNum = dataDict["TaskNode"]
            self.sql.Insert("attacktask", dataDict)
            self.NodeAllocation("Attack", NodeNum)
        elif(dataDict["TaskType"] == "Scan"):
            GlobalSetting.TaskID += 1
            dataDict["TaskID"] = GlobalSetting.TaskID
            self.sql.Insert("scantask", dataDict)
            self.NodeAllocation("Scan")
        else:
            print("Error Type")

    def Close(self):
        self.sql.Close()

def ProduceAttack():
    '''
    自主发起攻击，完成存库
    @return: 无
    '''
    attackCommandDict = {}
    attackCommandDict["TaskType"] = "Attack"
    attackCommandDict["AttackType"] = "DDoS"
    attackCommandDict["DstIP"] = "192.168.2.211"
    attackCommandDict["DstPort"] = 80
    attackCommandDict["Intensity"] = 1
    attackCommandDict["LastTime"] = 3600
    attackCommandDict["TaskNode"] = 3
    attackCommand = json.dumps(attackCommandDict)

    scanCommandDict = {}
    scanCommandDict["TaskType"] = "Scan"
    scanCommandDict["ScanType"] = "OS"
    scanCommandDict["DstIP"] = "192.168.2.211"
    scanCommandDict["DstPort"] = 80
    scanCommand = json.dumps(scanCommandDict)

    produceCommand = AnalyzeCommand()
    produceCommand.Analyze(scanCommand)

if __name__ == "__main__":
    ProduceAttack()