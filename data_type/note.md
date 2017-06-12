#数值型
int
long （2.x）长整形
complex 复数
bool （3.x）布尔型，在3.x版本中才有，true 表示1，false表示0，2.x版本中用1和0表示

---
#非数值型
- string字符串，不能更改
mstr = "hello world"
- list 列表，元素能够修改
mlist = [1, 'hello', 10.2, 3+4j]
- tuple 元组，元素不能修改
mtuple = (1, 'hello', 10.3)

- dictionary 字典，key-value
mdict = {1:'one', 'two':2, 'tuple':mtuple}
- sets 集合(3.x版本才有的)
mset = {'one', 'two', 'one', 1, 2}

---
非数值型，能够进行索引，切片，+，*操作
__注意：__
创建空集合使用函数 set()
创建空字典使用{}
创建空元组使用()，创建一个元素的元组，如下所示： mtuple = ('a', )，以逗号结束

isinstance：认为子类也是父类类型
type：不认为子类是父类类型

---
tuple=("all")
print tuple
结果是
all
这个地方将()作为数学公式中的小括号来处理，所以表示只有一个元素的元组是，需要在后面加上一个逗号，即 
tuple = ("all", )

元组与列表的区别，就在于元组的不可变性，如果向函数传递列表，在任何地方都能发生改变，但是元组不会改变。
**元组提供了一种完整性约束。**