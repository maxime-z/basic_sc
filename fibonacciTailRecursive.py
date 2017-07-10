# a tail recursion example for fibonacci sequence


def fibTailRecursive(n, a=0, b=1):
    if n == 1:
        return a
    else:
        return fibTailRecursive(n - 1, b, a + b)


for i in range(1, 11):
    print(fibTailRecursive(i))
