# -*- coding: utf-8 -*-
import scrapy
from NewsSpider.items import NewsItem
import re
import json
import time

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/org/liang-zi-wei-48/activities',
                  'https://www.zhihu.com/org/ji-qi-zhi-xin-65/activities',
                  'https://www.zhihu.com/org/tian-yan-cha-40/activities',
                  'https://www.zhihu.com/org/chu-le-75/activities',
                  'https://www.zhihu.com/org/zhi-shi-fen-zi-68-1/activities',
                  'https://www.zhihu.com/org/you-yan-she-47/activities',
                  'https://www.zhihu.com/org/deeptech-shen-ke-ji/activities',
                  'https://www.zhihu.com/org/ai-fan-er-85/activities',
                  'https://www.zhihu.com/org/zhong-guo-ke-pu-bo-lan/activities',
                  'https://www.zhihu.com/org/100offer/activities'
                  ]

    def parse(self, response):
        id = re.findall(r'session_id=[0-9]*',response.text)[0]
        author = (response.url.split('/')[-2])
        yield scrapy.Request(
            url='https://www.zhihu.com/api/v4/members/'+ author +'/activities?limit=7&'+id+'&desktop=True',
            callback=self.page
        )


    def page(self,response):
        item = NewsItem()
        js = json.loads(response.text)
        for post in js['data']:
            try:
                if time.localtime(post['created_time']).tm_yday != time.localtime(time.time()).tm_yday:
                    break
                if post['action_text'] == '发表了文章':
                    item['title'] = post['target']['title']
                    item['link'] = 'https://zhuanlan.zhihu.com/p/' + str(post['target']['id'])
                    item['site'] = 'zhihu'
                    yield item
            except:
                pass
        if time.localtime(js['data'][-1]['created_time']).tm_yday == time.localtime(time.time()).tm_yday:
            yield scrapy.Request(
                url=js['paging']['next'],
                callback=self.page
            )