from multiprocessing import  Queue
from threading import Thread

def Producer(q):
    print("start producer")
    q.put("hello")

    print("end producer\n")

def Consumer(q):
    print("start consumer\n")
    while 1:
        data = q.get()
        print("consumer get data:{0}".format(data))
        return data

if __name__ == "__main__":
    q = Queue()
    pro = Thread(target=Consumer,args=(q,))
    pro.start()
    Producer(q)