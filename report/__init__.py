# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re
import json
from datetime import datetime

from pandas._libs.tslibs import strptime
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def get_href(record):
    first = re.sub("(a href=\"#)([a-z]*)(\")", "", record)
    print(first)


class WebCrawler(CrawlSpider):
    name = 'Start'

    rules = (Rule(LinkExtractor(allow='/author/'), callback='parse1'),)
    start_urls = ['https://blog.griddynamics.com/all-authors/']

    def parse1(self, response):
        author_name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()
        date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
        job_title = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/p/text()').extract_first()
        linkedin_url = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[1]/ul/li/a/@href').extract_first()
        for row in date_title_part:
            date = Selector(text=row.extract()).xpath('///span/text()').extract_first()
            converted_date = datetime.strptime(date, '%B %d, %Y')
            title = Selector(text=row.extract()).xpath('///a/text()').extract_first()
            print(f"name: {author_name}, date: {converted_date} \t \t title: {title}, job_title: {job_title}, linkedin_url: {linkedin_url}")
            with open('results.txt', 'a+') as outfile:
                outfile.write(f"name: {author_name} \t,"
                              f" date: {converted_date} \t \t title: {title} \t,"
                              f" job_title: {job_title} \t,"
                              f" linkedin_url: {linkedin_url} \n")
                #json.dump(results, outfile)
                #f.write(f"author: {author_name}, date: {date} \t \t title: {title}, job title: {job_title}, linkedin url: {linkedin_url}, '\n',")

    def get_href(private, record):
        first = re.sub(r"(<a href=\"#)", "", record)
        print(first)


    def parse2(self, response):
        autori = list(response.xpath('//*[@id="authorsmini"]/div/a').getall())
        autori_list_clean = map(self.clean_from_tag, autori)
        list_autori = list(autori_list_clean)
        print('\n'.join(list_autori))
        print(len(list_autori))


    def clean_from_tag(self, tag):
        return re.sub(r"[\n\t]*", '', re.sub(r"<.*?>", '', tag))


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WebCrawler)
    process.start()

    #create another process that calls several Spiders for each pourpose
