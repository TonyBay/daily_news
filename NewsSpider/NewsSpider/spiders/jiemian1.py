# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem


class Jiemian1Spider(scrapy.Spider):
    name = 'jiemian1'
    call = '界面新闻'
    allowed_domains = ['jiemian.com']
    start_urls = ['https://www.jiemian.com/lists/446.html']

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
        for new in response.xpath('//div[@class="article-content"]//a'):
            item['title'] = new.xpath('./text()').extract()[0]
            item['link'] = new.xpath('./@href').extract()[0]
            item['site'] = 'jiemian'
            yield item

