import sys

''' learning python3
difference between python2.7 and python 3.6
'''

# first python 
print("hello world!");
print("你好，世界");

print(help(max));
#print(max.__doc__);

''' data type in python
number
string
boolean
list
tuple
sets
dictionary
'''
a, b, c, d = 20,  5.5, True, 4+3j;
print(type(a), type(b), type(c), type(d))

# list
print(isinstance(a, int))
list = [ 'abcd', 786 , 2.23, 'runoob', 70.2 ]
tinylist = [123, 'runoob']
 
print (list)            # 输出完整列表
print (list[0])         # 输出列表第一个元素
print (list[1:3])       # 从第二个开始输出到第三个元素
print (list[2:])        # 输出从第三个元素开始的所有元素
print (tinylist * 2)    # 输出两次列表
print (list + tinylist) # 连接列表