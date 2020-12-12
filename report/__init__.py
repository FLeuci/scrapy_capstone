# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re

from scrapy import Selector
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
import pandas as pd


def get_href(record):
    first = re.sub("(a href=\"#)([a-z]*)(\")", "", record)
    print(first)


class AllAuthorsCrawler(CrawlSpider):
    name = 'AllAuthors'

    rules = (Rule(LinkExtractor(allow=('/author/')), callback='cache_author_links'),)
    start_urls = ['https://blog.griddynamics.com/all-authors/']

    def cache_author_links(self, response):
        with open('authors.txt', 'a+') as f:
            f.write(response._get_url() + '\n')


class AllArticlesByAuthorCrawler(Spider):
    name = 'AllArticlesByAuthor'
    records = []

    def fetch_urls(self):
        author_urls = []
        with open('authors.txt') as f:
            for line in f:
                author_urls.append(line)
        return author_urls

    def start_requests(self):
        urls = self.fetch_urls()
        for one_url in urls:
            yield scrapy.Request(url=one_url, callback=self.print)

    def print(self, response):
        name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
        date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
        for row in date_title_part:
            date = Selector(text=row.extract()).xpath('///span/text()').extract_first()
            title = Selector(text=row.extract()).xpath('///a/text()').extract_first()
            record = {'name': name, 'date': date, 'title': title}
            self.records.append(record)

        df = pd.DataFrame(eval(str(self.records)))
        df.to_csv('authors_data.csv', mode='a', header=False)


if __name__ == "__main__":
    # process = CrawlerProcess()
    # process.crawl(AllAuthorsCrawler)
    # process.start()
    #
    # process.crawl(AllArticlesByAuthorCrawler)
    # process.start()
    configure_logging()
    runner = CrawlerRunner()


    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(AllAuthorsCrawler)
        yield runner.crawl(AllArticlesByAuthorCrawler)
        reactor.stop()


    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished

    # create another process that calls several Spiders for each pourpose
