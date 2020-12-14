# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import re

from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def get_href(record):
    first = re.sub("(a href=\"#)([a-z]*)(\")", "",record)
    print(first)


class WebCrawler(CrawlSpider):
    name = 'Start'

    #def start_requests(self):
    #    urls = 'https://blog.griddynamics.com/'
    #   yield scrapy.Request(url=urls, callback=self.parse)

    rules = (Rule(LinkExtractor(allow = ('/author/')), callback = 'parse1'),)
    start_urls = ['https://blog.griddynamics.com/all-authors/']

    # def start_requests(self):
    #     urls2 = 'https://blog.griddynamics.com/all-authors/'
    #     yield scrapy.Request(url=urls2, callback=self.parse2)
    def parse1(self, response):

        author_name = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/h3/text()').extract_first()

        date_title_part = response.xpath('//*[@id="woe"]/div[2]/div/div[2]/div[position() > 1]')
        job_title = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[2]/p/text()').extract_first()
        linkedin_url = response.xpath('//*[@id="woe"]/div[2]/div/div[1]/div[1]/ul/li/a/@href').extract_first()
        for row in date_title_part:
            date = Selector(text=row.extract()).xpath('///span/text()').extract_first()
            title = Selector(text=row.extract()).xpath('///a/text()').extract_first()
            print(f"name: {author_name}, date: {date} \t \t title: {title}, job_title: {job_title}, linkedin_url: {linkedin_url}")
            with open('authors.json', 'a+') as f:
                f.write(f"author: {author_name}, date: {date} \t \t title: {title}, job title: {job_title}, linkedin url: {linkedin_url}, '\n',")





    def get_href(private, record):
        first = re.sub(r"(<a href=\"#)","",record)
        print(first)


    def parse2(self, response):
        autori = list(response.xpath('//*[@id="authorsmini"]/div/a').getall())
        autori_list_clean = map(self.clean_from_tag, autori)
        list_autori = list(autori_list_clean)
        print('\n'.join(list_autori))
        print(len(list_autori))


    def clean_from_tag(self, tag):
        return re.sub(r"[\n\t]*", '', re.sub(r"<.*?>", '', tag))

#        author_list = response.xpath('//*[@id="woe"]/section/div/div[2]/a/article/div[2]/span/strong').extract()
 #       author_list_clean = map(self.clean_from_tag, author_list)
  #      list_author = list(author_list_clean)
   #     print('\n'.join(list_author))
#
 #       substring = 'a'
  #      count = list_author.count(substring)
   #     print(count)
#
#        date_list = response.xpath('//*[@id="woe"]/section/div/div[2]/a/article/div[2]/span/text()').extract()
#        date_list_clean = map(self.clean_from_tag, date_list)
#        print('\n'.join(date_list_clean))
#


    #    section = response.xpath('//*[@id="woe"]/section/div/div[2]/a/article')
     #   print(section)
      #  sec = section.xpath('div[2]/span/strong')
       # print(sec)

        #yield {
         #   'author': author_list_clean,
          #  'article': article_list_clean,
           # 'date': date_list_clean
        #}


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WebCrawler)
    process.start()

    #create another process that calls several Spiders for each pourpose
