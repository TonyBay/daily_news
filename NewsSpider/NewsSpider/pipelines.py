# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymysql


class DBPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            db='news',
            user='root',
            passwd='vertycal29'
        )
        self.cursor = self.connect.cursor()
        sql = """CREATE TABLE NEW( 
                 TITLE VARCHAR(300) NOT NULL, 
                 LINK VARCHAR(300) NOT NULL,
                 SITE VARCHAR(80) NOT NULL
                 )ENGINE=InnoDB DEFAULT CHARSET=utf8"""
        self.cursor.execute("DROP TABLE IF EXISTS NEW")
        self.cursor.execute(sql)

    def process_item(self, item, spider):
        sql = "INSERT INTO NEW(TITLE, LINK, SITE) \
               VALUES ('%s', '%s', '%s')" % \
              (item['title'],item['link'],item['site'])
        try:
            self.cursor.execute(sql)
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

class MdPipeline(object):

    def __init__(self):
        self.file = open('today_news.md','w')
        self.file.write('## '+time.strftime('%m/%d', time.localtime())+'\n\n')
        self.file.close()

    def open_spider(self, spider):
        head = spider.call
        self.file = open('today_news.md','a')
        self.file.write('### '+head+'\n')

    def process_item(self, item, spider):
        self.file.write('['+item['title']+']('+item['link']+')'+'\n\n')
        return item

    def close_spider(self,spider):
        self.file.close()