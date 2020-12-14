from scrapy import Selector
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
import report.Configs as conf

class ReportCrawler:
    articles = []

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
        return self.base_url

    def export_json(self):
        with open(f"./data/data.json", "w") as f:
            f.write(str(self.articles))


class AuthorInfoCrawler(CrawlSpider):
    name = 'AuthorInfoCrawler'
    rules = (Rule(LinkExtractor(allow=('/author/')), callback='parse'),)
    start_urls = [f"{conf.gd_base_url}/all-authors/"]

    def parse(self, response, **kwargs):
        key_url = response._get_url().rsplit('/')[-2]  # get the author nickname after the last slash
        name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
        job_title = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/p/text()').extract_first()
        linkedin_url = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[1]/ul/li/a/@href').extract_first()
        date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
        for row in date_title_part:
            row_extracted = row.extract()
            date = Selector(text=row_extracted).xpath('///span/text()').extract_first()
            article_title = Selector(text=row_extracted).xpath('///a/text()').extract_first()
            article_url = Selector(text=row_extracted).xpath('///a/@href').extract_first()
            ReportCrawler.articles.append({'keyUrl': key_url,
                                           'name': name,
                                           'jobTitle': job_title,
                                           'linkedinUrl': linkedin_url,
                                           'date': date,
                                           'article_title': article_title,
                                           'article_url': article_url})
class ArticleInfoCrawer(CrawlSpider):
    pass #to be completed
