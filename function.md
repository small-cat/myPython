# 字符串方法
1. find，在目标字符串中查找子串，返回第一次出现的位置索引，否则返回 -1
<code>'Hello world'.find('world')</code> 
将返回 6
2. join 连接序列中的元素，而且连接的元素必须是 **字符串**
<code>'+'.join(['1', '2', '3'])</code>
将返回 '1+2+3'
3. lower 返回字符串的小写字母版
相关函数参见islower, capitalize, swapcace, title, istitle, upper, isupper
4. replace 替换字符串中出现的所有匹配项
<code>'This is a test'.replace('is', 'eez')</code>
返回结果为 'Theez eez a test'

---

5. strip 去除字符串两侧的空格，不包括内部的空格
<code>'   Hello, World    '.strip()</code>
返回 'Hello, World'
6. split 是 join 的逆方法，将字符串分割成序列
<code>'/usr/bin/python'/split('/')</code>
结果为 ['', 'usr', 'bin', 'python']
相关函数： rsplit, splitlines
7. translate 替换字符串中的某些部分，处理的是单个字符
**能够替换换行符或者某些因平台而异的特殊字符**

---

# 字典常见方法
1. clear()
清楚字典中的所有项，当两个变量同时引用同一个字典时，如果其中一个调用 clear() 函数，再通过这两个变量访问字典时，字典都是空的

2. copy() 与 deepcopy()
copy是浅拷贝，返回一个具有相同key-value 的新字典，原字典内容发生改变，返回的新字典也会改变(因为值本身就是相同的)
deepcopy() 是深度拷贝，返回的是一个副本，原字典发生变化，新字典不变。

---

3. fromkeys 使用给定的键建立新的字典，每个键都有一个默认值 None
使用dict调用该方法，因为 dict 是所有字典的类型
dict.fromkeys(['name', 'age']) 
返回 {'name':None, 'age':None}， 默认值为 None，还可以自己设置默认值
dict.fromkeys(['name', 'age'], '(unknown)')
返回结果为 {'name':'(unknown)', 'age':'(unknown)'}

4. get 访问字典项，访问不存在的字典项时，会报错
5. has_key 检查字典中是够含有特定键，3.x 版本中去掉了该函数
d.has_key(k) 相当于 k in d

---

6. items 和 iteritems
items 将字典项以列表的方式返回，每一个项都表示为 (key, value) 的形式
iteritems 效率更高，返回的是一个迭代器对象，比如
<code>c = {'key1': ['hello'], 'name': ['redis', 'python']}
print c.items()
#返回[('key1', ['hello']), ('name', ['redis', 'python'])]
it = c.iteritems()
for k, v in it:
	print k, v
'''
返回
key1 ['hello']
name ['redis', 'python']
'''
</code>

---

7. pop 获得字典中给定键的值，并将这个 key-value 从字典中删除
d.pop('x')
8. popitem() 随机弹出字典中的一个项，并从原字典中删除
9. setdefault
<code>d={}
d.setdefault('name', 'unknown')</code>
返回值为 'unknown'
如果字典中存在键为'name'，将不发生改变，并返回该键的值，如果不存在，将创建该键，并将值设置为默认值'unknown'，同时返回该值
10. update 可以利用一个字典更新另外一个字典的值
