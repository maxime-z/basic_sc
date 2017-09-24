from functools import reduce

def char2num(c):
    nums = '0123456789'
    dic = {}
    for i,char in enumerate(nums):
        dic[char] = i
    return dic[c]

def fn(x,y):
    return 10*x + y

def str2int(s):
    return reduce(fn,map(char2num, s))

n = str2int('12345')
print(type(n),n,n-45)


def strTint(s):
    def char2num(c):
        nums = '0123456789'
        dic = {}
        for i, char in enumerate(nums):
            dic[char] = i
        return dic[c]

    def fn(x, y):
        return 10 * x + y
    return reduce(fn, map(char2num, s))

n = strTint('12345')
print(type(n),n,n-45)


def normalize(name):
    def cap(s):
        if not isinstance(s,str):
            raise TypeError("only str parameter acceptable")
        return s.capitalize()
    return map(cap,name)

names = ['adam', 'LISA', 'barT']

print(list(normalize(names)))


def prod(L):
    return reduce(lambda x,y:x*y, L)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))


# string to float


def char2numWithPoint(c):
    nums = '0123456789.'
    dic = {}
    for i,char in enumerate(nums):
        dic[char] = i
    return dic[c]


def fnF(x,y):

    return 10*x + y


def str2float(s):
    l = map(char2numWithPoint,s)
    print(list(l))


    return 0

print('str2float(\'123.456\') =', str2float('123.456'))
