# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem
import time

class DuanSpider(scrapy.Spider):
    name = 'rfi'
    call = '法国国际广播电台'
    allowed_domains = ['rfi.fr']
    start_urls = ['http://cn.rfi.fr/last_24h#']

    def parse(self, response):
        item = NewsItem()
        for new in response.xpath('//ul[@id="articleList"]/li'):
            if new.xpath('.//time/@datetime').extract()[0] != time.strftime("%y-%m-%d", time.localtime()):
                break
            item['title'] = new.xpath('.//h3/a/@title').extract()[0]
            item['link'] = 'http://cn.rfi.fr' + new.xpath('.//h3/a/@href').extract()[0]
            item['site'] = 'rfi'
            yield item