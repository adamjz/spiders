# -*- coding: utf-8 -*-
import scrapy,re
from slave.items import SlaveItem
from scrapy_redis.spiders import RedisSpider

class BookSpider(RedisSpider):
    name = 'slave_book'
    # 存储图书url的redis key
    redis_key = 'bookspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(BookSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        print('='*30,response.status)
        item = SlaveItem()
        item['id'] = response.url.split('/')[-2]
        item['title'] = response.css('h1 span::text').extract_first()

        # 获取info图书信息，若信息不存在则为None，存入mysql时对应值为Null
        info = response.css('#info').extract_first()

        try:
            # 作者
            authors = re.search('<span.*?作者.*?</span>(.*?)<br',info,re.S)
            if authors:
                item['author'] = '、'.join(re.findall('<a.*?>(.*?)</a>',authors.group(1),re.S)).replace('\n','').replace(' ','')
            else:
                item['author'] = None
            
            # 出版社
            if re.findall('<span.*?出版社:</span>(.*?)<br', info):
                item['press'] = ' '.join(re.findall('<span.*?出版社:</span>(.*?)<br', info)).strip()
            else:
                item['press'] = None

            # 原作名
            if re.findall('<span.*?原作名:</span>(.*?)<br', info):
                item['original'] = ' '.join(re.findall('<span.*?原作名:</span>(.*?)<br', info)).strip()
            else:
                item['original'] = None

            # 译者
            translators = re.search('<span.*?译者.*?</span>(.*?)<br',info,re.S)
            if translators:
                item['translator'] = '、'.join(re.findall('<a.*?>(.*?)</a>',translators.group(1),re.S)).replace('\n','').replace(' ','')
            else:
                item['translator'] = None
            
            # 出版年
            if re.findall('<span.*?出版年:</span>(.*?)<br', info):
                item['imprint'] = ' '.join(re.findall('<span.*?出版年:</span>(.*?)<br', info)).strip()
            else:
                item['imprint'] = None

            # 页数
            if re.findall('<span.*?页数:</span>.*?([0-9]+)<br', info):
                item['pages'] = ' '.join(re.findall('<span.*?页数:</span>.*?([0-9]+)<br', info)).strip()
            else:
                item['pages'] =  None

            # 价格
            if re.findall('<span.*?定价:</span>.*?([0-9\.]).*?<br', info):
                item['price'] = ' '.join(re.findall('<span.*?定价:</span>.*?([0-9\.]).*?<br', info)).strip()
            else:
                item['price'] = None
     
            # 装帧
            if re.findall('<span.*?装帧:</span>(.*?)<br', info, re.S):
                item['binding'] = ' '.join(re.findall('<span.*?装帧:</span>(.*?)<br', info, re.S)).strip()
            else:
                item['binding'] = None

            # 丛书
            if re.findall('<span.*?丛书:</span>.*?<a.*?>(.*?)</a>', info, re.S):
                item['series'] = ' '.join(re.findall('<span.*?丛书:</span>.*?<a.*?>(.*?)</a>', info, re.S)).strip()
            else:
                item['series'] = None

            # ISBN
            if re.findall('<span.*?ISBN:</span>.*?([0-9]+)<br', info, re.S):
                item['isbn'] = ' '.join(re.findall('<span.*?ISBN:</span>.*?([0-9]+)<br', info, re.S))
            else:
                item['isbn'] = None

            # 评分
            if response.css('strong.ll.rating_num::text').extract_first().strip():
                item['score'] = response.css('strong.ll.rating_num::text').extract_first().strip()
            else:
                item['score'] = None
            
            # 评价人数
            if response.css('a.rating_people span::text').extract_first():
                item['votes'] = response.css('a.rating_people span::text').extract_first().strip()
            else:
                item['votes'] = None

            # URL地址
            item['url'] = response.url

            yield item
        except Exception as Err:
            print('\n获取信息失败，原因：\n%s\n' % Err)