# -*- encoding: utf-8 -*-
import fileinput, re

"""
content of template file :
[x = 2]
[y = 3]
The sum of [x] and [y] is [x + y]
----
the result is:
The sum of 2 and 3 is 5
"""

# pattern
field_pat = re.compile(r'\[(.+?)\]')

# 收集变量
mscope = {}


def replacement(match):
    """
    replace template file
    """
    code = match.group(1)
    try:
        return str(eval(code, mscope))   # get result of expression conveyed by code, mscope as global namespace
    except SyntaxError:
        exec code in mscope  # if not expression, catch SyntaxError, and exec statement
                             # x = 2, y = 3
        print code           # show code
        return ''


lines = []
for line in fileinput.input('E:\document\VisualStudioCode\myPython\practise_pycharm\cmsz_python\\temp.txt'):
    lines.append(line)
text = ' '.join(lines)

"""
If repl is a function, it is called for every non-overlapping occurrence of pattern. 
The function takes a single match object argument, and returns the replacement string. 
"""
print field_pat.sub(replacement, text)

fp = open('E:\document\VisualStudioCode\myPython\practise_pycharm\cmsz_python\\temp.txt', 'r+')
lines = fp.readlines()
print lines

data = ['1\n', '2\n', '3\n', '4\n'] # 这种方法写文件，换行符需要自己设定，并且序列必须有字符串组成
fp.writelines(data)
fp.close()