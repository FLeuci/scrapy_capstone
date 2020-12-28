import main.spiders.report_crawler as rc
import main.utils as conf
import pandas as pd
import json
import collections
import matplotlib.pyplot as plt
import logging

logging.basicConfig(filename='test.log', level=logging.INFO)
if __name__ == "__main__":
    if conf.base_path_empty:
        crawler = rc.ReportCrawler()
        crawler.crawl()
        crawler.export_json()

    # Reading from Json files
    list_of_authors = pd.read_json('/Users/fleuci/report/data/authors.json')
    list_of_articlesJson = pd.read_json('/Users/fleuci/report/data/articles.json')
    list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')


class ReportMaker:
    # Getting a list of top 5 authors by number of articles
    def authors(self):
        authorscounter = list_of_authors.groupby("name")["article_title"].count()
        top5_authors = authorscounter.sort_values(ascending=False)
        logging.info('List of 5 best author for number of written articles: \n{}'.format(top5_authors[:5]))
        print(top5_authors[:5])
        return top5_authors[:5]

    # Getting a list of top 5 new articles
    def articles(self):
        top5_articles = pd.DataFrame(list_of_articles, columns=['title', 'dateFormatted'])
        top5_articles.sort_values(by=['dateFormatted'], inplace=True, ascending=False)
        logging.info('List of 5 most recent articles: \n{}'.format(top5_articles[:5]))
        print(top5_articles[:5])

    # Plot with counts of 7 popular tags
    def plotting(self):
        all_tags = list(list_of_articles.loc[:, "tags"])
        count = []
        for tag in all_tags:
            for i in tag:
                count.append(i)

        tag_count = collections.Counter(count)
        keys = []
        values = []
        for key, value in sorted(tag_count.items(), key=lambda value: value[1], reverse=True):
            tags = {'tag': key, 'quantity': value}
            keys.append(key)
            values.append(value)
            with open(f"{conf.base_path}tags.json", "a") as f:
                f.write(json.dumps(tags))
        plt.bar(keys[:7], values[:7])
        plt.xticks(fontsize=6)
        plt.xlabel('Tags')
        plt.ylabel("Tag's quantity")
        plt.title('Top 7 most popular tags')
        logging.info('Bar chart representing the 5 most popular tags')
        plt.savefig(f"{conf.base_path}plot.png")
        plt.show()


report_authors = ReportMaker.authors(list_of_authors)
report_articles = ReportMaker.articles(list_of_articles)
report_plot = ReportMaker.plotting(list_of_articles)


