import os
import sys
import scrapy


class WebCrawler(scrapy.Spider):
    name = 'Start'

    def startproject(self):
        urls = [
            'https: // blog.griddynamics.com /'
        ]
        yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        author_list = response.xpath('//*[@id="slick-slide01"]/a/article/div[1]/span/strong').extract()
        print(author_list)


