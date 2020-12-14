# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging


class ReportCrawler:
    author_urls = []

    def __init__(self) -> None:
        import os
        if os.path.exists(os.path.dirname("./data/")):
            import shutil
            shutil.rmtree(os.path.dirname("./data/"))
        os.makedirs(os.path.dirname("./data/"))

    class AllArticlesByAuthorCrawler(CrawlSpider):

        name = 'AllArticlesByAuthor'

        rules = (Rule(LinkExtractor(allow=('/author/')), callback='parse'),)
        start_urls = ['https://blog.griddynamics.com/all-authors/']

        def parse(self, response, **kwargs):
            key_url = response._get_url().rsplit('/')[-2]  # get the author nickname after the last slash
            name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
            job_title = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/p/text()').extract_first()
            linkedin_url = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[1]/ul/li/a/@href').extract_first()
            date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
            articles = []
            for row in date_title_part:
                row_extracted = row.extract()
                date = Selector(text=row_extracted).xpath('///span/text()').extract_first()
                title = Selector(text=row_extracted).xpath('///a/text()').extract_first()
                articles.append({'keyUrl': key_url,
                                 'name': name,
                                 'jobTitle': job_title,
                                 'linkedinUrl': linkedin_url,
                                 'date': date,
                                 'title': title})

            with open(f"./data/{key_url}-data.json", "w") as f:
                f.write(str(articles))

    def crawl(self):
        configure_logging()
        runner = CrawlerRunner()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(ReportCrawler.AllArticlesByAuthorCrawler)
            reactor.stop()

        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished


if __name__ == "__main__":
    crawler = ReportCrawler()
    crawler.crawl()

    # crawler.save_csv()

    # create another process that calls several Spiders for each pourpose
