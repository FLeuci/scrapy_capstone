import json
from scrapy import Selector, Request
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from report import utils as conf


class AuthorInfoCrawler(CrawlSpider):
    """
    Takes all needed information about authors
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
            art_date = Selector(text=row_extracted).xpath('///span/text()').extract_first()
            date_formatted = conf.parse_dtts(art_date, '%B %d, %Y')
            article_title = Selector(text=row_extracted).xpath('///a/text()').extract_first()
            article_url = Selector(text=row_extracted).xpath('///a/@href').extract_first()

            if date_formatted >= conf.crawl_date[0].get('LastExecutionDate'):
                conf.write_data_append('authors.json', json.dumps({'keyUrl': key_url,
                                                                   'name': name,
                                                                   'jobTitle': job_title,
                                                                   'linkedinUrl': linkedin_url,
                                                                   'date': date_formatted,
                                                                   'article_title': article_title,
                                                                   'article_url': article_url}))


class ArticleInfoCrawler(Spider):
    """
    Takes all needed information about articles
    """
    name = 'ArticleInfoCrawler'

    def start_requests(self):
        """
        Crawls each authors pages starting from all-authors main page stored in authors report
        """
        authors_pandas = conf.read_from_data('authors.json')
        author_link_list = list(
            map(lambda obj: (obj['keyUrl'], conf.gd_base_url + obj['article_url'], obj['article_url']),
                authors_pandas))
        for link in author_link_list:
            yield Request(url=link[1])

    def parse(self, response, **kwargs):
        """
        Extracts all the data from the crawled pages and appends them to articles list
        """
        title = response.xpath('//*[@id="wrap"]/h1/text()').extract_first()
        if title:
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
                if date_formatted >= conf.crawl_date[0].get('LastExecutionDate'):
                    conf.write_data_append('articles.json', json.dumps({'title': title,
                                                                        'urlFullVersion': url_to_full_version,
                                                                        'first160': first_160,
                                                                        'dateFormatted': date_formatted,
                                                                        'tags': tags,
                                                                        'authorUrl': f"{conf.gd_base_url}"
                                                                                     f"{full_author_url}",
                                                                        'authorName': author_fullname,
                                                                        'author_key': full_author_url.rsplit('/')[-2]
                                                                        }))
