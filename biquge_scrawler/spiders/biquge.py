# -*- coding: utf-8 -*-
import scrapy
import urllib
import html
import re
from biquge_scrawler.items import BookMainItem, BookDircItem, BookSectionItem, BookCloseItem, BookMainItemLoader, BookDircItemLoader, BookSectionItemLoader


class CommonSpider(scrapy.Spider):
    name = 'biquge_scrawler'

    def __init__(self):
        self._debug = False
        pass

    # debug, save pages to disk
    def page_2_local(self, request):
        if not self._debug:
            return

        with open(self.url_2_path(request.url), 'wb') as f:
            f.write(request.body)

    # transform url to a simple filename
    def url_2_path(self, url):
        assert isinstance(url, str)

        scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(
            url)

        # print('urlparse -> {}'.format(
        #     (scheme,netloc,path,params,query,fragment)))

        assert isinstance(scheme, str)
        assert isinstance(netloc, str)
        assert isinstance(path, str)
        assert isinstance(params, str)
        assert isinstance(query, str)
        assert isinstance(fragment, str)

        if path.endswith('/'):
            path += 'index.html'

        netloc = netloc.replace('.', '_').replace(':', '_')
        path = path.replace('\\', '_').replace('/', '_')

        # print('urlparse -> {}'.format(
        #     (scheme,netloc,path,params,query,fragment)))

        return netloc+path


class BiqugeSpider(CommonSpider):
    name = 'biquge'
    allowed_domains = ['www.biquge.info']
    start_urls = ['https://www.biquge.info/22_22533/',      # 凡人修仙传仙界篇
                  'https://www.biquge.info/1_1245/',        # 剑来
                  'https://www.biquge.info/10_10240/',      # 凡人修仙传
                  ]

    # parse main info page
    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)

        # debug
        # print('Main page URL: {}'.format(response.url))
        self.page_2_local(response)

        track = response.url

        # Item Loader
        main_loader = BookMainItemLoader(BookMainItem(), response=response)
        # Using Item Loader to populate items
        main_loader.add_css(
            'bookname', '''div#maininfo>div#info>h1::text''')
        main_loader.add_css(
            'authname', '''div#maininfo>div#info>p:nth-of-type(1)::text''')
        main_loader.add_css(
            'category', '''div#maininfo>div#info>p:nth-of-type(2)::text''')
        main_loader.add_css(
            'updatetm', '''div#maininfo>div#info>p:nth-of-type(3)::text''')
        main_loader.add_css(
            'lastsect', '''div#maininfo>div#info>p:nth-of-type(4)>a:nth-of-type(1)::text''')
        main_loader.add_css(
            'introduc', '''div#maininfo>div#intro>p::text''')
        main_loader.add_value('track', track)

        yield main_loader.load_item()

        # Item Loader
        dirc_loader = BookDircItemLoader(BookDircItem(), response=response)
        # Using Item Loader to populate items
        dirc_loader.add_css(
            'sections', '''div.box_con>div#list>dl>dd>a[href*=html][title]::attr(title)''')
        dirc_loader.add_value('track', track)

        yield dirc_loader.load_item()

        # crawl first section

        # xpath for sections hrefs
        x_href_1st = response.css(
            '''div.box_con>div#list>dl>dd:nth-of-type(1)>a::attr(href)''')
        assert isinstance(x_href_1st, scrapy.selector.SelectorList)

        # first section hrefs
        href_1st = x_href_1st.extract_first().strip()
        assert isinstance(href_1st, str) and href_1st

        abs_href_1st = response.urljoin(href_1st)
        yield scrapy.Request(abs_href_1st, callback=self.parse_section, meta={'track': track})

    # parse section page
    def parse_section(self, response):
        assert isinstance(response, scrapy.http.Response)

        track = response.meta['track']

        # debug
        x_title = response.css('''title::text''')
        assert isinstance(x_title, scrapy.selector.SelectorList)
        title = x_title.extract_first()
        # print('Section page Title:{}, URL: {}'.format(title, response.url))
        self.page_2_local(response)

        # Item Loader
        sect_loader = BookSectionItemLoader(
            BookSectionItem(), response=response)
        # Using Item Loader to populate items
        sect_loader.add_value('track', track)
        sect_loader.add_css(
            'section_name', '''div.content_read div.bookname>h1::text''')
        sect_loader.add_css(
            'section_data', '''div.content_read div#content::text''')

        yield sect_loader.load_item()

        # crawl next section page
        x_next_section_href = response.css(
            '''div.content_read div.bottem>a:nth-of-type(4)::attr(href)''')
        assert isinstance(x_next_section_href, scrapy.selector.SelectorList)

        next_section_href = x_next_section_href.extract_first()

        if next_section_href is None:
            itm = BookCloseItem()
            itm['track'] = track
            yield itm
            pass
            print('{} Extrace href section None'.format(title))
        elif len(next_section_href) == 0:
            itm = BookCloseItem()
            itm['track'] = track
            yield itm
            pass
            print('{} Extrace href section len is 0'.format(title))
        elif next_section_href.endswith('/'):
            itm = BookCloseItem()
            itm['track'] = track
            yield itm
            pass
            print('{} This is the last one section.'.format(title))
        else:
            next_section_href = response.urljoin(next_section_href)
            yield scrapy.Request(next_section_href, callback=self.parse_section, meta={'track': track})
