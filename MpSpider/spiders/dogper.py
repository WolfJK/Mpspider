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
from copy import deepcopy

file = open('./remain/%s' % 'log.txt', encoding='utf-8', mode='w')
logger = logging.getLogger(__name__)

logging.basicConfig(
            level=logging.WARNING,
            format='levelname:%(levelname)s ,[line:%(lineno)d]== [filename]: %(filename)s [message]:%(message)s',
            datefmt='[%d/%b/%Y %H:%M:%S]',
            stream=file
        )

class DogSpider(CrawlSpider):  # scrapy.spiders
    name = 'dog'
    allowed_domains = ['club.goumin.com', 'lingdang.goumin.com']
    start_urls = ['http://lingdang.goumin.com/v2/thread-index']
    # s = scrapy_redis.get_redis(host='localhost', port=6379, db=0)

    # redis_key = 'dog:requests'

    # start_urls = ['http://dastest.marcpoint.com/wordchart/']
    #  提供账号生成的 token
    temp = 'Hm_lvt_8d0447bcda7403d6e941367e44cbeea8=1576060198; _ga=GA1.2.473392251.1576060199; wyq_jcrb_wyq_jcrb_=8276; oldPath=/; JSESSIONID=556950d3-7afe-4992-9ceb-a8b5a5a81079'
    seqnum = 'GMPCBBS1555577562755000'
    datas = {"uid": '0', "token": 'j6fv473ug7sh2bvep6vjywibnmhcog7vccf6a8rg47mu85yp2myq65rhhwjt0ig3',
            "seqnum": seqnum, "data": ''}
    logger.info(settings.DEFAULT_REQUEST_HEADERS)
    PageNums = 1 #  页数

    def start_requests(self):
        logger.info('--start_requests()---')
        logger.info(json.dumps(self.datas))
        for i in range(1, self.PageNums + 1):
            item = dict()
            t = deepcopy(self.datas)
            t['data'] = {"count": '2', "page": str(i)}
            yield scrapy.Request(url=self.start_urls[0],  callback=self.parse, body=json.dumps(t), meta=dict(item=item), method='POST')
            # yield self.make_requests_from_url(url)


    def parse(self, response):
        '''处理首页查询的内容'''
        logger.info('--parse()---')
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
                url = 'http://lingdang.goumin.com/v2/thread/%s' % str(item['acticle_id'])
                # 可变参数 id，louzhu
                temp = {"id": "", "page": '1', "order": '0', "count": '20', "louzhu": '0', "first_pid": '0',
                                 "last_pid": '0', "overview": '1', "source": '1'}
                if str(item['acticle_content_type']) != '1':
                    temp.update({'louzhu': '1'})
                if item['acticle_id']:
                    temp['id'] = str(item['acticle_id'])
                t = deepcopy(self.datas)
                t['data'] = temp
                logger.info(self.datas)
                # yield item
                yield scrapy.Request(url=url,  callback=self.parseArticleInfo, body=json.dumps(t),
                                     meta=dict(item=deepcopy(item)), method='POST')
        except Exception as e:
            logger.warning(e)


    def parseArticleInfo(self, response):
        logger.info('--parseArticleInfo()---')
        item = response.meta['item']
        try:
            response_data = json.loads(response.text.replace('for (;;);', '').replace('end;;;', ''))
            if response_data['code'] == 11112:
                yield item
            item['louzhuid'] = response_data['data']['louzhuid']
            item['louzhu'] = response_data['data']['louzhu']
            item['postcount'] = response_data['data']['postcount']
            item['comments'] = list()
            for comment in response_data['data']['posts']:

                comment_info = {
                    'comment_id': comment['authorid'],
                    'comment_pid': comment['pid'],
                    'comment_name': comment['author'],
                    'comment_time': comment['dateline'],  # 时间戳
                    'comment_content': comment['message']
                }
                item['comments'].append(comment_info)
            logger.info(len(item['comments']))
            # 继续抓取用户信息  http://club.goumin.com/personal/index.html?uid=1254570
            uer_url = 'http://lingdang.goumin.com/v2/userinfo'
            logger.info('--==============================()---')
            t = deepcopy(self.datas)
            t['data'] = {"userid": str(item['louzhuid'])}
            yield scrapy.Request(uer_url, body=json.dumps(t), method='POST', meta={'item': deepcopy(item)}, callback=self.parseUserInfo)
            # yield scrapy.FormRequest(uer_url, formdata=t, method='POST', meta={'item': deepcopy(item)}, callback=self.parseUserInfo)
            # yield item
        except Exception as e:
            logger.warning(e)

    def wrapper(self, func):
        logger.info('--wrapper()---')
        def commonReponse(self, *args, **kwargs):
            return func(*args, **kwargs)
        return commonReponse


    def parseUserInfo(self, response):
        logger.info('--parseUserInfo()---')
        item = response.meta['item']
        try:
            response_data = json.loads(response.text.replace('for (;;);', '').replace('end;;;', ''))
            item['infos'] = dict()
            item['infos']['user_id'] = response_data['data']['userid']
            item['infos']['user_brief'] = response_data['data']['bio']
            item['infos']['user_address'] = response_data['data']['location']
            item['infos']['user_gender'] = response_data['data']['gender']
            item['infos']['register_at'] = response_data['data']['daycount']
            item['infos']['name'] = response_data['data']['nickname']
            item['infos']['avatar_img'] = response_data['data']['avatar']
            # item['infos']['pet_name'] = response_data['data']['nickname']
            item['infos']['postcount'] = response_data['data']['threadcount']
            item['infos']['fans_count'] = response_data['data']['fansnums']
            item['infos']['follow_count'] = response_data['data']['follownums']
            item['infos']['name'] = response_data['data']['nickname']
            item['infos']['name'] = response_data['data']['nickname']

            achive = 'http://lingdang.goumin.com/v4/user/user-achievement'
            t = deepcopy(self.datas)
            t['data'] = {"uid": str(item['louzhuid'])}
            t['uid'] = str(item['louzhuid'])
            yield scrapy.Request(url=achive,  callback=self.parseAchaive, body=json.dumps(t),
                                     meta=dict(item=deepcopy(item)), method='POST')
        except Exception as e:
            logger.info(e)


    def parseAchaive(self, response):
        logger.info('--parseAchaive()---')
        item = response.meta['item']
        response_data = json.loads(response.text.replace('for (;;);', '').replace('end;;;', ''))
        item['infos']['like_count'] = response_data['data']['like_num']
        item['infos']['reply_count'] = response_data['data']['comment_num']
        yield item