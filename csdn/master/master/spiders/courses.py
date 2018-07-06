# -*- coding: utf-8 -*-
import scrapy
from master.items import MasterItem  


class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['edu.csdn.net']
    start_urls = ['https://edu.csdn.net/courses/k']

    def parse(self, response):
        courses_list = response.selector.css('div.course_dl_list')
        item = MasterItem()
        for course in courses_list:
            item['url'] = course.css('a::attr(href)').extract_first()
            yield item

        next_url = response.css('a.btn-next::attr(href)').extract_first()
        print('下一页URL：\n\t\t %s' % next_url)
        if next_url != response.url:
            url = response.urljoin(next_url)
            print(url, response.url)
            yield scrapy.Request(url=url, callback=self.parse)



