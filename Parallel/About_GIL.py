# from web page: http://cenalulu.github.io/python/gil-in-python/

#! /usr/bin/python

from threading import Thread
import time

def my_counter():
    i = 0
    for _ in range(100000000):
        i += 1
    return True


def single_thread():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        t.join()
    end_time = time.time()
    print("Total time for single thread: %.4f " % (end_time - start_time))


def multi_thread():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        thread_array[tid] = t
    for i in range(2):
        thread_array[i].join()
    end_time = time.time()
    print("Total time for multi threads: %.4f " % (end_time - start_time))


def main():
    single_thread()
    multi_thread()


if __name__ == '__main__':
    main()