# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem
import time

class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['rs']
    start_urls = ['https://cn.reuters.com/news/archive/chinaNews?view=page&page=1',
                  'https://cn.reuters.com/news/archive/CNTopGenNews?view=page&page=1',
                  'https://cn.reuters.com/news/archive/CNIntlBizNews?view=page&page=1']

    def parse(self, response):
        item = NewsItem()
        for new in response.xpath('//div[@class="story-content"]'):
            if new.xpath('.//span[@class="timestamp"]/text()').extract()[0].replace(' ','').find(time.strftime("%d", time.localtime())+'日') == -1:
                break
            item['title'] = new.xpath('.//a/h3/text()').extract()[0].replace('\t','')
            item['link'] = 'https://cn.reuters.com' + new.xpath('.//a/@href').extract()[0]
            yield item
        if response.xpath('//div[@class="story-content"]//span[@class="timestamp"]/text()').extract()[-1].replace(' ','').find(time.strftime("%d", time.localtime())+'日') != -1:
            yield scrapy.Request(
                url=response.url[:-1] + str(int(response.url[-1])+1),
                callback=self.parse
            )
