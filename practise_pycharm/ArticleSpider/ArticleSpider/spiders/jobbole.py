# -*- coding: utf-8 -*-
import scrapy
import re

__author__ = "Sholegance (mblrwuzy@gmail.com)"
__date__ = ""
__status__ = ""
__version__ = ""

__metaclass__ = type


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/111600/']

    def parse(self, response):
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0]
        match_re = re.match("([0-9/]*).*", response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip())
        if match_re:
            datetime = match_re.group(1)
        votes = int(response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0])
        match_fav = re.match('.*(\d+).*', response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0])
        if match_fav:
            fav_nums = int(match_fav.group(1))

        print("title:%s, datetime:%s, votes:%d\n" % (title, datetime, votes))
        print("fav_nums: ", fav_nums)

        pass
