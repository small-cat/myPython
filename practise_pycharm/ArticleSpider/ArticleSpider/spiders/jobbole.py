# -*- coding: utf-8 -*-
import scrapy

__author__ = "Sholegance (mblrwuzy@gmail.com)"
__date__ = ""
__status__ = ""
__version__ = ""

__metaclass__ = type


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        pass
