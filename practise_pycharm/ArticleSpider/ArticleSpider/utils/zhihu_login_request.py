# -*- encoding: utf-8 -*-
import requests
import re
import time
import os

from PIL import Image

__author__ = "Sholegance"

# python 中的 cookie lib，能够读取本地的 cookie 文件，生成 cookie，然后赋值给requests 的 cookie
try:
    import cookielib    # python 2版本
except ImportError:
    import http.cookiejar as cookielib  # python3 版本


session = requests.session()    # 某一次连接，是一个长链接，keep-alive，这样就不需要每一次 request 的时候，都要去建立一次连接
# 使用 cookielib 实例化 session的cookies，然后才能使用save() 保存cookies，不然在后面就会报错
# 当前目录中的 cookies.txt 内容是我根据在 firefox 浏览器登录成功后，记录的 cookies 复制下来的，此处代码没有校验码，还不能登录成功
# 如果想成功登录，就将下面的 cookies_new.txt 改成 cookies.txt 即可
session.cookies = cookielib.LWPCookieJar(filename="cookies_new.txt")

try:
    # 成功加载 load cookie 之后，将不再返回首页
    session.cookies.load(ignore_discard=True)
except Exception:
    print("can not load cookies")

agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"
header = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": agent
}


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        # f.write(response.text)
        # 上边打开文件的方式是 wb，写入的时候， python3 会将数据转成 unicode 编码，直接写入的话，会出现
        # TypeError: a bytes-like object is required, not 'str'，所以需要先将数据编码成 utf-8 编码，再写入，也就是 bytes-like
        f.write(response.text.encode("utf-8"))
    print("get index page into index_page.html")
    f.close()


def get_xsrf_by_request():
    """
    requests.get 方法访问的时候，http get 的消息header中的 user-agent 默认设置的是 python2/python3,有些服务器会验证
    user-agent 的合法性，从而一定程度上阻止直接使用requests这种方法爬虫，比如返回 500 的错误码

    header 可以是自定义的
    """
    response = requests.get("https://www.zhihu.com", headers=header)    # 这个参数必须是 headers
    # print(response.text)
    match_obj = re.search('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def get_xsrf_by_session():
    response = session.get("https://www.zhihu.com", headers=header)    # 这个参数必须是 headers
    # print(response.text)
    match_obj = re.search('.*name="_xsrf" value="(.*?)"', response.text)    # match vs search
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def zhihu_login(account, password):
    """
    模拟知乎登录
    """
    post_data = {}
    post_url = ""
    if re.match("^1\d{10}", account):   # 手机号码
        print("phone login")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            # "_xsrf":get_xsrf_by_request(),
            "_xsrf": get_xsrf_by_session(),
            "phone_num": account,
            "password": password
        }

        print(header)
        print(post_data)
    else:
        if "@" in account:
            print("email login")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf_by_session(),
                "email": account,
                "password": password
            }

        # response = requests.post(post_url, data=post_data, headers = header)

    # get check code image
    checkcode_url = "https://www.zhihu.com/captcha.gif?r=" + str(int(time.time()*1000)) + "&type=login"
    print(checkcode_url)
    """
    下面获取验证码，只能使用 session.get，而不能使用 requests.get
    因为一次 session 就是一次会话，在后面继续使用验证码登录时，是在同一个 session 中的，session 会记录很多值，cookie 等
    但是，如果使用的是 requests ，前后就不再同一个会话中，那么后面将带有验证码的 post_data 发送过去时，会显示验证码无效，
    登录失败
    
    但是在 scrapy 中，是没有 session的，使用 requests 又不行，如何解决呢？
    """
    resp = session.get(checkcode_url, headers=header).content
    with open("checkcode.gif", "wb") as f:
        f.write(resp)
    f.close()

    try:
        im = Image.open("checkcode.gif")
        im.show()
        im.close()
    except:
        pass

    post_data["captcha"] = input("checkcode:")
    response_text = session.post(post_url, data=post_data, headers = header)
    session.cookies.save()  # 将服务器返回的 cookies 保存到本地，下一次登录的时候，直接从文件中获取


def is_login():
    """
    通过个人中心页面返回状态码，来判断用户是否处于登录状态
    """
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        # httpcode 为 200 表示正确，用户处于登录状态，否则，处于未登录状态
        # 302 表示临时重定向
        print("用户未登录")
        return False
    else:
        print("用户已登录")
        return True

if __name__ == "__main__":
    zhihu_login("13530210085", "wuzhenyu25977758")
    # get_index()
    is_login()