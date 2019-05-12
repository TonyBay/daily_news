# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem
import time

class ZaobaoSpider(scrapy.Spider):
    name = 'zaobao'
    call = '南华早报'
    allowed_domains = ['zaobao.com']
    start_urls = ['https://www.zaobao.com/news/china',
                  'https://www.zaobao.com/special/report/politic/cnpol'
                  ]

    def parse(self, response):
        item = NewsItem()
        for new in response.xpath('//div[@class="post-list view-content"]/div/div'):
            if new.xpath('.//span[@class="datestamp"]/text()').extract()[0] != time.strftime("%d/%m/%Y", time.localtime()):
                break
            item['title'] = new.xpath('.//span[@class="post-title"]/text()').extract()[0]
            item['link'] = 'https://www.zaobao.com' + new.xpath('.//a/@href').extract()[0]
            yield item