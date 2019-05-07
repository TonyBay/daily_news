# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem

class ThecoverSpider(scrapy.Spider):
    name = 'thecover'
    allowed_domains = ['thecover.cn']
    start_urls = ['http://www.thecover.cn/channel_51']

    def parse(self, response):
        item = NewsItem()
        for new in response.xpath('//div[@class="grid-item"]'):
            if new.xpath('.//span[@class="time"]/text()').extract()[0].find('天') != -1:
                break
            item['title'] = new.xpath('.//h2/text()').extract()[0]
            item['link'] = 'http://www.thecover.cn' + new.xpath('./a/@href').extract()[0]
            item['site'] = 'thecover'
            yield item



