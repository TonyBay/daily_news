# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class DBPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            db='news',
            user='root',
            passwd='vertycal29'
        )
        # 数据库游标，用于操作数据库
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("INSERT INTO new(title,link,tag,site,time) VALUES (%s,%s,%s,%s,%s)",(item['title'],item['link'],item['tag'],item['site'],item['time']))
            self.connect.commit()
        except Exception as e:
            print(e)

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

class NewsPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item



