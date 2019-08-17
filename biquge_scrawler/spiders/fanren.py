# -*- coding: utf-8 -*-
import scrapy


class FanrenSpider(scrapy.Spider):
    name = 'fanren'
    allowed_domains = ['www.biquge.info']
    start_urls = ['https://http://www.biquge.info/22_2253/']

    def parse(self, response):
        pass
