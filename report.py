import main.spiders.report_crawler as rc
import main.utils as conf
import pandas as pd
import logging
from main.rep_mak import ReportMaker

logging.basicConfig(filename='test.log', level=logging.INFO)

if __name__ == "__main__":
    if conf.base_path_empty:
        crawler = rc.ReportCrawler()
        crawler.crawl()
        crawler.export_json()

    report_maker = ReportMaker()

    # Reading from Json files
    list_of_authors = pd.read_json(f'{conf.base_path}authors.json')
    list_of_articlesJson = pd.read_json(f'{conf.base_path}articles.json')
    list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')

    report_maker.authors(list_of_authors)
    report_maker.articles(list_of_articles)
    report_maker.plotting(list_of_articles)


