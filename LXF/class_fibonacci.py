# -*- encoding = utf-8 -*-

class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a , self.b = self.b , self.a +self.b
        if self.a > 100000:
            raise StopIteration()
        return self.a

    def __str__(self):
        return 'a Fibonacci series instance'

    def __getitem__(self, n):
        a, b = 1,1
        if isinstance(n, int):
            for x in range(n):
                a, b = b, a+b
                return a
        if isinstance(n, slice):
            start = n.start
            end = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(end):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L



print(Fib())

#for n in Fib():
#    print(n)

print(Fib()[0])

print(Fib()[0:5])


#REST API - URL
class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__


#print(Chain().status.user.timeline.list)

class ParamChain(object):
    def __init__(self, path=''):
         self._path = path


    def __getattr__(self, path):
        if path == 'users':
            def users(username):
                # return ParamChain('%s/%s' %(self._path, username))
                return self.__getattr__('users/'+username)
            return users
        else:
            return ParamChain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

# Top implementation
class ParamChain2(object):
    def __init__(self, path=''):
         self._path = path

    def __getattr__(self, path):
        return ParamChain2('%s/%s' % (self._path, path))

    def __call__(self, parameter):
        return ParamChain2('%s/%s' % (self._path, parameter))

    def __str__(self):
        return self._path

    __repr__ = __str__



paramChain = ParamChain()
print(type(paramChain))

print(paramChain.status.user.timeline.list)
print(paramChain.users('leizh').repos.projet)

print(ParamChain2().users('michael').group('student').repos)


