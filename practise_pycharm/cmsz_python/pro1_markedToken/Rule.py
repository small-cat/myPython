# -*- encoding:utf-8 -*-
__metaclass__ = type
# --------- Rule ------------

from util import *

class Rule:
    """
    define rules to deal with matched block, this is a super class
    """
    def __init__(self):
        self.type = ''

    def actions(self, block, handler):
        if block:
            handler.start(self.type)
            handler.feed(block)
            handler.end(self.type)
            return True


class HeadlineRule(Rule):
    """
    headline rule inherited from Rule
    """
    def __init__(self):
        super(HeadlineRule, self).__init__()
        self.type = 'headline'
        self.level = 0

    def condition(self, block):
        """
        以 # 开头的 block 为标题
        #   一级标题
        ##  二级标题
        ### 三级标题
        ####四级标题
        """
        for s in block:
            if s == '#':
                self.level += 1
            else:
                break
        if self.level == 0:
            return False
        else:
            return self.level

    def actions(self, block, handler):
        """
        去掉 # 和末尾的回车
        """
        handler.start(self.type, self.level)
        handler.feed(strip_enter(block)[self.level:])
        handler.end(self.type, self.level)
        self.level = 0          # 分析器 parser 中的规则都是类对象，这些对象都是重复使用的，使用一次，需要清空一次
        return True


class TitleRule(Rule):
    """
    pass
    """
    def __init__(self):
        super(TitleRule, self).__init__()
        self.type = 'title'

    def condition(self, block): # do nothing
        return False


class ListItemRule(Rule):
    """
    以 ‘-’ 或者 ‘*’ 开始，并且第二个字符是空格的行，是为列表项
    """
    def __init__(self):
        super(ListItemRule, self).__init__()
        self.type = 'listitem'

    def condition(self, block):
        if block[0]=='-' or block[0]=='*':
            if block[1] == ' ':
                return True
        return False

    def actions(self, block, handler):
        """
        需要去除开头的 '-'或者'*', 去掉末尾的 \r, \n
        """

        handler.start(self.type)
        handler.feed(strip_enter(block)[2:])
        handler.end(self.type)
        return True


class ListRule(ListItemRule):
    """
    列表规则:
    列表从第一个列表项的块和最后一个列表项块之间，在最后一个连续列表项之后结束
    """
    def __init__(self):
        super(ListRule, self).__init__()
        self.type = 'list'
        self.inside = False

    def condition(self, block):
        return True

    def actions(self, block, handler):
        if ListItemRule.condition(self, block) and not self.inside:
            # 这是第一个列表项
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            # 这是最后一个列表项
            handler.end(self.type)
            self.inside = False     # endif
        return False        # 此时 block 不是列表项，返回False，继续处理 block，如果返回 True，将不再继续处理 block


class ParagraphRule(Rule):
    """
    段落是其他规则没有覆盖到的块
    """
    def __init__(self):
        super(ParagraphRule, self).__init__()
        self.type = 'paragraph'

    def condition(self, block):
        return True


if __name__ == '__main__':
    from Handler import *
    listItem = ListItemRule()
    handler = HTMLRenderer()
    block = '- hello world'
    if listItem.condition(block):
        listItem.actions(block, handler)