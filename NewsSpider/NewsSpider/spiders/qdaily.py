# -*- coding: utf-8 -*-
import scrapy
import time
from NewsSpider.items import NewsItem


class QdailySpider(scrapy.Spider):
    name = 'qdaily'
    allowed_domains = ['qdaily.com']
    start_urls = ['http://www.qdaily.com/categories/18.html']

    def parse(self, response):
        for new in response.xpath('//h3[@class]'):
            if new.xpath('ancestor::a//span/@data-origindate').extract()[0].split(' ')[0] != time.strftime("%Y-%m-%d", time.localtime()):
                break
            if new.xpath('./text()').extract()[0].find('大公司头条') != -1:
                yield scrapy.Request(
                    url='http://www.qdaily.com' + new.xpath('ancestor::a/@href').extract()[0],
                    callback=self.page
                )
                break

    def page(self,response):
        item = NewsItem()
        for new in response.xpath('//div[@class="detail"]/p[@line]'):
            title = new.xpath('.//b//text()').extract()
            if title:
                item['title'] = title[0]
            else:
                item['title'] = ''
                for text in new.xpath('.//text()').extract():
                    item['title'] += text.replace(' ','')
            item['link'] = new.xpath('.//a/@href').extract()[0]
            item['site'] = 'qdaily'
            print(item)