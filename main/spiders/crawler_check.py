import json

from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
import main.utils as conf


class CheckerCrawler:
    all_articles = []

    @staticmethod
    def crawl():
        configure_logging()
        runner = CrawlerRunner()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(Checker)
            reactor.stop()

        crawl()
        reactor.run()


class Checker(CrawlSpider):
    name = 'ArticlesCheckCrawler'
    start_urls = ['https://blog.griddynamics.com/all-authors/']
    rules = (Rule(LinkExtractor(allow='/author/'), callback='parse'),)

    def parse(self, response, **kwargs):
        titles = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div/a/text()').extract()
        for title in titles:
            CheckerCrawler.all_articles.append(title)
        #         date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
        #         for row in date_title_part:
        #             row_extracted = row.extract()
        #             article_title = Selector(text=row_extracted).xpath('///a/text()').extract_first()
        #             Checker.all_articles.append(article_title)
