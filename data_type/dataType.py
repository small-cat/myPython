# -*- encoding:utf-8 -*-

print "###### DATA TYPE ######"

# LIST
print "LIST"
MLIST = ['abcd', 786, 2.23, 'runoob', 70.2]
MTINYLIST = [123, 'runoob']
print MLIST            # 输出完整列表
print MLIST[0]         # 输出列表第一个元素
print MLIST[1:3]       # 从第二个开始输出到第三个元素
print MLIST[2:]        # 输出从第三个元素开始的所有元素
print MTINYLIST * 2    # 输出两次列表
print MLIST + MTINYLIST # 连接列表

# Dictionary
print "DICTIONARY"
MDICT = {}
MDICT['one'] = "This is one"
MDICT[2] = "This is two"
MTINYDICT = {'name':'john', 'code':6734, 'dept':'sales'}
print MDICT['one']          # 输出键为'one' 的值
print MDICT[2]              # 输出键为 2 的值
print MTINYDICT             # 输出完整的字典
print MTINYDICT.keys()      # 输出所有键
print MTINYDICT.values()    # 输出所有值
MDICT2 = {1:'one', 'two':2}
print MDICT2

# mix
MTUPLE = ("abcd", 1, MDICT)
MY_DICT = {'mdict':MTUPLE}
print MTUPLE
print MY_DICT

# convert
A = 100
B = 100.23
MSTR = "10 + 20.1"
print int(B)
print float(A)
print complex(A)
print str(B)
print repr(MSTR)
print eval(MSTR)
print tuple(MSTR)
print list(MSTR)
print set(MSTR)