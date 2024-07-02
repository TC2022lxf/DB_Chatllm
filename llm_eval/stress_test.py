from threading import Thread
from multiprocessing import Process
import os

def work():
    print('hello')

if __name__ == '__main__':
    #在主进程下开启线程
    t=Thread(target=work)
    t.start()
    print('主线程')
    '''
    打印结果:
    hello
    主线程/主进程
    '''

    #在主进程下开启子进程
    t=Process(target=work)
    t.start()
    print('/主进程')
    '''
    打印结果:
    主线程/主进程
    hello
    '''