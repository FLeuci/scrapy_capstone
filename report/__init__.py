# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def get_href(record):
    first = re.sub("(a href=\"#)([a-z]*)(\")", "",record)
    print(first)


class AllAuthorsCrawler(CrawlSpider):
    name = 'AllAuthors'

    rules = (Rule(LinkExtractor(allow = ('/author/')), callback = 'cache_author_links'),)
    start_urls = ['https://blog.griddynamics.com/all-authors/']

    def cache_author_links(self, response):
        with open('authors.txt', 'a+') as f:
            f.write(response._get_url() + '\n')

class AllArticlesByAuthorCrawler(CrawlSpider):
    name = 'AllArticlesByAuthor'
    def fetch_urls(self):
        author_urls = []
        with open('data') as f:
            for line in f:
                author_urls.append(line)
        return author_urls

    start_urls = fetch_urls()


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(AllAuthorsCrawler)
    process.start()

    #create another process that calls several Spiders for each pourpose
