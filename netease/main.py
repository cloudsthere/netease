# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# print(dir(process))
process.crawl('tech', last_crawl_time = 110)
process.start() # the script will block here until the crawling is finished