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
import codecs
import json
import MySQLdb


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

    def spider_close(self):
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
        self.conn = MySQLdb.connect('localhost', 'spider', 'wuzhenyu', 'article_spider', charset="utf8",
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