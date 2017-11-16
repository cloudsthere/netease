# -*- coding: utf-8 -*-
import scrapy


class IthomeSpider(scrapy.Spider):
    name = 'ithome'
    allowed_domains = ['http://it.ithome.com/']
    start_urls = ['http://http://it.ithome.com//']

    def __init__(self, last_crawl_time):
        super().__init__()
        self.last_crawl_time = last_crawl_time

    def parse(self, response):
        lines = response.xpath('//div[@class="new-list"]//li'); 

        for line in lines:
            print(line)
        
