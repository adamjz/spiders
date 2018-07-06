# -*- coding: utf-8 -*-
import scrapy
from jd.items import JdItem

class GoodsSpider(scrapy.Spider):
    name = 'goods'
    allowed_domains = ['jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672']

    def parse(self, response):
        products = response.xpath('.//div[@id="plist"]/ul[contains(@class, "gl-warp")]/li[@class="gl-item"]')
        # print('products\t\t',products)
        for product in products:
            item = JdItem()
            item['name'] = product.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
            item['url'] = 'https:' + product.xpath('.//div[@class="p-name"]/a/@href').extract_first()
            item['price'] = product.xpath('.//div[@class="p-price"]/strong[@class="J_price"][1]/i/text()').extract_first()
            item['comment'] = product.xpath('.//a[@class="comment"]/text()').extract_first()
            item['shop'] = product.xpath('.//div[@class="p-shop"]/span/a/text()').extract_first()
            # print(item)
            yield item

        next_url = response.xpath('.//a[@class="pn-next"]/@href').extract_first()
        if next_url != None:
            url = response.urljoin(next_url)
            yield scrapy.Request(url=url, callback=self.parse)