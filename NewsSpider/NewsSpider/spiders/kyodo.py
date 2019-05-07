# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem

class KyodoSpider(scrapy.Spider):
    name = 'kyodo'
    call = '共同社'
    allowed_domains = ['china.kyodonews.net']
    start_urls = ['https://china.kyodonews.net/kyodo_news?page=1']

    def parse(self, response):
        item = NewsItem()
        time = response.xpath('//ul[@id="js-postListItems"]/li/p/text()').extract()[0].split('-')[0]
        for new in response.xpath('//ul[@id="js-postListItems"]/li'):
            try:
                news_time = new.xpath('./p/text()').extract()[0].split('-')
                if news_time[0] != time:
                    break
                title = new.xpath('.//h3/text()').extract()[0]
                if title.find('详讯') != -1 or title.find('独家') != -1:
                    item['title'] = title
                    item['link'] = 'https://china.kyodonews.net' + new.xpath('./a/@href').extract()[0]
                    item['site'] = 'kyodo'
                    yield item
            except:
                pass
        if response.xpath('//ul[@id="js-postListItems"]/li/p/text()').extract()[-2].split('-')[0] == time:
            yield scrapy.Request(
                url=response.url[:-1] + str(int(response.url[-1]) + 1),
                callback=self.parse
            )
