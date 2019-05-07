# -*- coding: utf-8 -*-

import scrapy
from NewsSpider.items import NewsItem

class GuanchaSpider(scrapy.Spider):
    name = 'guancha'
    call = '观察者'
    allowed_domains = ['guancha.cn']
    start_urls = ['https://www.guancha.cn/GuanChaZheTouTiao/list_1.shtml']

    def parse(self, response):
        item = NewsItem()
        time = response.xpath('//div[@class="content-headline"]/div/span/text()').extract()[0].split(' ')[0]
        for new in response.xpath('//div[@class="content-headline"]'):
            try:
                news_time = new.xpath('./div/span/text()').extract()[0].split(' ')
                if news_time[0] != time:
                    break
                item['title'] = new.xpath('./h3/a/text()').extract()[0]
                item['link'] = 'https://www.guancha.cn' + new.xpath('./h3/a/@href').extract()[0]
                item['site'] = 'guancha'
                yield item
            except:
                pass