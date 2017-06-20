# -*- encoding:utf-8 -*-

from Rule import *
from Handler import *


__metaclass__ = type


class Parser:
    """
    read a text file, applying rules and controlling a handler
    对文件进行语法分析，添加规则，添加过滤器
    """
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_filter(self, pattern, name):
        def mfilter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(mfilter)

    def parse(self, filename):
        mfile = open(filename, 'r')
        self.handler.start('document', filename)
        for block in blocks(mfile):
            for m_filter in self.filters:
                block = m_filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.actions(block, self.handler)
                    if last:
                        break
        self.handler.end('document')    # end func parse
        mfile.close()


class BasicTextParser(Parser):
    """
    在构造函数中添加规则和过滤器的具体语法分析器
    """
    def __init__(self, handler):
        super(BasicTextParser, self).__init__(handler)
        self.add_rule(HeadlineRule())
        self.add_rule(TitleRule())
        self.add_rule(ListRule())       # ListRule必须要在ListItemRule前面加入到规则序列中，因为 ListRule 是 ListItemRule
                                        # 的子集，且依赖于 ListItemRule 出现
        self.add_rule(ListItemRule())
        self.add_rule(ParagraphRule())

        self.add_filter(r'\*([^*]+?)\*[^\*]', 'emphasis')           # _斜体* 这种情况无效
        self.add_filter(r'_([^_]+?)_[^_]', 'emphasis')
        self.add_filter(r'(http[s]://[a-zA-Z0-9/\.\-]+)', 'url')    # https://www.baidu.com
        self.add_filter(r'([a-zA-Z0-9\.\-]+@[a-zA-Z0-9\.\-]+)', 'mail')     # mblrwuzy@gmail.com
        self.add_filter(r'[\*]{2}(.+?)[\*]{2}', 'bold')             # ___BOLD*** 这种情况无效
        self.add_filter(r'[_]{2}(.+?)[_]{2}', 'bold')
        self.add_filter(r'(\[)(.*)(\])(\()(.*)(\))', 'url_md')      # [hyper link](https://test.com)
        self.add_filter(r'(!\[)(.*)(\])(\()([a-zA-Z0-9/_:\.\-]+)([ ]*.*)(\))', 'image_md')  # ![img1](img_link)
        self.add_filter(r'`(.*?)`', 'code_md')


handler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse('file1.md')