# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from biquge_scrawler.items import BookItem, SectionItem, CloseItem


class BookPipeline(object):
    def __init__(self):
        self.opened_books = None

    def process_item(self, item, spider):
        assert isinstance(item, scrapy.Item)

        if isinstance(item, BookItem):
            self.opened_books = open(item['bookname'] + '.txt', 'wb')
        elif isinstance(item, SectionItem):
            self.opened_books.write(
                item['section_name'].replace('\xa0', '').encode())
            self.opened_books.write(
                item['section_data'].replace('\xa0', '').encode())
        elif isinstance(item, CloseItem):
            self.opened_books.close()

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
