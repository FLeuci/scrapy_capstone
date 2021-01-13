from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer


class Checker(CrawlSpider):
    name = 'ArticlesCheckCrawler'
    start_urls = ['https://blog.griddynamics.com/all-authors/']
    rules = (Rule(LinkExtractor(allow='/author/'), callback='parse'),)

    def parse(self, response, **kwargs):
        titles = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div/a/text()').extract()
        for title in titles:
            with open('all_titles.txt', 'w') as f:
                f.write(title + '\n')






