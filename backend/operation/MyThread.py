import time
from threading import Thread

a = ''
# 自定义线程函数
def my_threadfunc(name='python3'):
    if a =='':
        raise ValueError("a is null")
    else:
        print(a)
    for i in range(2):
        print("hello", name)
        time.sleep(1)

if __name__ == "__main__":
    # 创建线程01，不指定参数
    thread_01 = Thread(target=my_threadfunc)
    a = 'test'
    # 启动线程01
    thread_01.start()
    thread_01.join()

    # 创建线程02,指定参数，注意逗号不要少，否则不是一个tuple
    thread_02 = Thread(target=my_threadfunc, args=('Curry',))
    # 启动线程02
    thread_02.start()