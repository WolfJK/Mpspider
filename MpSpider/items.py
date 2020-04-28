# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MpspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    database_name = scrapy.Field()
    table_name = scrapy.Field()
    udf = scrapy.Field()
    starttime = scrapy.Field()
    endtime = scrapy.Field()
    _state = scrapy.Field()
    entity_lexicon = scrapy.Field()
    nums = scrapy.Field()

class SaasspiderItem(scrapy.Item):
    info_title = scrapy.Field()
    info_from = scrapy.Field()
    info_location = scrapy.Field()
    info_proper = scrapy.Field()
    info_keywords = scrapy.Field()
    info_nums = scrapy.Field()
    info_date = scrapy.Field()
    info_url = scrapy.Field()
    pinglun = scrapy.Field()
    duanlian = scrapy.Field()

