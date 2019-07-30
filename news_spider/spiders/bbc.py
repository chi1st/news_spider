# -*- coding: utf-8 -*-
import scrapy
import re
import time

from news_spider.items import NewsSpiderItem


class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['https://www.bbc.com/news/world/']

    def parse(self, response):
        href = response.xpath('//*[contains(@class, gs-c-promo)]/@href')
        for i in href:
            url = response.urljoin(i.extract())
            if self.end_num(url):
                yield scrapy.Request(url, callback=self.parse_news)

    def parse_news(self, response):
        url = response.url
        title = response.xpath('//h1[@class="story-body__h1"]/text()').extract_first()
        post_time = response.xpath(
            '//div[@class="date date--v2"]/text()').extract_first()
        content = response.xpath(
            '//div[@class="story-body__inner"]//p//text()'
        )
        content = ' '.join(content.extract())
        if title:
            item = NewsSpiderItem()
            item['url'] = url
            item['title'] = title
            item['report_time'] = post_time
            item['content'] = content
            item['crawl_time'] = time.time()
            yield item

    def end_num(self, string):
        text = re.compile(r".+\d$")
        if text.match(string):
            return True
        else:
            return False
