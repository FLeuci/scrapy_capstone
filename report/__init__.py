# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import glob
import os

import scrapy
import re
from scrapy import Selector
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
import pandas as pd


class ReportCrawler:
    author_urls = []
    records = dict()

    class AllAuthorsCrawler(CrawlSpider):
        name = 'AllAuthors'

        rules = (Rule(LinkExtractor(allow=('/author/')), callback='cache_author_links'),)
        start_urls = ['https://blog.griddynamics.com/all-authors/']

        def cache_author_links(self, response):
            ReportCrawler.author_urls.append(response._get_url())

    class AllArticlesByAuthorCrawler(Spider):
        name = 'AllArticlesByAuthor'

        def start_requests(self):
            for one_url in ReportCrawler.author_urls:
                yield scrapy.Request(url=one_url, callback=self.print)

        def print(self, response):
            key_url = response._get_url().rsplit('/')[-2] #get the author nickname after the last slash
            name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
            date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
            articles = []
            for row in date_title_part:
                date = Selector(text=row.extract()).xpath('///span/text()').extract_first()
                title = Selector(text=row.extract()).xpath('///a/text()').extract_first()
                articles.append({'name': name, 'date': date, 'title': title})
            author_articles = {'authorKey': key_url, 'articles': articles}
            ReportCrawler.records.update(author_articles)


            # df = pd.DataFrame(eval(str(self.records)))
            # df.to_json(f"{key_url}-data.json")

    def save_csv(self):
        df = pd.DataFrame(eval(str(self.records)))
        df.to_csv(f"data.csv")
        #does not work

    def crawl(self):
        configure_logging()
        runner = CrawlerRunner()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(ReportCrawler.AllAuthorsCrawler)
            yield runner.crawl(ReportCrawler.AllArticlesByAuthorCrawler)
            reactor.stop()

        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished


if __name__ == "__main__":
    crawler = ReportCrawler()
    crawler.crawl()
    crawler.save_csv()

    # create another process that calls several Spiders for each pourpose
