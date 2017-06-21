# -*- encoding: utf-8 -*-
__author__ = 'sholegance'

import re

line = "adsbooooooooooobbby"
line2 = 'study in 北方交通大学'
reg_pattern1 = '.*(b.*b).*'
reg_pattern2 = '.*?(b.*b).*'
reg_pattern3 = '.*?(b.*?b).*'
reg_pattern4 = '.*?([\u4E00-\u9FA5]+大学)'

# 汉字
# [\u4E00-\u9FA5]

print(reg_pattern1, re.match(reg_pattern1, line).group(1))
print(reg_pattern2, re.match(reg_pattern2, line).group(1))
print(reg_pattern3, re.match(reg_pattern3, line).group(1))
print(re.match(reg_pattern4, line2).group(1))
