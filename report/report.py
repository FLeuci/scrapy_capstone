import json
from datetime import date

import utils as conf
import logging
from rep_mak import ReportMaker

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    conf.exec_spider('AuthorInfoCrawler')
    conf.exec_spider('ArticleInfoCrawler')
    report_maker = ReportMaker()
    list_of_authors = conf.read_from_data('authors.json', is_pandas=True)
    list_of_articles_json = conf.read_from_data('articles.json', is_pandas=True)
    list_of_articles = list_of_articles_json.drop_duplicates(subset='title')
    last_exec_num = conf.crawl_date[0].get('LastExecutionArticleNum')
    new_articles_num = len(list_of_articles.index)
    if new_articles_num == last_exec_num:
        logging.info("No new articles found")
    else:
        report_maker.authors(list_of_authors)
        report_maker.articles(list_of_articles)
        report_maker.plotting(list_of_articles)
    today_as_string = date.today().strftime('%Y%m%d')
    conf.write_in_data('crawl_checkpoint.json',
                       json.dumps({'LastExecutionDate': today_as_string,
                                   'LastExecutionArticleNum': new_articles_num}))
