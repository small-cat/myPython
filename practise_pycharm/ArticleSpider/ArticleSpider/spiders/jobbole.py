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
        print(tags)

        cpyrights = response.xpath("//div[@class='copyright-area']/*/text()").extract()
        content = response.xpath("//div[@id='cnblogs_post_body']/*/text()").extract()

        pass
