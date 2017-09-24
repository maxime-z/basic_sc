class Student1(object):
    # def __init__(self, s):
    #     self._score = s

    def get_score(self):
        return self._score

    def set_score(self, s):
        if not isinstance(s, int):
            raise TypeError('score must be an integer!')
        if s < 0 or s > 100:
            raise  ValueError('score must in the interval [0,100]!')
        self._score = s


# 通过@property,既能检查参数,又可以用类似属性这样简单的方式来访问类的变量
class Student(object):
    def __init__(self, s):
        self._score = s

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self,s):
        if not isinstance(s, int):
            raise TypeError('score must be an integer!')
        if s < 0 or s > 100:
            raise  ValueError('score must in the interval [0,100]!')
        self._score = s




if __name__ == '__main__':

    david = Student1()
    david.set_score(95)
    print('score: %d' % david.get_score())
    print('Done')

    maxi = Student(90)
    maxi.score=10
    print('score: %d' % maxi.score)
    a = maxi.age
    print(a)



