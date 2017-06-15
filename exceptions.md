## exceptions 异常模块
查看模块中所有的异常方法
import exceptions
dir(exceptions)
## 自定义异常
class SomeCustomeExceptions(Exception): pass
即创建一个集成自 Exception 异常类的子类，再添加自己的异常方法

---

## 捕捉异常
try:
	x = input()
    y = input()
    print x/y
except (ZeroDivisionError, NameError, TypeError), e
	print e
可以一次捕捉多个异常，如上面，通过元组的方式，也可以分别捕捉每一个异常，通过多写几个except 语句的方式。
e 表示捕捉异常对象，程序捕获到异常时，不会停止，同时又能访问异常对象本身，就通过对象 e 来访问

---

## 捕捉所有异常
try：
	statement
except:
	print "Something wrong"
    
或者
except Exception ,e
	print e
对异常对象 e 做一些检查会更好

---

## 完整的异常语句
try:
	statement
except:
	statement
else:
	statement
finally:
	statement
