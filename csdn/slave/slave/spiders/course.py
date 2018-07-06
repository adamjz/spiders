# -*- coding: utf-8 -*-
import scrapy
from slave.items import SlaveItem
from scrapy_redis.spiders import RedisSpider

class CourseSpider(RedisSpider):
    name = 'course'
    # allowed_domains = ['edu.csdn.net']
    # start_urls = ['http://edu.csdn.net/']
    redis_key = 'csdnspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(CourseSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        info = response.css('div.info_right')
        item = SlaveItem()
        item['id'] = response.css('#course_id::attr(value)').extract_first()
        item['title'] = info.css('h1::text').extract_first().strip()
        item['url'] = response.url
        item['hours'] = info.css('span.pinfo::text').extract_first().split('/')[-1]
        item['forwho'] = info.css('span.for::text').extract_first()
        item['joined_num'] = info.css('span.num::text').extract_first()
        item['price'] = info.css('span.money::text').extract_first().strip()
        # print(item)
        yield item