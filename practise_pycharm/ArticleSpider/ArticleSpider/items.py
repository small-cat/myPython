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
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def get_nums(value):
    """
    通过正则表达式获取 评论数，点赞数和收藏数
    """
    re_match = re.match(".*?(\d+).*", value)
    if re_match:
        nums = (int)(re_match.group(1))
    else:
        nums = 0

    return nums


def get_date(value):
    re_match = re.match("([0-9/]*).*", value)
    if re_match:
        create_date = re_match.group(1)


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
        input_processor = MapCompose(get_date)
    )
    url = scrapy.Field()            # 文章路径
    front_img_url_download = scrapy.Field(    # 文章封面图片路径,用于下载，赋值时必须为数组形式
        # 默认 output_processor 是 TakeFirst()，这样返回的是一个字符串，不是 list，此处必须是 list
        # 修改 output_processor
        output_processor = MapCompose(return_value)
    )
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field() # 保存图片路径（本地路径）
    fav_nums = scrapy.Field(        # 收藏数
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(    # 评论数
        input_processor=MapCompose(get_nums)
    )
    vote_nums = scrapy.Field(       # 点赞数
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(           # 标签分类 label
        # 本身就是一个list, 输出时，将 list 以 commas 逗号连接
        input_processor = MapCompose(remove_comment_tag),
        output_processor = Join(",")
    )
    content = scrapy.Field(        # 文章内容
        # content 我们不是取最后一个，是全部都要，所以不用 TakeFirst()
        output_processor=Join("")
    )
    object_id = scrapy.Field()      # 文章内容的md5的哈希值，能够将长度不定的 url 转换成定长的序列


class ArticleItemLoader(ItemLoader):
    """
    自定义 ItemLoader, 就相当于一个容器
    """
    # 这里表示，输出获取的 ArticleItemLoader 提取到的值，都是 list 中的第一个值
    # 如果有的默认不是去第一个值，就在 Field() 中进行修改
    default_output_processor = TakeFirst()