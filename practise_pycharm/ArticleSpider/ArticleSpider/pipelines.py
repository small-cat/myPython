# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
与数据存储相关
"""
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

import codecs
import json
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    """
    仅对封面图片进行操作,将图片保存在本地中的路径传递出来
    """
    # 获取图片下载后的保存路径,这个在 settings.py 中进行设置了的
    def item_completed(self, results, item, info):
        """

        :param results: 这是一个list, 由tuple 组成，tuple中第一个元素为True/False,第二个元素为字典，path 为字典中的key，值
        为图片的本地保存路径
        :param item:
        :param info:
        :return:
        """
        img_file_path = ""
        if "front_img_url" in item:
            for ok, value in results:
                img_file_path = value["path"]
            item["front_img_path"] = img_file_path

        return item     # 因为后面还有pipeline 需要接收


class JsonWithEncodingPipeline(object):
    """
    处理 item 数据，保存为json格式的文件中
    """
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'   # False，才能够在处理非acsii编码的时候，不会出错，尤其
        #中文
        self.file.write(lines)
        return item     # 必须 return

    def spider_close(self, spider):
        """
        把文件关闭
        """
        self.file.close()


class JsonExporterPipeline(object):
    """
    scrapy.exporters 提供了几种不同格式的文件支持，能够将数据输出到这些不同格式的文件中，查看 JsonItemExporter 源码即可获知
    __all__ = ['BaseItemExporter', 'PprintItemExporter', 'PickleItemExporter',
           'CsvItemExporter', 'XmlItemExporter', 'JsonLinesItemExporter',
           'JsonItemExporter', 'MarshalItemExporter']，这些就是scrapy 支持的文件
    """
    def __init__(self):
        """
        先打开文件，传递一个文件
        """
        self.file = open('articleexporter.json', 'wb')
        #调用 scrapy 提供的 JsonItemExporter到处json文件
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_close(self, spider):
        """
        close file
        :param spider:
        :return:
        """
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    """
    store item data into mysql
    查阅python mysqldb 的文档
    """
    def __init__(self):
        # 连接数据库
        self.conn = MySQLdb.connect('192.168.0.101', 'spider', 'wuzhenyu', 'article_spider', charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, create_date, url, url_object_id, front_img_url, front_img_path, comment_nums, 
            fav_nums, vote_nums, tags, content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, '%s', '%s')
        """ % (item["title"], item["create_date"], item["url"], item["object_id"],item["front_img_url"],
               item["front_img_path"], item["comment_nums"], item["fav_nums"], item["vote_nums"], item["tags"],
               item["content"])

        # self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["object_id"],
        #                                 item["front_img_url"], item["front_img_path"], item["comment_nums"],
        #                                 item["fav_nums"], item["vote_nums"], item["tags"], item["content"]))
        print(insert_sql)
        self.cursor.execute(insert_sql)
        self.conn.commit()

    def spider_close(self, spider):
        self.cursor.close()
        self.conn.close()


class MysqlTwistedPipeline(object):
    """
    利用 Twisted API 实现异步入库 MySQL 的功能
    Twisted 提供的是一个异步的容器，MySQL 的操作还是使用的MySQLDB 的库
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        被 spider 调用，将 settings.py 传递进来，读取我们配置的参数
        模仿 images.py 源代码中的 from_settings 函数的写法
        """
        # 字典中的参数，要与 MySQLdb 中的connect 的参数相同
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )

        # twisted 中的 adbapi 能够将sql操作转变成异步操作
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用 twisted 将 mysql 操作编程异步执行
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) # handle exceptions

    def handle_error(self, failure, item, spider):
        """
        处理异步操作的异常
        """
        print(failure)

    def do_insert(self, cursor, item):
        """
        执行具体的操作，能够自动 commit
        根据不同的 item，构建不同的sql语句插入到数据库中
        """
        # if item.__class__.__name == "JobboleArticleItem" 这种方法比较死板

        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
