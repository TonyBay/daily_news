# -*- coding: utf-8 -*-
import scrapy
import time
from NewsSpider.items import NewsItem


class QdailySpider(scrapy.Spider):
    name = 'qdaily'
    call = '好奇心日报'
    allowed_domains = ['qdaily.com']
    start_urls = ['http://www.qdaily.com/']

    def parse(self, response):

        for new in response.xpath('//div[@class="packery-container articles"]/div'):
            try:
                if new.xpath('.//span[@class="smart-date"]/@data-origindate').extract()[0].split(' ')[0] != time.strftime("%Y-%m-%d", time.localtime()):
                    break
                if new.xpath('.//h3/text()').extract()[0].find('大公司头条') != -1:
                    yield scrapy.Request(
                        url='http://www.qdaily.com' + new.xpath('.//a/@href').extract()[0],
                        callback=self.page
                    )
                    break
            except:
                pass

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
            yield item