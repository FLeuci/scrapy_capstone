import json

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer


class CheckerCrawler:
    all_articles = []

    @staticmethod
    def crawl():
        configure_logging()
        # runner = CrawlerRunner()
        process = CrawlerProcess()

        # @defer.inlineCallbacks
        def crawl():
            # yield runner.crawl(Checker)
            # reactor.stop()
            process.crawl(Checker)
            process.start()

        crawl()
        # reactor.run()


class Checker(CrawlSpider):
    name = 'ArticlesCheckCrawler'
    start_urls = ['https://blog.griddynamics.com/all-authors/']
    rules = (Rule(LinkExtractor(allow='/author/'), callback='parse'),)

    def parse(self, response, **kwargs):
        titles = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div/a/text()').extract()
        for title in titles:
            CheckerCrawler.all_articles.append(title)

