import json
import os
from scrapy import Selector, Request
from scrapy.crawler import CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

import main.utils as conf


class ReportCrawler:
    """
    Wrapper class responsible of launching spiders needed for generating report
    """
    authors = []
    articles = []

    def __init__(self):
        """
        Create a directory representing the value inside @{main.utils.base_path} if not exists
        """
        if not os.path.exists(os.path.dirname(conf.__file__)):
            os.makedirs(os.path.dirname(conf.__file__))

    @staticmethod
    def crawl():
        configure_logging()
        runner = CrawlerRunner()

        """
        Make a function that reads from last_articles_numbers file and compare with actual
        """

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(AuthorInfoCrawler)
            yield runner.crawl(ArticleInfoCrawer)
            reactor.stop()

        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished

    @staticmethod
    def export_json():
        """
        Export the results obtained from the crawling into JSON files
        """
        conf.write_in_data("authors.json", json.dumps(ReportCrawler.authors))
        conf.write_in_data("articles.json", json.dumps(ReportCrawler.articles))


class AuthorInfoCrawler(CrawlSpider):
    """
    Take all information needed about authors
    """
    name = 'AuthorInfoCrawler'
    rules = (Rule(LinkExtractor(allow='/author/'), callback='parse'),)
    start_urls = [f"{conf.gd_base_url}/all-authors/"]

    def parse(self, response, **kwargs):
        """
        Extracts all the data from the crawled pages and appends them to authors list
        """
        key_url = response._get_url().rsplit('/')[-2]  # get the author nickname after the last slash
        name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
        job_title = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/p/text()').extract_first()
        linkedin_url = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[1]/ul/li/a/@href').extract_first()
        date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
        for row in date_title_part:
            row_extracted = row.extract()
            date = Selector(text=row_extracted).xpath('///span/text()').extract_first()
            date_formatted = conf.parse_dtts(date, '%B %d, %Y')
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
    """
    Take all information needed about articles
    """
    name = 'ArticleInfoCrawer'

    def start_requests(self):
        """
        Crawls each authors pages starting from all-authors main page stored in authors report
        """
        author_link_list = list(
            map(lambda obj: (obj['keyUrl'], conf.gd_base_url + obj['article_url'], obj['article_url']),
                ReportCrawler.authors))
        for link in author_link_list:
            yield Request(url=link[1])

    def parse(self, response, **kwargs):
        """
        Extracts all the data from the crawled pages and appends them to articles list
        """
        title = response.xpath('//*[@id="wrap"]/h1/text()').extract_first()
        url_to_full_version = response._get_url()
        first_160 = ''.join(response.xpath('//*[@id="woe"]/section/div/p/text()').extract())[:160]
        base_date = response.xpath('//*[@id="wrap"]/div/div[2]/text()').extract_first()
        date_formatted = conf.exec_func_chain(base_date,
                                              [conf.clean_records_regex,
                                               lambda v: v[0:-2],
                                               lambda v: conf.parse_dtts(v, '%b %d, %Y')])

        tags = response.xpath('//*[@id="woe"]/section[3]/div/div/a/text()').extract()
        authors_section = response.xpath('//*[@id="wrap"]/div/div[1]/div/span/a')
        for row in authors_section:
            full_author_url = Selector(text=row.extract()).xpath('///@href') \
                .extract_first()
            author_fullname = conf.clean_records_regex(
                Selector(text=row.extract()).xpath('///span/text()').extract_first())
            ReportCrawler.articles.append({
                'title': title,
                'urlFullVersion': url_to_full_version,
                'first160': first_160,
                'dateFormatted': date_formatted,
                'tags': tags,
                'authorUrl': f"{conf.gd_base_url}{full_author_url}",
                'authorName': author_fullname,
                'author_key': full_author_url.rsplit('/')[-2]
            })
