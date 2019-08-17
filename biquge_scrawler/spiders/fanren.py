# -*- coding: utf-8 -*-
import scrapy
import urllib
import html
import re
from biquge_scrawler.items import BookItem


class CommonSpider(scrapy.Spider):
    name = 'biquge_scrawler'

    def __init__(self):
        self._debug = True
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


class FanrenSpider(CommonSpider):
    name = 'fanren'
    allowed_domains = ['www.biquge.info']
    start_urls = ['https://www.biquge.info/22_22533/']

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)

        # debug
        # print('Main page URL: {}'.format(response.url))
        self.page_2_local(response)

        # xpath for book main page
        x_maininfo = response.xpath(
            '''//div[@class='box_con']/div[@id='maininfo']''')
        assert isinstance(x_maininfo, scrapy.selector.SelectorList)
        x_info = x_maininfo.xpath('''./div[@id='info']''')
        assert isinstance(x_info, scrapy.selector.SelectorList)
        x_bookname = x_info.css('''h1::text''')
        x_attribut = x_info.css('''p::text''')
        assert isinstance(x_info, scrapy.selector.SelectorList)
        assert isinstance(x_info, scrapy.selector.SelectorList)
        x_introduc = x_maininfo.css('''div[id=intro] p::text''')
        assert isinstance(x_introduc, scrapy.selector.SelectorList)

        # generate Item
        itm = BookItem()
        itm['bookname'] = html.unescape(x_bookname.extract_first().strip())
        itm['introduc'] = html.unescape(x_introduc.extract_first().strip())
        itm['authname'] = ''
        itm['category'] = ''
        itm['updatetm'] = ''

        for _attri in x_attribut.extract():
            _attri = html.unescape(_attri)
            if re.match('''作\\s*者''', _attri):
                itm['authname'] = _attri.split(':', 1)[1].strip()
            elif re.match('''类\\s*别''', _attri):
                itm['category'] = _attri.split(':', 1)[1].strip()
            elif re.match('''最\\s*后\\s*更\\s*新''', _attri):
                itm['updatetm'] = _attri.split(':', 1)[1].strip()

        # print('bookname: {}'.format(itm['bookname']))
        # print('authname: {}'.format(itm['authname']))
        # print('category: {}'.format(itm['category']))
        # print('updatetm: {}'.format(itm['updatetm']))
        # print('introduc: {}'.format(itm['introduc']))

        yield itm

        # xpath for sections
        x_sections = response.css(
            '''div[class=box_con] div[id=list] dl dd a[href*=html]''')
        assert isinstance(x_sections, scrapy.selector.SelectorList)
        x_hrefs = x_sections.css('''a::attr(href)''')
        assert isinstance(x_hrefs, scrapy.selector.SelectorList)

        # first section
        href_1st = x_hrefs.extract_first().strip()
        assert isinstance(href_1st, str) and href_1st

        # crawl first section
        abs_href_1st = response.urljoin(href_1st)
        yield scrapy.Request(abs_href_1st, callback=self.parse_section)

    def parse_section(self, response):
        pass
