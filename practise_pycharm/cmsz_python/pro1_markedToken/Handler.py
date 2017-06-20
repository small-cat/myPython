# -*- encoding:utf-8 -*-
__metaclass__ = type

import re

# ----------- Processor --------------


class Handler:
    """
    define function: start, end, sub
    """

    def __init__(self):
        pass

    def callback(self, prefix, name, *args):
        """
        call back, get attribute prefix_name, and return return
        result of prefix_name called
        """
        method = getattr(self, prefix+name, None)   # get attribute prefix_name

        # in python 3.x, can not use callable, do as follows:
        # if hasattr(method, '__call__'): return method(*args)
        if callable(method):
            return method(*args)

    def start(self, name, *args):
        self.callback('start_', name, *args)

    def end(self, name, *args):
        self.callback('end_', name, *args)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                return match.group(0)   # endif
            return result       # end function substitution
        return substitution     #end function sub


class HTMLRenderer(Handler):
    """
    implementations of every marked token
    """
    def __init__(self):
        super(HTMLRenderer, self).__init__()
        pass        # do something next

    def start_paragraph(self):
        print "<p>"

    def end_paragraph(self):
        print "</p>"

    def start_headline(self, level):
        """
        level of headline
        :param level:  1 - h1, 2 - h2, 3 - h3
        """
        if level == 1:
            print "<h1>",
        elif level == 2:
            print "<h2>",
        elif level == 3:
            print "<h3>",
        elif level == 4:
            print "<h4>",
        else:
            raise Exception("wrong level of headline")

    def end_headline(self, level):
        if level == 1:
            print "</h1>"
        elif level == 2:
            print "</h2>"
        elif level == 3:
            print "</h3>"
        elif level == 4:
            print "</h4>"
        else:
            raise Exception("wrong level of headline")

    def start_document(self, filename):
        """
        HTML 文件的名称，作为原文本文件名
        """
        print '<!DOCTYPE html><html><head><title>%s</title>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>' % filename

    def end_document(self):
        """
        HTML 文件的结束
        """
        print "</body></html>"

    def start_list(self):
        print "<ul>"

    def end_list(self):
        print "</ul>"

    def start_listitem(self):
        print "<li>",

    def end_listitem(self):
        print "</li>"

    def start_title(self):
        print "<title>",

    def end_title(self):
        print "</title>"

    def sub_url(self, match):
        return "<a href=%s>%s</a>" % (match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))

    def sub_emphasis(self, match):
        return "<em>%s</em>" % match.group(1)

    def feed(self, data):
        print data,

    # TODO: continue to implement func: image, table, bold, code, hyperlink

    def sub_bold(self, match):
        return '<strong>%s</strong>' % match.group(1)

    def sub_url_md(self, match):
        return '<a href="%s>%s</a>' % (match.group(5), match.group(2))      # [hyper link](https://test.com)

    def sub_image_md(self, match):
        return '<img src="%s" alt="%s" title="%s"/>' % (match.group(5), match.group(2), match.group(6))

    def sub_code_md(self, match):
        return '<code>%s</code>' % match.group(1)


if __name__ == '__main__':
    handler = HTMLRenderer()
    print re.sub(r'\*([^*]+?)\*[^\*]', handler.sub('emphasis'), '*This* *is* a ***test***')
    print re.sub(r'[\*]{3}([^*]+?)[\*]{3}', handler.sub('bold'), 'This *is* a ***test***')
    print re.sub(r'(http[s]://[a-z0-9/\.\-]*)', handler.sub('url'), 'baidu(https://www.baidu.com you know?')
    print re.sub(r'(http[s]://[a-z0-9/\.\-]*)', handler.sub('url'), 'https://www.baidu.com')
    print re.sub(r'([a-zA-Z0-9\.]+@[a-zA-Z0-9\.]+)', handler.sub('mail'), 'plz mail to mblrwuzy@gmail.com, thanks')
    print re.sub(r'(\[)(.*)(\])(\()(.*)(\))', handler.sub('url_md'), '[hyper link](https://test.com)')
    print re.sub(r'(!\[)(.*)(\])(\()([a-zA-Z0-9/_:\.\-]+)([ ]*.*)(\))', handler.sub('image_md'),
                 '![image1](https://www.baidu.com/image00001.png "dsadsadsdas")')
    print re.sub(r'(!\[)(.*)(\])(\()([a-zA-Z0-9/_:\.\-]+)([ ]*.*)(\))', handler.sub('image_md'),
                 '![image1](https://www.baidu.com/image00001.png)')
    print re.sub(r'`(.*?)`', handler.sub('code_md'), '`int a = 0``dsadsa`')