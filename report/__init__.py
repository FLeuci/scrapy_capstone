# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re
import json
from datetime import datetime

from pandas._libs.tslibs import strptime
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor

# if __name__ == "__main__":
#    process = CrawlerProcess()
#    process.crawl(WebCrawler)
#    process.start()

# create another process that calls several Spiders for each pourpose
from scrapy import Selector
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
import json
#import report.Configs as conf
from datetime import datetime


class ReportCrawler:
    articles = []
    articles_details = []

    def __init__(self):
        import os
        if os.path.exists(os.path.dirname("./data/")):
            import shutil
            shutil.rmtree(os.path.dirname("./data/"))
        os.makedirs(os.path.dirname("./data/"))

    def crawl(self):
        configure_logging()
        runner = CrawlerRunner()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(AuthorInfoCrawler)
            reactor.stop()

        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished

    def get_base_url(self):
        self.base_url = 'https://blog.griddynamics.com/'
        return self.base_url

    def export_json(self):
        with open('./data/data.json', 'w') as f:
            f.write(str(self.articles))


class AuthorInfoCrawler(CrawlSpider):
    name = 'AuthorInfoCrawler'
    rules = (Rule(LinkExtractor(allow=('/author/')), callback='parse'),)
    start_urls = ['https://blog.griddynamics.com//all-authors/']

    def parse(self, response, **kwargs):
        key_url = response._get_url().rsplit('/')[-2]  # get the author nickname after the last slash
        name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
        job_title = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/p/text()').extract_first()
        linkedin_url = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[1]/ul/li/a/@href').extract_first()
        date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
        for row in date_title_part:
            row_extracted = row.extract()
            raw_date = Selector(text=row_extracted).xpath('///span/text()').extract_first()
            date = datetime.strptime(raw_date, '%B %d, %Y').strftime('%Y%m%d')
            article_title = Selector(text=row_extracted).xpath('///a/text()').extract_first()
            article_url = Selector(text=row_extracted).xpath('///a/@href').extract_first()
            ReportCrawler.articles.append({'keyUrl': key_url,
                                           'name': name,
                                           'jobTitle': job_title,
                                           'linkedinUrl': linkedin_url,
                                           'date': date,
                                           'article_title': article_title,
                                           'article_url': article_url})


class ArticleInfoCrawler(Spider):
    name = 'ArticleInfoCrawler'


    def start_requests(self):
        author_link_list = list(
            map(lambda obj: (obj['keyUrl'], 'https://blog.griddynamics.com' + obj['article_url']),
                ReportCrawler.articles))
        for link in author_link_list:
            yield scrapy.Request(url= link[1])
        return super().start_requests()
        #yield_url


    def parse(self, response, **kwargs):

        title = response.xpath('//*[@id="wrap"]/h1/text()').extract_first()
        url_to_full_version = response._get_url()
        body = response.path('//*[@id="woe"]/section/div/p/text()').extract()
        first_160 = body[:160]
        publication_date = response.xpath('//*[@id="wrap"]/div/div[2]/text()').extract_first()
        authors_fullname = response.xpath('//*[@id="wrap"]/div/div[position() > 1]')
        tags = response.xpath('//*[@id="woe"]/section/div/div/text()').extract()
        for row in authors_fullname:
            row_extracted = row.extract()
            author_fullname = Selector(text=row_extracted).xpath('///span/text()').extract_first()
            key_url = Selector(text=row_extracted).xpath('///a/@href').extract_first()
            ReportCrawler.articles_details.append({'title': title,
                                                   'url': url_to_full_version,
                                                   'first 160': first_160,
                                                   'date': publication_date,
                                                   'author': author_fullname,
                                                   'article_url': key_url,
                                                   'tag': tags })



if __name__ == "__main__":
    crawler = ReportCrawler()
    crawler.crawl()
    crawler.export_json()
