import scrapy

Class Capstone(scrapy.Spider):
    name = 'capstone'
    start_urls = [
        'https://blog.griddynamics.com/'
    ]

    def parse(self, response):
        search_results = response.xpath('//*[@id="woe"]/section/div/div[2]/a/article')

        for result in search_results:
            result_loader = ItemLoader()
