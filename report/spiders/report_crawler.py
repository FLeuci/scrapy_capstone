from scrapy import Selector, Request
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
import report.Configs as conf
from datetime import datetime


class ReportCrawler:
    authors = []
    articles = []
    base_path = "./data/"

    def __init__(self):
        import os
        if os.path.exists(os.path.dirname(ReportCrawler.base_path)):
            import shutil
            shutil.rmtree(os.path.dirname(ReportCrawler.base_path))
        os.makedirs(os.path.dirname(ReportCrawler.base_path))

    def crawl(self):
        configure_logging()
        runner = CrawlerRunner()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(AuthorInfoCrawler)
            yield runner.crawl(ArticleInfoCrawer)
            reactor.stop()

        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished

    def export_json(self):
        with open(f"{ReportCrawler.base_path}authors.json", "w") as f:
            f.write(str(ReportCrawler.authors))


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
            date_formatted = datetime.strptime(date, '%B %d, %Y').strftime('%Y%m%d')
            article_title = Selector(text=row_extracted).xpath('///a/text()').extract_first()
            article_url = Selector(text=row_extracted).xpath('///a/@href').extract_first()
            ReportCrawler.authors.append({'keyUrl': key_url,
                                           'name': name,
                                           'jobTitle': job_title,
                                           'linkedinUrl': linkedin_url,
                                           'date': date_formatted,
                                           'article_title': article_title,
                                           'article_url': article_url})


class ArticleInfoCrawer(Spider):
    name = 'ArticleInfoCrawer'

    def start_requests(self):
        author_link_list = list(
            map(lambda obj: (obj['keyUrl'], conf.gd_base_url + obj['article_url'], obj['article_url']),
                ReportCrawler.authors))
        for link in author_link_list:
            yield Request(url=link[1])

    def parse(self, response):
        title = response.xpath('//*[@id="wrap"]/h1/text()').extract_first()
        url_to_full_version = response._get_url()
        first_160 = ''.join(response.xpath('//*[@id="woe"]/section/div/p/text()').extract())[:160]
        publication_date = response.xpath('//*[@id="wrap"]/div/div[2]/text()').extract_first()
        authors_section = response.xpath('//*[@id="wrap"]/div/div[1]/div/span/a')

        #//*[@id="wrap"]/div/div[1]/div[1]/span/a/span/text()
        #//*[@id="wrap"]/div/div[1]/div[1]/span/a/@href
        for row in authors_section:
            full_author_url = Selector(text=row.extract()).xpath('///a/@href').extract_first()
            author_fullname = Selector(text=row.extract()).xpath('///a/span/text()').extract_first()
            print()
        # author_fullname
        # author_url = //*[@id="wrap"]/div/div[2]/text()
        #tags



        print(response)
