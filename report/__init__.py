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


class WebCrawler(CrawlSpider):
    name = 'Start'

    #def start_requests(self):
    #    urls = 'https://blog.griddynamics.com/'
    #   yield scrapy.Request(url=urls, callback=self.parse)

    rules = (Rule(LinkExtractor(), callback = 'parse2'),)
    start_urls = ['https://blog.griddynamics.com/all-authors/']

    # def start_requests(self):
    #     urls2 = 'https://blog.griddynamics.com/all-authors/'
    #     yield scrapy.Request(url=urls2, callback=self.parse2)
    def get_href(private, record):
        first = re.sub(r"(<a href=\"#)","",record)
        print(first)

    def parse2(self, response):
        autori = list(response.xpath('//*[@id="authorsmini"]/div/a').getall())
        self.get_href(autori[0])
        autori_list_clean = map(self.clean_from_tag, autori)
        list_autori = list(autori_list_clean)
        print('\n'.join(list_autori))

        substring = 'Vlad'
        counter = list_autori.count(substring)
        print(counter)

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
 #       article_list = response.xpath('//*[@id="woe"]/section/div/div[2]/a/article/h4').extract()
  #      article_list_clean = map(self.clean_from_tag, article_list)
   #     print('\n'.join(article_list_clean))

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
