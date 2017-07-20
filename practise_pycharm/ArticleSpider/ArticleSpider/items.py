# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
"""
定义数据保存的格式
"""

import scrapy
import re
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from ArticleSpider.utils.common import extract_nums
from ArticleSpider.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT


def get_date(value):
    re_match = re.match("([0-9/]*).*?", value.strip())
    if re_match:
        create_date = re_match.group(1)
    else:
        create_date = ""
    return create_date


def remove_comment_tag(value):
    """
    去掉 tag 中的 “评论” 标签
    """
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    """
    do nothing, 只是为了覆盖 ItemLoader 中的 default_processor
    """
    return value


def get_scanned_num(value):
    """
    获取知乎浏览数
    """
    if len(value) == 2:
        return value[1]
    else:
        return 0


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    """
    定义自己的 Item 类
    """
    """
    # 定义1：在 jobbole.py 中纯粹使用 response.css 来提取数据
    title = scrapy.Field()          # Field()能够接收和传递任何类型的值,类似于字典的形式
    create_date = scrapy.Field()    # 创建时间
    url = scrapy.Field()            # 文章路径
    front_img_url_download = scrapy.Field()  # 文章封面图片路径,用于下载，赋值时必须为数组形式
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field() # 保存图片路径（本地路径）
    fav_nums = scrapy.Field()       # 收藏数
    comment_nums = scrapy.Field()   # 评论数
    vote_nums = scrapy.Field()      # 点赞数
    tags = scrapy.Field()           # 标签分类 label
    # cpyrights = scrapy.Field()      # 版权，著作人相关信息
    content = scrapy.Field()        # 文章内容
    object_id = scrapy.Field()      # 文章内容的md5的哈希值，能够将长度不定的 url 转换成定长的序列
    """

    # 定义2：在 jobbole.py 中，使用 ItemLoader 来提取数据
    #
    """
    title = scrapy.Field(
        input_processor = MapCompose(lambda x:x+"-Sholegance"),     # 当 item 的值传递进来的时候，可以通过这个做预处理
        output_processor = TakeFirst()
    )
    MapCompose 参数可以是任意多个函数，也可以是lambda 的匿名函数，item 传入的值，通过 itemloader 获取的，是一个 list，该
    list 中的每一个元素都会调用所有 MapCompose 中传入的函数并进行处理
    
    TakeFirst() 表示输出给 title 的只是取第一个值
    但是，如果有 100 个变量，这么做就需要在每一个变量的定义 Field() 离添加这些，比如添加 TakeFirst()，这也是一件很繁琐的事情
    所以，我们可以自定义一个 ItemLoader 类，继承 scrapy.loader 中的 ItemLoader 类，然后设置默认值就可，
    如下定义的 ArticleItemLoader 类
    """
    title = scrapy.Field()
    create_date = scrapy.Field(     # 创建时间
        input_processor=MapCompose(get_date),
        output_processor=Join("")
    )
    url = scrapy.Field()            # 文章路径
    front_img_url_download = scrapy.Field(    # 文章封面图片路径,用于下载，赋值时必须为数组形式
        # 默认 output_processor 是 TakeFirst()，这样返回的是一个字符串，不是 list，此处必须是 list
        # 修改 output_processor
        output_processor=MapCompose(return_value)
    )
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field() # 保存图片路径（本地路径）
    fav_nums = scrapy.Field(        # 收藏数
        input_processor=MapCompose(extract_nums)
    )
    comment_nums = scrapy.Field(    # 评论数
        input_processor=MapCompose(extract_nums)
    )
    vote_nums = scrapy.Field(       # 点赞数
        input_processor=MapCompose(extract_nums)
    )
    tags = scrapy.Field(           # 标签分类 label
        # 本身就是一个list, 输出时，将 list 以 commas 逗号连接
        input_processor=MapCompose(remove_comment_tag),
        output_processor = Join(",")
    )
    content = scrapy.Field(        # 文章内容
        # content 我们不是取最后一个，是全部都要，所以不用 TakeFirst()
        output_processor=Join("")
    )
    object_id = scrapy.Field()      # 文章内容的md5的哈希值，能够将长度不定的 url 转换成定长的序列

    def get_insert_sql(self):
        insert_sql = """insert into article(title, create_date, url, url_object_id, front_img_url, front_img_path, \
        comment_nums, fav_nums, vote_nums, tags, content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, \
        '%s', '%s');""" % (self["title"], self["create_date"], self["url"], self["object_id"], self["front_img_url"],
        self["front_img_path"], self["comment_nums"], self["fav_nums"], self["vote_nums"], self["tags"],
        self["content"])

        return insert_sql


class ArticleItemLoader(ItemLoader):
    """
    自定义 ItemLoader, 就相当于一个容器
    """
    # 这里表示，输出获取的 ArticleItemLoader 提取到的值，都是 list 中的第一个值
    # 如果有的默认不是取第一个值，就在 Field() 中进行修改
    default_output_processor = TakeFirst()


class ZhihuQuestionItem(scrapy.Item):
    """
    知乎的问题 item
    """
    question_id = scrapy.Field(
        output_processor=TakeFirst()
    )        # 问题 id
    question_topics = scrapy.Field(
        output_processor=Join(",")
    )    # 问题主题
    question_url = scrapy.Field(
        output_processor=TakeFirst()
    )       # 问题链接
    question_title = scrapy.Field(
        output_processor=TakeFirst()
    )     # 问题标题
    question_content = scrapy.Field(
        output_processor=Join("")
    )   # 问题内容
    answer_num = scrapy.Field(
        input_processor=MapCompose(extract_nums),
        output_processor=TakeFirst()
    )         # 回答数
    comments_num = scrapy.Field(
        input_processor=MapCompose(extract_nums),
        output_processor=TakeFirst()
    )       # 评论数
    attentioned_num = scrapy.Field(
        output_processor=TakeFirst()
    )    # 关注数
    scanned_num = scrapy.Field(
        input_processor=MapCompose(get_scanned_num),
        output_processor=TakeFirst()
    )        # 浏览数
    crawl_time = scrapy.Field(
        output_processor=TakeFirst()
    )         # 爬取时间

    def get_insert_sql(self):
        """
        构造知乎 question 表的sql
        """
        # 不理解为什么全部都是使用 %s
        insert_sql = "insert into zhihu_question(question_id, question_url, question_title, answer_num, comments_num," \
                     " attentioned_num, scanned_num, question_topics) values (%s, %s, %s, %s, %s, %s, %s, %s) " \
                     " ON DUPLICATE KEY UPDATE answer_num=answer_num, comments_num=comments_num, " \
                     "attentioned_num=attentioned_num, scanned_num=scanned_num"

        params = (self["question_id"], self["question_url"], self["question_title"], self["answer_num"],
                  self["comments_num"], self["attentioned_num"], self["scanned_num"], self["question_topics"])
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    """
    知乎回答 item
    """
    question_id = scrapy.Field()        # 问题 id
    answer_url = scrapy.Field()         # 回答链接
    answer_id = scrapy.Field()          # 回答 id
    author_id = scrapy.Field()          # 回答者 id
    author_name = scrapy.Field()        # 回答者昵称
    author_gender = scrapy.Field()      # 回答者性别 1 2
    answer_content = scrapy.Field()     # 回答内容
    praise_num = scrapy.Field()         # 点赞数
    comments_num = scrapy.Field()       # 评论数
    create_time = scrapy.Field()        # 创建时间
    update_time = scrapy.Field()        # 更新时间
    crawl_time = scrapy.Field()         # 爬取时间

    def get_insert_sql(self):
        """
        构造知乎 answer 表的 sql
        """
        # 将 timestamp 秒数转换成时间
        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)

        insert_sql = "insert into zhihu_answer(question_id, answer_url, answer_id, author_id, author_name, " \
                     "author_gender, answer_content, praise_num, comments_num, create_time, update_time, " \
                     "crawl_time, crawl_update_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                     "ON DUPLICATE KEY UPDATE answer_content=answer_content, " \
                     "praise_num=praise_num, comments_num=comments_num, update_time=update_time "
        params = (self["question_id"], self["answer_url"], self["answer_id"], self["author_id"], self["author_name"],
            self["author_gender"], self["answer_content"], self["praise_num"], self["comments_num"],
            create_time, update_time, self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
            datetime.datetime.now().strftime(SQL_DATE_FORMAT))

        return insert_sql, params
