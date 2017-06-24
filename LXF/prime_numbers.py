# -*- coding = ntf-8 -*-
def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n

def _not_divisible(n):
    return lambda x: x % n > 0

# the Sieve of Eratosthenes
# 埃拉托色尼筛选法
def primes():
    yield  2
    it = _odd_iter()
    while True:
        n = next(it)
        yield  n
        it = filter(_not_divisible(n),it)

g = (x**2 for x in range(1,100))


# test
i = 0
a = primes()
while i < 100:
    i += 1
    #print(next(g))

    print(next(a))# why it does not work like the function below

# test2
for n in primes():
    if n < 1000:
        print(n)
    else:
        break

