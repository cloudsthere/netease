# -*- coding: utf-8 -*-
import scrapy
import re
import pymysql, time, html


class TechSpider(scrapy.Spider):
    name = 'tech'
    allowed_domains = ['tech.163.com']
    start_urls = ['http://tech.163.com/gd/']

    # �����ݿ�����
    db = pymysql.connect("192.168.10.10","homestead","secret","wordpress", charset = 'utf8' )
     
    # ʹ�� cursor() ��������һ���α���� cursor
    cursor = db.cursor()

    # ��ǰ�б�ҳ
    page = 1;
    list_url = 'http://tech.163.com/special/gd2016_{list_page}/' 
    last_crawl_time = 0;

    def __init__(self, last_crawl_time):
        super().__init__()
        self.last_crawl_time = last_crawl_time


    # �ϴ�����ʱ��
    # sql = 'select execute_time from crawl_log where spider="%s" order by id desc limit 1' % name;
    # last_crawl_time = cursor.execute(sql);
    # print(domain)

    # �������м�¼
    # sql = 'insert into crawl_log (spider, excute_time) values '

    # ��ȡ������������
    def parse(self, response):

        i = 0
        detail_urls = ''
        while i < len(response.xpath('//*[@id="news-flow-content"]/li')):
            i += 1
            # �б�ҳ���ж��Ƿ����
            post_time = response.xpath('//*[@id="news-flow-content"]/li[%d]//p[@class="sourceDate"]/text()' % i ).extract_first()
            # print(post_time)
            post_time = time.mktime(time.strptime(post_time, '%Y-%m-%d %H:%M:%S'))
            if (post_time > self.last_crawl_time):
                xpath = '//*[@id="news-flow-content"]/li[%d]/div[1]/h3/a/@href' % i
                detail_url = response.xpath(xpath).extract_first()

                yield scrapy.Request(detail_url, callback = self.parseDetail)

        # �ж��Ƿ�������һҳ
        # ��ʱ��post_time�����һ����
        print(self.last_crawl_time)
        
        if (post_time > self.last_crawl_time):
            self.page = self.page + 1
            list_url = self.list_url.format(list_page = str(self.page).zfill(2))
            # print(list_url)
            yield scrapy.Request(list_url, callback = self.parse)



    # ��������ҳ
    def parseDetail(self, response):

        title = response.xpath('//*[@id="epContentLeft"]/h1/text()').extract_first()
        title = title.replace('"', '\\"')
        content = response.xpath('//*[@id="endText"]').extract_first()
        content = content.replace('"', '\\"')
        post_time_raw = response.xpath('//*[@class="post_time_source"]/text()').extract_first()
        post_time = re.search ('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', post_time_raw).group(0)
        post_source_website = response.xpath('//a[@id="ne_article_source"]/text()').extract_first()
        post_source_url = response.xpath('//a[@id="ne_article_source"]/@href').extract_first()

        # print(response.url)

        try:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            sql = '''
            insert into wp_posts 
            (post_author, post_date, post_excerpt, to_ping, pinged, post_content_filtered,post_date_gmt, post_content, post_title, post_modified, post_modified_gmt, 
            source, source_website, source_url)
            values ("%s", "%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")
            ''' % (1, post_time, '', '', '', '', post_time, content, title, now, now, 'netease', post_source_website, post_source_url)

            # ִ��sql���
            self.cursor.execute(sql)
            # �ύ�����ݿ�ִ��
            self.db.commit()

            sql = 'update wp_posts set post_name=%d where ID=%d' % (self.cursor.lastrowid, self.cursor.lastrowid)
            self.cursor.execute(sql);
            self.db.commit();

        except Exception as e:
            print('sql exception: ', e)
            print(response.url)


# if (__name__ == '__main__'):
#     TechSpider.parse()


