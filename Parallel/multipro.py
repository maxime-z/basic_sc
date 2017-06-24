import multiprocessing
import time

def f(x):
    return x * x


def multiProcess(n):
    cores = 1
    pool = multiprocessing.Pool(processes=cores)
    xs = range(n)


    start_time = time.time()
    #method 1:map
    pool.map(f,xs)
    end_time = time.time()
    return end_time-start_time

def singleProcess(n):
    cores = 1
    pool = multiprocessing.Pool(processes=cores)
    xs = range(n)

    start_time = time.time()
    # method 1:map
    pool.map(f, xs)
    end_time = time.time()
    return end_time-start_time

def main():
    n = int(10e5)
    print(singleProcess(n))
    print(multiProcess(n))

if __name__ == '__main__':
    main()