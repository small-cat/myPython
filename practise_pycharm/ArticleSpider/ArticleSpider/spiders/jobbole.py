# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from urllib import parse
from ArticleSpider.utils.common import gen_md5

from ArticleSpider.items import JobBoleArticleItem

__author__ = "Sholegance (mblrwuzy@gmail.com)"
__date__ = ""
__status__ = ""
__version__ = ""

__metaclass__ = type


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url，交给 scrapy 下载后并进行解析，即调用 parse 函数解析
        2. 然后获取下一页的文章 url，按照1 2 循环

        ---
        对于 parse 函数，一般做三种事情
        a. 解析返回的数据 response data
        b. 提取数据，生成 ITEM
        c. 生成需要进一步处理 URL 的 Request 对象
        """
        post_nodes = response.css("#archive .floated-thumb .post-thumb")    # a selector, 可以在这个基础上继续做 selector
        # 某些网站中，url 仅仅只是一个后缀，需要将当前页面的url+后缀进行拼接，使用的是 parse.urljoin(base, url)
        # 如果urljoin中的url没有域名，将使用base进行拼接，如果有域名，将不会进行拼接,此函数在 python3 的 urllib 库中
        # Request(meta参数)：meta参数是一个字典{},作为回调函数的参数
        for post_node in post_nodes:
            post_url = post_node.css("a::attr(href)").extract_first("")     # extract_first("")传递了一个“”空置作为默认值
            img_url = post_node.css("a img::attr(src)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={"front-image-url":img_url}, callback=self.parse_detail)

        # 必须考虑到有前一页，当前页和下一页链接的影响，使用如下所示的方法
        next_url = response.css("span.page-numbers.current+a::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        """
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0]
        match_re = re.match("([0-9/]*).*",
                            response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip())
        if match_re:
            create_date = match_re.group(1)
        votes = int(response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0])
        match_fav = re.match('.*?(\d+).*',
                             response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0])
        if match_fav:
            fav_nums = int(match_fav.group(1))
        else:
            fav_nums = 0

        comments_nums_match = re.match(".*?(\d+).*",
                                       response.xpath("//a[@href='#article-comment']/span/text()").extract_first())
        if comments_nums_match:
            comments_nums = int(comments_nums_match.group(1))
        else:
            comments_nums = 0

        tag_lists = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_lists = [ele for ele in tag_lists if not ele.strip().endswith('评论')]
        tags = ','.join(tag_lists)

        cpyrights = response.xpath("//div[@class='copyright-area']/*/text()").extract()
        #content = response.xpath("//div[@class='entry']/*/text()").extract()
        """

        ########################################
        #implement with css selector
        article_item = JobBoleArticleItem() # 实例化 item 对象

        front_img_url = response.meta.get("front-image-url", "") # 封面图
        title = response.css(".entry-header h1::text").extract()[0]
        match_date = re.match("([0-9/]*).*",
                              response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip())
        if match_date:
            create_date = match_date.group(1)

        votes_css = response.css(".vote-post-up h10::text").extract_first()
        if votes_css:
            vote_nums = int(votes_css)
        else:
            vote_nums = 0

        ma_fav_css = re.match(".*?(\d+).*",
                              response.css(".bookmark-btn::text").extract_first())
        if ma_fav_css:
            fav_nums = int(ma_fav_css.group(1))
        else:
            fav_nums = 0

        ma_comments_css = re.match(".*?(\d+).*",
                                   response.css("a[href='#article-comment'] span::text").extract_first())
        if ma_comments_css:
            comment_nums = int(ma_comments_css.group(1))
        else:
            comment_nums = 0

        tag_lists_css = response.css(".entry-meta-hide-on-mobile a::text").extract()
        tag_lists_css = [ele for ele in tag_lists_css if not ele.strip().endswith('评论')]
        tags = ','.join(tag_lists_css)

        cpyrights = response.css(".copyright-area").extract()
        content = response.css(".entry *::text").extract()

        # 复制 item 对象
        article_item["title"] = title
        article_item["create_date"] = create_date
        article_item["url"] = response.url
        article_item["front_img_url"] = [front_img_url]
        article_item["fav_nums"] = fav_nums
        article_item["comment_nums"] = comment_nums
        article_item["vote_nums"] = vote_nums
        article_item["tags"] = tags
        article_item["cpyrights"] = cpyrights
        article_item["content"] = content
        article_item["object_id"] = gen_md5(response.url)

        # 将 item 传递到 scrapy, scrapy 会通过 http 将 item 传递到 pipeline, 数据操作，都可以集中在 pipeline 中进行处理
        yield article_item
