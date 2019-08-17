# -*- coding: utf-8 -*-
import scrapy
import urllib
import html
import re
from biquge_scrawler.items import BookItem, SectionItem, CloseItem


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


class FanrenSpider(CommonSpider):
    name = 'fanren'
    allowed_domains = ['www.biquge.info']
    start_urls = ['https://www.biquge.info/22_22533/']

    # scrawl main info page
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

    # scrawl every section page
    def parse_section(self, response):
        assert isinstance(response, scrapy.http.Response)

        # debug
        x_title = response.css('''title::text''')
        assert isinstance(x_title, scrapy.selector.SelectorList)
        title = x_title.extract_first()
        # print('Section page Title:{}, URL: {}'.format(title, response.url))
        self.page_2_local(response)

        # content xpath
        x_content = response.css('''div[class=content_read]''')
        assert isinstance(x_content, scrapy.selector.SelectorList)
        x_section_name = x_content.css('''div[class=bookname] h1::text''')
        assert isinstance(x_section_name, scrapy.selector.SelectorList)
        x_section_data = x_content.css('''div[id=content]::text''')
        assert isinstance(x_section_data, scrapy.selector.SelectorList)
        x_section_bottems = x_content.css('''div[class=bottem] a''')
        assert isinstance(x_section_bottems, scrapy.selector.SelectorList)

        itm = SectionItem()
        itm['section_name'] = x_section_name.extract_first()
        itm['section_data'] = '\r\n'.join(x_section_data.extract())

        yield itm

        # extract next section URL
        href_section_next = ''
        for _x_bottem in x_section_bottems:
            assert isinstance(_x_bottem, scrapy.selector.Selector)
            button = _x_bottem.css('''a::text''').extract_first()
            href = _x_bottem.css('''a::attr(href)''').extract_first()
            if re.match('下\\s*一\\s*章', button):
                href_section_next = href
                break

        if href_section_next is None:
            yield CloseItem()
            pass
            print('{} Extrace href section None'.format(title))
        elif len(href_section_next) == 0:
            yield CloseItem()
            pass
            print('{} Extrace href section len is 0'.format(title))
        elif href_section_next.endswith('/'):
            yield CloseItem()
            pass
            print('{} This is the last one section.'.format(title))
        else:
            href_section_next = response.urljoin(href_section_next)
            yield scrapy.Request(href_section_next, callback=self.parse_section)
