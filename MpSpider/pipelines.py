# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MpspiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'sa_spider':

            print('ITEM', item, spider.name)

        return item



class DogPipeline(object):
    def process_item(self, item, spider):
        # print('ITEM', item, spider.name)
        return item
