# -*- coding: utf-8 -*-
import scrapy
import time
from NewsSpider.items import NewsItem

class WscSpider(scrapy.Spider):
    name = 'wsc'
    allowed_domains = ['wallstreetcn.com']
    start_urls = ['https://wallstreetcn.com/themes/1005119']

    def parse(self, response):
        item = NewsItem()
        for new in response.xpath('//div[@class="group-item"]'):
            if new.xpath('.//time/@datetime').extract()[0].split('T')[0] != time.strftime("%Y-%m-%d", time.localtime()):
                break
            yield scrapy.Request(
                url='https://wallstreetcn.com' + new.xpath('.//a/@href').extract()[0],
                callback=self.page
            )


    def page(self,response):
        pass