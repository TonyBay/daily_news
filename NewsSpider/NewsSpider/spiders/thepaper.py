# -*- coding: utf-8 -*-
import scrapy


class ThepaperSpider(scrapy.Spider):
    name = 'thepaper'
    allowed_domains = ['pp.com']
    start_urls = ['http://pp.com/']

    def parse(self, response):
        pass
