import pymysql

class SqlOperation:
    def __init__(self, sqlName="netattack"):
        self.sqlName = sqlName
        self.db = ''
        self.cursor = ''
    def Connect(self):
        try:
            self.db = pymysql.connect(host="192.168.2.168",user="root",password="123",database=self.sqlName)
            self.cursor = self.db.cursor()
            print("Sql Connect Success")
        except pymysql.Error as e:
            print("Sql Connect Fail", str(e))

    def Insert(self,table,dict):
        keys = []
        values = []
        for key,value in dict.items():
            # print("key:",key," value:", value)
            keys.append(key)
            if(isinstance(value,int)):
                values.append(str(value))
            if (isinstance(value, float)):
                values.append(str(value))
            if(isinstance(value,str)):
                temp ="'"+value+"'"
                values.append(temp)
        sql = "INSERT INTO " + table + "("
        sql += ", ".join(keys) + ")"
        sql += " VALUES (" + ",".join(values) + ")"
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Insert Success")
        except:
            self.db.rollback()
            print("Insert Fail")

    def Update(self,table,dict):
        condition = []
        conditionFlag = True
        sql = "UPDATE " + table + " SET "
        for key, value in dict.items():
            if conditionFlag:
                if (isinstance(value, str)):
                    temp = "'" + value + "'"
                elif (isinstance(value, int)):
                    temp = str(value)
                else:
                    temp = value
                condition.append(key)
                condition.append(temp)
                conditionFlag = False
                continue
            # print("key:",key," value:", value)
            if (isinstance(value, int)):
                temp = str(value)
            if (isinstance(value, float)):
                temp = str(value)
            if (isinstance(value, str)):
                temp = "'" + value + "'"
            sql += key + '=' + temp + ','
        sql = sql.strip(',')
        sql += ' WHERE ' + condition[0] + '=' + condition[1]
        # update_sql = 'update resource set NodeIP="192.168.1.212" where CPU=18 '
        # sql2 = "UPDATE resource SET CPU=12.3,Memory=56.3 WHERE NodeIP=192.168.2.212"

        # print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Update Success")
        except:
            self.db.rollback()
            print("Update Fail")

    def SqlQueryOne(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            # print(result)
            print("Query Success")
            return result
        except:
            # self.db.rollback()
            print("Query Fail")
    def SqlQuery(self,sql):
        try:
            self.cursor.execute(sql)
            tupleResults = self.cursor.fetchall()
            results = []
            for row in tupleResults:
                results.append(row)
            # print(result)
            print("Query Success")
            return results
        except:
            # self.db.rollback()
            print("Query Fail")

    def Close(self):
        self.db.close()

def test():
    sqlOpe = SqlOperation()
    sqlOpe.Connect()
    # table = "scantask"
    # insertDict = {"TaskID":42,"TaskType":"12", "ScanType":"ScanType","DstIP":"192.168.2.138","DstPort":6666}
    # sqlOpe.Insert(table,insertDict)
    # query = "SELECT * FROM resource where NodeIP={}".format("'192.168.2.217'")
    # # query = "SELECT * FROM resource"
    # print(query)
    # result = sqlOpe.SqlQueryOne(query)
    # if result:
    #     updateDict = {"NodeIP": "192.168.2.216", "CPU": 21.3, "Memory": 45.3, "Time": "12"}
    #     sqlOpe.Update("resource", updateDict)
    # else:
    #     insertDict = {"NodeIP": "192.168.2.217", "CPU": 62.6, "Memory": 53.6, "Time": "12"}
    #     sqlOpe.Insert("resource", insertDict)
    # query = "SELECT NodeIP from resource ORDER BY (CPU+Memory)ASC LIMIT 2"
    # results = sqlOpe.SqlQuery(query)

    query = "SELECT TaskID from task ORDER BY TaskID DESC LIMIT 1"
    results = sqlOpe.SqlQueryOne(query)

if __name__ == "__main__":
    test()

