# -*- coding: utf-8 -*-
import scrapy
import time
from NewsSpider.items import NewsItem

class WscSpider(scrapy.Spider):
    name = 'wsc'
    call = '华尔街见闻'
    allowed_domains = ['wallstreetcn.com']
    start_urls = ['https://wallstreetcn.com/themes/1005119']

    def parse(self, response):
        for new in response.xpath('//div[@class="group-item"]'):
            if new.xpath('.//time/text()').extract()[0].split('，')[0].find(time.strftime("%m月%d日", time.localtime())) == -1:
                break
            yield scrapy.Request(
                url='https://wallstreetcn.com' + new.xpath('.//a/@href').extract()[0],
                callback=self.page
            )


    def page(self,response):
        item = NewsItem()
        for new in response.xpath('//div[@class="rich-text"]/p[@align]//a'):
            title = ''
            for text in new.xpath('.//text()').extract():
                title += text
            item['title'] = title
            try:
                item['link'] = new.xpath('./@href').extract()[0]
            except:
                item['link'] = response.url
            item['site'] = 'wsc'
            yield item
