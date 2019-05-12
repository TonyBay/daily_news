# -*- coding: utf-8 -*-
import scrapy
import time
from NewsSpider.items import NewsItem
class SputnikSpider(scrapy.Spider):
    name = 'sputnik'
    call = '俄罗斯卫星通讯社'
    allowed_domains = ['sputniknews.cn']
    start_urls = ['http://sputniknews.cn/politics/']

    def start_requests(self):
        yield scrapy.Request(
            url='http://sputniknews.cn/politics/' + time.strftime("%Y%m%d", time.localtime()),
            callback=self.parse
        )

    def parse(self, response):
        item = NewsItem()
        for new in response.xpath('//div[@class="b-plainlist__info"]'):
            item['title'] = new.xpath('./h2/a/text()').extract()[0]
            item['link'] = 'http://sputniknews.cn' + new.xpath('./h2/a/@href').extract()[0]
            item['site'] = 'sputnik'
            yield item
        try:
            yield scrapy.Request(
                url='http://sputniknews.cn' + response.xpath('//div[@class="b-more"]/a/@data-href').extract()[0],
                callback=self.parse
            )
        except:
            pass
