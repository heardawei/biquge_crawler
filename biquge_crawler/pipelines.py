# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from biquge_crawler.items import BookMainItem, BookDircItem, BookSectionItem, BookCloseItem


def to_utf8_bytes(str):
    return str.replace('\xa0', '').encode()


class BookPipeline(object):
    def __init__(self):
        # All books stream store here, key is : item['track']
        self.opened_books = {}

    def process_item(self, item, spider):
        assert isinstance(item, scrapy.Item)

        if isinstance(item, BookSectionItem):
            fd = self.opened_books[item['track']]
            fd.write(to_utf8_bytes(item['section_name']))
            fd.write(to_utf8_bytes('\r\n'))
            for _line in item['section_data']:
                fd.write(to_utf8_bytes(_line))
                fd.write(to_utf8_bytes('\r\n'))

        elif isinstance(item, BookDircItem):
            fd = self.opened_books[item['track']]
            a = type(item['sections'])
            print('{} {}'.format(a, len(item['sections'])))
            for _section_name in item['sections']:
                fd.write(to_utf8_bytes(_section_name))
                fd.write(to_utf8_bytes('\r\n'))

        elif isinstance(item, BookMainItem):
            bookname = item['bookname'] + '.txt'
            fd = open(bookname, 'wb')
            fd.write(to_utf8_bytes(item['bookname']))
            fd.write(to_utf8_bytes('\r\n'))
            fd.write(to_utf8_bytes(item['introduc']))
            fd.write(to_utf8_bytes('\r\n'))
            fd.write(to_utf8_bytes(item['authname']))
            fd.write(to_utf8_bytes('\r\n'))
            fd.write(to_utf8_bytes(item['category']))
            fd.write(to_utf8_bytes('\r\n'))
            fd.write(to_utf8_bytes(item['updatetm']))
            fd.write(to_utf8_bytes('\r\n'))
            fd.write(to_utf8_bytes(item['lastsect']))
            fd.write(to_utf8_bytes('\r\n'))

            self.opened_books[item['track']] = fd

        elif isinstance(item, BookCloseItem):
            self.opened_books.pop(item['track']).close()

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
