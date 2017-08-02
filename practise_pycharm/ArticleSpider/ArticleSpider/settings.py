# -*- coding: utf-8 -*-

# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
import sys

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArticleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True 一般这个设置为 false
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# 在 scrapy engine 与 downloader 中间就是 downloader middleware
DOWNLOADER_MIDDLEWARES = {
    'ArticleSpider.middlewares.MyCustomDownloaderMiddleware': None,
    'ArticleSpider.middlewares.RandomUserAgentMiddleWare': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES 这个参数，配置是一些类名，ITEM 传递到pipelines 时会经过这个类
# 在下面配置了一个 ImagesPipeline 这个类，是 pipelines 提供的能够用于下载图片的类
# 类后面接的数字，表示的是 ITEM 流经这个类的顺序，数字越小，该类就越早处理 ITEM 对象
ITEM_PIPELINES = {
  # 'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
  # 'scrapy.pipelines.images.ImagesPipeline': 1,
  # 'ArticleSpider.pipelines.ArticleImagePipeline': 1,
  # 'ArticleSpider.pipelines.JsonWithEncodingPipeline': 2,
  # 'ArticleSpider.pipelines.JsonExporterPipeline':2,
  # 'ArticleSpider.pipelines.MysqlPipeline': 2,
  'ArticleSpider.pipelines.MysqlTwistedPipeline': 2,
}

# 在 ITEM_PIPELINES 配置图片类之后，下载图片的话，还需要配置 ITEM 中哪一个字段是图片的URL，存放在什么地方
# 图片下载操作，需要 module PIL, pip install pillow
IMAGES_URLS_FIELD = "front_img_url_download"     # ITEM 中的图片 URL，用于下载
# 注意： 此处对 ITEM中的 front_img_url 这个参数的值，要求是数组形式，否则，
# 就会出现错误 ValueError: Missing scheme in request url: h， 在 parse() 函数中赋值的时候，就以数组的形式进行赋值
PROJECT_IMAGE_PATH = os.path.abspath(os.path.dirname(__file__))   # 获取当前文件所在目录
IMAGES_STORE = os.path.join(PROJECT_IMAGE_PATH, "images")         # 下载图片的保存位置

# 设置路径，将当前项目路径加入到 PYTHON_HOME 环境变量中

# 对下在的图片进行过滤，最小为 100*100
# IMAGES_MIN_HEIGHT = 100
# IMAGES_MIN_WIDTH = 100

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MySQL params
MYSQL_HOST = "192.168.0.101"
MYSQL_DBNAME = "article_spider"
MYSQL_USER = "spider"
MYSQL_PASSWORD = "wuzhenyu"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

# user_agent_list = []
RANDOM_UA_TYPE = "random"