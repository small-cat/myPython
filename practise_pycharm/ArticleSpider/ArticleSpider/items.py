# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
"""
定义数据保存的格式
"""

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleItem(scrapy.Item):
    """
    定义自己的 Item 类
    """
    title = scrapy.Field()          # Field()能够接收和传递任何类型的值,类似于字典的形式
    create_date = scrapy.Field()    # 创建时间
    url = scrapy.Field()            # 文章路径
    front_img_url = scrapy.Field()  # 文章封面图片路径
    front_img_path = scrapy.Field() # 保存图片路径（本地路径）
    fav_nums = scrapy.Field()       # 收藏数
    comment_nums = scrapy.Field()   # 评论数
    vote_nums = scrapy.Field()      # 点赞数
    tags = scrapy.Field()           # 标签分类 label
    cpyrights = scrapy.Field()      # 版权，著作人相关信息
    content = scrapy.Field()        # 文章内容

