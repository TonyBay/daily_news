# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem


class Jiemian2Spider(scrapy.Spider):
    name = 'jiemian2'
    call = '界面新闻'
    allowed_domains = ['jiemian.com']
    start_urls = ['https://www.jiemian.com/lists/459.html',
                  'https://www.jiemian.com/lists/280.html',
                  'https://www.jiemian.com/lists/426.html',
                  'https://www.jiemian.com/lists/430.html',
                  'https://www.jiemian.com/lists/431.html',
                  'https://www.jiemian.com/lists/428.html',
                  'https://www.jiemian.com/lists/175.html',]

    def parse(self, response):
        for new in response.xpath('//div[@class="news-view left card"]'):
            time = new.xpath('.//span[@class="date"]/text()').extract()[0]
            if time.find('今天') == -1:
                break
            yield scrapy.Request(
                url=new.xpath('.//h3/a/@href').extract()[0],
                callback=self.page
            )


    def page(self, response):
        item = NewsItem()
        for new in response.xpath('//div[@class="article-main"]//h3/text()').extract():
            item['title'] = new
            item['link'] = response.url
            item['site'] = 'jiemian'
            yield item

