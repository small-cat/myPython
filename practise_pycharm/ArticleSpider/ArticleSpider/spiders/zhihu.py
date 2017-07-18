# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json
from PIL import Image

from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem

try:
    import urlparse as parse # in python2
except ImportError:
    from urllib import parse


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_answer_url = """
    https://www.zhihu.com/api/v4/questions/{0}/answers?include=data[*].is_normal,is_collapsed,annotation_action,\
    annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,\
    editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,\
    review_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;\
    data[*].author.follower_count,badge[?(type=best_answerer)].topics&offset={1}&limit={2}&sort_by=default"""

    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"
    }

    def parse(self, response):
        """
        提取出 html 页面中的所有 url，深度优先遍历，跟踪这些 url 进一步提取
         如果提取的 url 为 /question/XXX 就下载之后直接进入解析页面
         如果提取的 url 为 /answer/XXX 需要先进行处理，这是知乎的两个不同的版本
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果是 question 相关页面，则下载后交由提取函数进行处理
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)

                # scrapy 是通过 yield 将 Request 对象提交给下载器下载的
                # 如果是 url，交给下载器下载，如果是 item，路由到 pipeline 做处理
                yield scrapy.Request(url, meta={"question_id": question_id}, headers=self.headers,
                                     callback=self.parse_question)
            else:
                # 深度优先，如果没有匹配到，那么继续请求页面 url
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        """
        处理 question 页面，从页面中提取出具体的 question item 和 answer item

        这个函数中也可以继续按照 parse 一样，对所有的 url 进行跟踪
        """
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        if "answer" not in response.url:
            # 处理新版本
            item_loader.add_css("question_title", ".QuestionHeader .QuestionHeader-title::text")
            item_loader.add_css("question_content", ".QuestionHeader-detail .RichText::text")
            item_loader.add_value("question_url", response.url)
            item_loader.add_value("question_id", int(response.meta.get("question_id", "")))
            item_loader.add_css("answer_num", ".QuestionMainAction::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("attentioned_num", ".NumberBoard-value::text")
            item_loader.add_css("scanned_num", ".NumberBoard-value::text")
            item_loader.add_css("question_topics", ".Tag-content .Popover div::text")
        else:
            # 处理旧版本
            item_loader.add_css("question_title", ".QuestionHeader .QuestionHeader-title::text") #
            item_loader.add_css("question_content", ".QuestionHeader-detail .RichText::text") #
            item_loader.add_value("question_url", response.url)
            item_loader.add_value("question_id", int(response.meta.get("question_id", "")))
            item_loader.add_css("answer_num", ".QuestionMainAction::text") #
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("attentioned_num", ".NumberBoard-value::text")
            item_loader.add_css("scanned_num", ".NumberBoard-value::text")
            item_loader.add_css("question_topics", ".Tag-content .Popover div::text")

        question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(int(response.meta.get("question_id")), 0, 20),
                             headers=self.headers, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        """
        提取知乎 answer item
        """
        pass

    def start_requests(self):
        """
        返回登录页面，在回调函数中，提取 xrsf 的值
        """
        return [scrapy.Request('https://www.zhihu.com/#signin', callback=self.login, headers=self.headers)]

    def get_checkcode(self):
        """
        获取验证码
        """

    def login(self, response):
        response_text = response.text
        xsrf = ""

        match_obj = re.search('.*name="_xsrf" value="(.*?)"', response_text)
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "13530210085",
                "password": "wuzhenyu25977758",
                "captcha": ""
            }

        t = str(int(time.time() * 1000))
        checkcode_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)

        """
        必须保证验证码的使用，与得到验证码的链接请求是在同一个会话连接中，此处使用 Request 的方法，
        通过 scrapy 将请求下载之后，使用回调函数，在回调函数中进行处理，保证回调函数中的 response 与获取验证码时
        是在同一个会话中
        """
        yield scrapy.Request(checkcode_url, meta={"post_data": post_data}, headers=self.headers,
                             callback=self.login_with_checkcode)

    def login_with_checkcode(self, response):
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = response.meta.get("post_data", {})
        with open("checkcode.gif", "wb") as f:
            f.write(response.body)
            f.close()

        try:
            im = Image.open("checkcode.gif")
            im.show()
            # im.close()    # no close function
        except:
            pass

        post_data["captcha"] = input("checkcode: ")

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        """
        检查登录是否成功
        """
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)   # 默认回调函数为 parse