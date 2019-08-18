# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity


class BookTraceItem(scrapy.Item):
    # This item contains a track-flag convience for find book context.
    track = scrapy.Field()


class BookMainItem(BookTraceItem):
    # This item represent a book main page.
    bookname = scrapy.Field()
    authname = scrapy.Field()
    category = scrapy.Field()
    updatetm = scrapy.Field()
    lastsect = scrapy.Field()
    introduc = scrapy.Field()


class BookDircItem(BookTraceItem):
    # This item represent a book sections list page.
    sections = scrapy.Field()


class BookSectionItem(BookTraceItem):
    # This item represent a section content.
    section_name = scrapy.Field()
    section_data = scrapy.Field()


class BookCloseItem(BookTraceItem):
    # This item represent a book reach ends.
    book_end = scrapy.Field()


class BookMainItemLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    pass


class BookDircItemLoader(scrapy.loader.ItemLoader):
    track_out = TakeFirst()
    sections_out = Identity()
    pass


class BookSectionItemLoader(scrapy.loader.ItemLoader):
    default_output_processor = TakeFirst()
    section_data_out = Identity()
    pass
