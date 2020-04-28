# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from MpSpider import settings
import pymysql
import logging

logger = logging.getLogger(__name__)


class MpspiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'sa_spider':

            print('ITEM', item, spider.name)

        return item



class DogPipeline(object):
    def process_item(self, item, spider):
        print('ITEM', item, spider.name)
        self.cursor.execute('show tables')
        for i in self.cursor.fetchall():
            print(i)
        return item


    def saveArticle(self):
        sql = '''
        insert into article ()
        '''


    def open_spider(self, spider):
        logger.info(settings.MYSQL_SETTINGS)
        self.conn = pymysql.Connection(**settings.MYSQL_SETTINGS)
        self.cursor = self.conn.cursor()


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

