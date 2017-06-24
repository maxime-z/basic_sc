# -*- encoding = utf-8 -*-

class Student(object):

    #__slots__ limits the dynamically bound attributes
    # This limit does not impose on its subclasses
    __slots__ = ('__name','__score','set_age','age')

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s %3d' % (self.__name, self.__score))

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 60:
            return 'B'
        else:
            return 'C'



#
Lei = Student('Lei', 100)
Qianlin = Student('Qianlin',90)

# Dynamic binding of attributes to an instance
Lei.age = 10
print('Dynamic bound attribut <age>: %s' % Lei.age)

def set_age(self,age):
    self.age = age

# Dynamic binding of methods to an instance
from types import MethodType
Lei.set_age = MethodType(set_age,Lei)

Lei.set_age(27)
print('Attribut <age> modified by dynamically bound method <set_age>: %s' % Lei.age )

# These attributes or methods bound to an instance only limited to the specific instance

##print(Qianlin.age) !AttributeError

# It is also possible to dynamically bind attributes or methods to the class
Student.set_age = set_age
Qianlin.set_age(25)

print('%s <age> %s' % ('Qianlin',Qianlin.age))


# The limits imposed by __slots__
#Qianlin.nationality = 'Chinese'

# The limit is relieved for its subclasses
class GraduatedStudent(Student):
    pass

someone = GraduatedStudent('Other',80)
someone.nationality = 'Chinese'

print(someone.nationality)