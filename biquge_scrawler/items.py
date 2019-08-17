# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # This is a BookItem represent a book main page.
    bookname = scrapy.Field()
    authname = scrapy.Field()
    category = scrapy.Field()
    updatetm = scrapy.Field()
    introduc = scrapy.Field()
