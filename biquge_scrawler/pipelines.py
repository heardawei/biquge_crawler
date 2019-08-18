# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from biquge_scrawler.items import BookMainItem, BookSectionItem, BookCloseItem


class BookPipeline(object):
    def __init__(self):
        # All books stream store here, key is : item['track']
        self.opened_books = {}

    def process_item(self, item, spider):
        assert isinstance(item, scrapy.Item)

        if isinstance(item, BookMainItem):
            bookname = item['bookname'] + '.txt'
            self.opened_books[item['track']] = open(bookname, 'wb')
        elif isinstance(item, BookSectionItem):
            self.opened_books[item['track']].write(
                item['section_name'].replace('\xa0', '').encode())
            self.opened_books[item['track']].write(
                item['section_data'].replace('\xa0', '').encode())
        elif isinstance(item, BookCloseItem):
            self.opened_books[item['track']].close()
            self.opened_books.pop(item['track'])

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
