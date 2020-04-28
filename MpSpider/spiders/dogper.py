# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.loader import ItemLoader as il
from scrapy.spiders import CrawlSpider  # 该类支持只爬取 start_urls 列表中 url
from scrapy_redis.spiders import RedisSpider
import logging
from MpSpider import settings
from scrapy_redis.utils import bytes_to_str

logger = logging.getLogger(__name__)

# logging.basicConfig(
#             level=logging.WARNING,
#             format='levelname:%(levelname)s , filename: %(filename)s ',
#             datefmt='[%d/%b/%Y %H:%M:%S]',
#             filemode='a'
#            )

class DogSpider(RedisSpider):  # scrapy.spiders
    name = 'dog'
    allowed_domains = ['club.goumin.com']
    # start_urls = ['http://lingdang.goumin.com/v2/thread-index']
    # s = scrapy_redis.get_redis(host='localhost', port=6379, db=0)

    redis_key = 'dog:requests'

    # start_urls = ['http://dastest.marcpoint.com/wordchart/']
    #  提供账号生成的 token
    temp = 'Hm_lvt_8d0447bcda7403d6e941367e44cbeea8=1576060198; _ga=GA1.2.473392251.1576060199; wyq_jcrb_wyq_jcrb_=8276; oldPath=/; JSESSIONID=556950d3-7afe-4992-9ceb-a8b5a5a81079'
    seqnum = 'GMPCBBS1555577562755000'
    data = {"uid": '0', "token": '0', "seqnum": seqnum, "data": {"count": '20', "page": '1'}}
    logger.warning(settings.DEFAULT_REQUEST_HEADERS)

    def start_requests(self):
        logger.warning(json.dumps(self.data))
        for i in range(1, 2 + 1):
            self.data['data']['page'] = str(i)
            logger.info(self.start_urls)
            print('--->', self.data, '<------')
            yield scrapy.Request(url=self.start_urls[0], body=json.dumps(self.data), callback=self.parse, method='POST', dont_filter=True)
            # yield scrapy.FormRequest(url=self.start_urls[0], formdata=self.data, callback=self.parse, method='POST', dont_filter=True)


    def parse(self, response):
        '''处理首页查询的内容'''
        try:
            response_data = json.loads(response.text.replace('for (;;);', '').replace('end;;;', ''))
            for article in response_data['data']['threads']:
                item = dict(
                    acticle_id=article['tid'],
                    acticle_title=article['subject'],
                    acticle_views=article['views'],
                    acticle_replies=article['replies'],
                    acticle_authorid=article['authorid'],
                    acticle_grouptitle=article['grouptitle'],
                    acticle_content_type=article['content_type']
                )
                url = 'http://lingdang.goumin.com/v2/thread/%d' % item['acticle_id']
                send = {"uid": '0', "token": '0', "seqnum": "GMPCBBS1555577562755000",
                        "data": {"id": "", "page": '1', "order": '0', "count": '20', "louzhu": '0', "first_pid": '0',
                                 "last_pid": '0', "overview": '1', "source": '1'}}
                if item['acticle_content_type'] != 1:
                    send.update({'louzhu': '1'})
                if item['acticle_id']:
                    send['data']['id'] = str(item['acticle_id'])
                logger.warning(send)
                yield item
                # yield scrapy.Request(url=url,  callback=self.parseArticleInfo, body=json.dumps(send), meta=dict(item=item), method='POST')
        except Exception as e:
            logger.warning(e)


    def parseArticleInfo(self, response):
        item = response.meta['item']
        try:
            response_data = json.loads(response.text.replace('for (;;);', '').replace('end;;;', ''))
            item['louzhuid'] = response_data['data']['louzhuid']
            item['louzhu'] = response_data['data']['louzhu']
            item['postcount'] = response_data['data']['postcount']
            for comment in response_data['data']['posts']:
                item['comments'] = list()
                comment_info = {
                    'comment_id': comment['authorid'],
                    'comment_pid': comment['pid'],
                    'comment_name': comment['author'],
                    'comment_time': comment['dateline'],  # 时间戳
                    'comment_content': comment['message']
                }
                item['comments'].append(comment_info)
            yield item
        except Exception as e:
            logger.warning(e)
