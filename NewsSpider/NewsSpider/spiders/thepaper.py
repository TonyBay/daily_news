# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem
from scrapy.spiders.crawl import Rule, CrawlSpider

class ThePaperSpider(CrawlSpider):
    name = 'thepaper'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://www.thepaper.cn/list_25462',
                  'https://www.thepaper.cn/list_25490',
                  'https://www.thepaper.cn/list_25423',
                  'https://www.thepaper.cn/list_25426',
                  'https://www.thepaper.cn/list_25424',
                  'https://www.thepaper.cn/list_25463',
                  'https://www.thepaper.cn/list_25428',
                  'https://www.thepaper.cn/list_25429',
                  'https://www.thepaper.cn/list_25427',
                  'https://www.thepaper.cn/list_25438'
                  ]

    def parse(self, response):
        if response.xpath('//div[@class="list_logo"]//img/@alt').extract():
            node_id = response.selector.re(r'load_index\.jsp\?nodeids=[0-9]*')[0]
            yield scrapy.Request(
                url='https://www.thepaper.cn/{}&topCids=&pageidx=1'.format(node_id),
                callback=self.page,
            )

    def page(self, response):
        item = NewsItem()
        for new in response.xpath('//div[@class="news_li"]'):
            if new.re(r'<span class="trbszan">'):
                if new.re(r'[0-9]{1,2}小时前|[0-9]{1,2}分钟前'):
                    item['title'] = new.xpath('.//h2/a/text()').extract()[0]
                    item['link'] = 'https://www.thepaper.cn/' + new.xpath('.//a/@href').extract()[0]
                    item['site'] = 'thepaper'
                    yield item
        if len(response.selector.re(r'[0-9]{1,2}小时前|[0-9]{1,2}分钟前')) == 20:
            yield scrapy.Request(
                url=response.url[:-1] + str(int(response.url[-1]) + 1),
                callback=self.page,
            )
