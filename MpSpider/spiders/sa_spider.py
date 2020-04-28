# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.loader import ItemLoader as il
from scrapy.spiders import CrawlSpider  # 该类支持只爬取 start_urls 列表中 url
import logging

logger = logging.getLogger(__name__)

class SaspiderSpider(CrawlSpider):  # scrapy.spiders
    name = 'sa_spider'
    allowed_domains = ['sl.marcpoint.com']
    start_urls = ['http://sl.marcpoint.com/monitor/queryMonitorList']
    # start_urls = ['http://dastest.marcpoint.com/wordchart/']
    #  提供账号生成的 token
    temp = 'Hm_lvt_8d0447bcda7403d6e941367e44cbeea8=1576060198; _ga=GA1.2.473392251.1576060199; wyq_jcrb_wyq_jcrb_=8276; oldPath=/favicon.ico; JSESSIONID=8a8f5815-16da-471f-8aac-2a9609c1cb74'
    cookies = {i.split('=')[0]:i.split('=')[1] for i in temp.replace(' ', '').split(';')}

    send_data = {
        'keywordId': '783',
        'monitorTime': '1',
        'monitorStartTime': '',
        'monitorEndTime': '',
        'options': '1',
        'comblineflg': '2',
        'infoOrder': 'Published',
        'sort': '2',
        'isLocationAddress': '-1',
        'cloneWebFlag': '1',
        'matchType': '1',
        'forwardWeibo': '1',
        'origin': '1',
        'queryType': '1',
        'page': '1',
        'pageSize': '50',
        'province': '全国',
        'insideOrOutside': '0',
        'captureWebsiteName': '全部',
        'shortUrlType': '1',
        'certificationType': '1',
        'ocrContentType': '1',
        'weiboHandleType': '0',
        'commentType': '0',
        'accurateSearch': '0',
        'accurateWord': '-1',
        'accurateRegional': '全国',
        'accurateIndustry': '',
        'accurateExcludeRegional': '',
    }

    def start_requests(self):

        yield scrapy.FormRequest(url=self.start_urls[0], method='POST', callback=self.parse, cookies=self.cookies, meta=dict(name='jack'), formdata=self.send_data)


    def parse(self, response):
        # _stat = response.json()['status']
        # _body = response.json()['msg']
        logger.info(response.text)
        x_span = response.xpath("//div[@clase='list-group-item']")
        for span in x_span:
            item = dict()
            logger.warning('nnn')
            item['name'] = span.xpath('./div/label/text()')
            item['value'] = span.xpath('./div/span/span/text()')
            yield item
