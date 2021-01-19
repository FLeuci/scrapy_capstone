import utils as conf
import logging
from rep_mak import ReportMaker


logging.basicConfig(level=logging.INFO)


def crawl():
    conf.exec_spider('AuthorInfoCrawler')
    conf.exec_spider('ArticleInfoCrawler')

    report_maker = ReportMaker()
    list_of_authors = conf.read_from_data('authors.json')
    list_of_articles_json = conf.read_from_data('articles.json')
    list_of_articles = list_of_articles_json.drop_duplicates(subset='title')
    report_maker.authors(list_of_authors)
    report_maker.articles(list_of_articles)
    report_maker.plotting(list_of_articles)


if __name__ == "__main__":
    if not conf.path_exist('articles.json'):
        crawl()
    else:
        with open(f'{conf.base_path}/all_articles.json', 'rb') as f:
            old_articles = list(map(lambda x: x.rstrip().decode("utf-8"), f.readlines()))

        conf.exec_spider('ArticlesCheckCrawler')

        with open(f'{conf.base_path}/all_articles.json', 'rb') as f:
            new_articles = list(map(lambda x: x.rstrip().decode("utf-8"), f.readlines()))

        flag = True
        for new_art in new_articles:
            flag = new_art in old_articles
        if not flag:
            crawl()
        else:
            logging.info("No new articles found")
