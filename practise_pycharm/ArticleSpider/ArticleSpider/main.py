# -*- encoding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os

print(os.path.abspath(__file__))
print(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])

execute(["scrapy", "crawl", "zhihu"])