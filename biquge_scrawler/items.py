# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookTraceItem(scrapy.Item):
    # This item contains a track-flag convience for find book context.
    track = scrapy.Field()


class BookMainItem(BookTraceItem):
    # This item represent a book main page.
    bookname = scrapy.Field()
    authname = scrapy.Field()
    category = scrapy.Field()
    updatetm = scrapy.Field()
    introduc = scrapy.Field()


class BookSectionItem(BookTraceItem):
    # This item represent a section content.
    section_name = scrapy.Field()
    section_data = scrapy.Field()


class BookCloseItem(BookTraceItem):
    # This item represent a book reach ends.
    book_end = scrapy.Field()
