# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem

class HuxiuSpider(scrapy.Spider):
    name = 'huxiu'
    allowed_domains = ['huxiu.com']
    start_urls = ['https://www.huxiu.com/channel/107.html']

    def parse(self, response):
        for new in response.xpath('//div[@data-aid]'):
            if new.xpath('.//span[@class="time"]/text()').extract()[0].find('天') != -1:
                break
            if new.xpath('.//a[@class="transition"]/@title').extract()[0].find('虎嗅') != -1:
                yield scrapy.Request(
                    url='https://www.huxiu.com' + new.xpath('.//a[@class="transition"]/@href').extract()[0],
                    callback=self.page
                )

    def page(self,response):
        item = NewsItem()
        for new in response.xpath('//div[@class="article-wrap"]//p//a'):
            item['title'] = new.xpath('./text()').extract()[0]
            item['link'] = new.xpath('./@href').extract()[0]
            item['site'] = 'huxiu'
            yield item