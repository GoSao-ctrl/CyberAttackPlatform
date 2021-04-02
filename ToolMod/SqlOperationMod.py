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
            self.cursor.execute("SELECT VERSION()")
            data = self.cursor.fetchone()
            print("data:", data)
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

    def SqlQuery(self,sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                print(row)
            print("Query Success")
        except:
            # self.db.rollback()
            print("Query Fail")

    def Close(self):
        self.db.close()

def test():
    db = pymysql.connect(host="192.168.2.168", user="root", password="123", database="netattack")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("data:", data)

    # sql = """INSERT INTO scantask(TaskID, TaskType, ScanType, DstIP,DstPort)
    #        VALUES (%d,"%s","%s","%s",%d)""" % (1, "a", "12", "127.0.0.1", 6666)
    sql = "INSERT INTO scantask(TaskID, TaskType, ScanType, DstIP,DstPort) VALUES (224242, 'a', '12', '127.0.0.1', 6666)"
    try:
        cursor.execute(sql)
        db.commit()
        print("Insert Success")
    except:
        db.rollback()
        print("Insert Fail")

    db.close()

if __name__ == "__main__":
    # test()
    sqlOpe = SqlOperation()
    sqlOpe.Connect()
    table = "scantask"
    insertDict = {"TaskID":42,"TaskType":"12", "ScanType":"ScanType","DstIP":"192.168.2.138","DstPort":6666}
    sqlOpe.Insert(table,insertDict)
    sql = "SELECT * FROM scantask"
    sqlOpe.SqlQuery(sql)

