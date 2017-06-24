# -*- coding: utf-8 -*-
x = "I\'m \"Leizh\""
print(x)

y = r"I'm \"Leizh\""
print(y)

toprint = [123, 456.789, 'Hello, world', 'Hello \'Adam\'', r'Hello "Lei"', r'''Hello, 
12123
lisa''']

for v in toprint:
    print(v)

print('包含中文的字符串')

print(ord('张'))
print(chr(24353))

print('张'.encode('UTF-8'))

#格式化输出 format string output
# %s, %d, %f, %x (hexadecimal integer)
output = 'Hi, %s, you have won %d RMB, congratulations to be the %x%% lucky ones'
print(output % ('Lei', 1000, 2))


#exercise
s1 = 72
s2 = 85

r = (s2-s1)/s1
print('%.1f %%' % (100*r))

if s1 > 100:
    s1 += 1
elif s1 < 80:
    s1 -= 1
else:
    s1 /= 2




