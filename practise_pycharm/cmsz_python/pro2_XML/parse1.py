# -*- encoding: utf-8 -*-
__metaclass__ = type

from xml.sax.handler import ContentHandler
from xml.sax import parse


class HeadlineHandler(ContentHandler):
    def __init__(self):
        # in python2.x, there will cause an error: TypeError, type , not class object
        super(HeadlineHandler, self).__init__()
        self.data = []
        self.headlines = []
        self.in_headline = False

    def startElement(self, name, attrs):
        if name == 'h1':
            self.in_headline = True
            print(attrs.items())

    def endElement(self, name):
        if name == 'h1':
            text = ''.join(self.data)
            self.data = []
            self.headlines.append(text)
            self.in_headline = False

    def characters(self, content):
        if self.in_headline:
            self.data.append(content)

    def getHeadlines(self):
        return self.headlines

if __name__ == '__main__':
    headlineHandler = HeadlineHandler()
    parse('website.xml', headlineHandler)

    for h in headlineHandler.getHeadlines():
        print(h)
