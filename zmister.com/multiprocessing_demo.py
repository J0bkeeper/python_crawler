#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.28 13:13'


from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreaderPool
import time

def test1():
    for n in range(100000):
        for i in range(100000):
            n += i


#多线程，多进程模块下的多线程
def test4():
    for n in range(100000):
        def test5(i):
            n += i
    tpool = ThreaderPool(processes=1)
    tpool.map_async(test5,range(100000))
    tpool.close()
    tpool.join()


def test2():
    for n in range(100000):
        def test3(i):
            n += i
    pool = Pool(processes=1)
    pool.map_async(test3,range(100000))
    pool.close()
    pool.join()


start_time = time.time()
test1()
stop_time = time.time()
print("for循环",stop_time-start_time)

start_time1 = time.time()
test4()
stop_time1 = time.time()
print("多线程",stop_time1-start_time1)

start_time2 = time.time()
test2()
stop_time2 = time.time()
print("多进程",stop_time2-start_time2)