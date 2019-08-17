# -*- coding: utf-8 -*-
import scrapy
import urllib


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
        pass
