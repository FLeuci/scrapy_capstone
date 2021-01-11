import main.spiders.report_crawler as rc
import main.utils as conf
import pandas as pd
import logging
from main.rep_mak import ReportMaker
from main.spiders.crawler_check import CheckerCrawler

logging.basicConfig(filename='../test.log', level=logging.INFO)

if __name__ == "__main__":
    #TODO LOAD PREVIOUS ARTICLES FILE
    conf.read_from_data("num_articles.json") #is a single list as pandas
    #TODO add crawling for Check AND SAVE THE ARTICLE NAMES IN FILE (WATCH OUT AT THE FILE NAME)
    crawler = CheckerCrawler()
    crawler.crawl()
    number_articles = CheckerCrawler.all_articles
    #IF ALL ARTICLES ARE THE SAME... ELSE
    #conf.write_in_data("num_articles.json", json.dumps(number_articles))
    #TODO COMPARE ARTICLES

    if conf.base_path_empty: #IF THERE IS SOMETHING NEW
        crawler = rc.ReportCrawler()
        crawler.crawl()
        crawler.export_json()

    report_maker = ReportMaker()

    # Reading from Json files
    list_of_authors = conf.read_from_data("authors.json")
    list_of_articlesJson = pd.read_json(f'{conf.__file__}articles.json')
    list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')

    report_maker.authors(list_of_authors)
    report_maker.articles(list_of_articles)
    report_maker.plotting(list_of_articles)
