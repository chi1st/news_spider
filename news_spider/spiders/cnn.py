# -*- coding: utf-8 -*-
import scrapy

import re

from news_spider.items import NewsSpiderItem


class CnnSpider(scrapy.Spider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/world/']

    def parse(self, response):
        href = response.xpath('//article//h3//a/@href')
        for i in href:
            url = response.urljoin(i.extract())
            if self.is_url_needed(url):
                yield scrapy.Request(url, callback=self.parse_news)

    def parse_news(self, response):
        title = response.xpath('//article//h1/text()').extract_first()
        post_time = response.xpath('//article//p[@class="update-time"]/text()').extract_first()
        content = response.xpath('//*[@id="body-text"]//*[contains(@class, "zn-body__paragraph")]//text()')
        content = ' '.join(content.extract())
        item = NewsSpiderItem()
        item['title'] = title
        item['post_time'] = post_time
        item['content'] = content
        yield item

    def get_pubtime_by_url(self, url):
        m = re.search(r'(20\d{2})[/:-]([0-1]?\d)[/:-]([0-3]?\d)', url)
        res = ' '.join(m.groups()) if m else None
        return res

    def is_url_needed(self, url):
        if url.endswith('.html'):
            if self.get_pubtime_by_url(url):
                return True
        else:
            return False
