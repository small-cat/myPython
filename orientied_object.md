# 面向对象 - 继承、封装和多态
## 继承
1. 指定超类
Class A
Class B(A)
2. 检查继承
issubclass()
类的特殊属性：`__bases__`, `__class__`
isinstance()
3. 多重继承
当多个基类中同时都有相同的方法时，子类中该方法的定义为基类顺序中第一个出现该方法的基类定义，所以，特别需要注意__多重继承中积累的顺序(方法判定顺序 Method Resolution Order)__

---

4. 接口和内省
hasattr(tc, 'talk') 查看兑现是否含有 talk 方法
hasattr(x, '`__call__`') 检查 x 方法是否可调用
getattr 和 setattr 可用于获得和设置对象属性
如：<code>
setattr(tc, 'name', 'small-cat')
tc.name的值即为 small-cat</code>

特殊属性: `__dict__`能够查看对象内存所有存储的值
相关模块： inspect，能够过去对象的组成