import os
import spiders.report_crawler as rc
import utils as conf
import logging
from rep_mak import ReportMaker
from spiders.crawler_check import CheckerCrawler
import json
import pandas as pd

logging.basicConfig(filename='../test.log', level=logging.INFO)

if __name__ == "__main__":
    prev_articles = None

    crawler = CheckerCrawler()
    crawler.crawl()
    new_articles = set(CheckerCrawler.all_articles)

    if not conf.path_exist("all_articles.json"):
        conf.write_in_data("all_articles.json", json.dumps(CheckerCrawler.all_articles))
        prev_articles = []
    else:
        prev_articles = set(json.loads("all_articles.json"))
    flag = True
    for new_art in new_articles:
        flag = new_art in prev_articles
    #if not all(new_art in new_articles for new_art in prev_articles):
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
    f = open("authors.json",)
    list_of_authors = json.loads(f)
    list_of_articlesJson = conf.read_from_data('articles.json')
    list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')

    report_maker.authors(list_of_authors)
    report_maker.articles(list_of_articles)
    report_maker.plotting(list_of_articles)
