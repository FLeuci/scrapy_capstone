import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import spiders.report_crawler as rc
import utils as conf
import logging
from rep_mak import ReportMaker
from spiders.crawler_check import Checker
import json
import pandas

logging.basicConfig(filename='../test.log', level=logging.INFO)

if __name__ == "__main__":
    prev_articles = None

    if not conf.path_exist('all_articles.json'):
        crawler = rc.ReportCrawler()
        crawler.crawl()
        crawler.export_json()
    else:
        list_of_articlesJson = conf.read_from_data('articles.json')
        list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')
        prev_articles = list_of_articles.loc[:, ['title']]

        # TODO Launch spider crawler_check just for all titles
        import subprocess

        process = subprocess.Popen(['scrapy', 'runspiders', 'ArticlesCheckCrawler'],
                shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        new_articles = conf.read_from_data('articles.json')

        flag = True
        for new_art in new_articles:
            flag = new_art in prev_articles
        if not all(new_art in new_articles for new_art in prev_articles):
            if not flag:
                crawler = rc.ReportCrawler()
                crawler.crawl()
                crawler.export_json()
            else:
                logging.info("No new articles found")

    report_maker = ReportMaker()

    # # Reading from Json files
    # with open('authors.json') as f:
    #     list_of_authors = json.load(f)

    list_of_authors = conf.read_from_data('authors.json')
    list_of_articlesJson = conf.read_from_data('articles.json')
    list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')

    report_maker.authors(list_of_authors)
    report_maker.articles(list_of_articles)
    report_maker.plotting(list_of_articles)
