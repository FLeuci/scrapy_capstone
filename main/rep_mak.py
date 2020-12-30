import json
import collections
import matplotlib.pyplot as plt
import main.utils as conf
import pandas as pd
import logging


class ReportMaker:

    # Getting a list of top 5 authors by number of articles
    def authors(self, list_of_authors):
        authors_counter = list_of_authors.groupby("name")["article_title"].count()
        top5_authors = authors_counter.sort_values(ascending=False)
        logging.info('List of 5 best author for number of written articles: \n{}'.format(top5_authors[:5]))
        return self.to_array(top5_authors)[:5]

    # Getting a list of top 5 new articles
    def articles(self, list_of_articles):
        top5_articles = list_of_articles.loc[:, ['title', 'dateFormatted']]
        top5_articles_sorted = top5_articles.sort_values(by=['dateFormatted'], ascending=False)
        logging.info('List of 5 most recent articles: \n{}'.format(top5_articles_sorted[:5]))
        series = pd.Series(top5_articles_sorted['dateFormatted'].values, index=top5_articles_sorted['title'])
        return self.to_array(series[:5])

    # Plot with counts of 7 popular tags
    def plotting(self, list_of_articles):
        global tags
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

        return tags

    def to_array(self, pandas_df):
        df_as_dict = pandas_df.to_dict()
        return list(zip(df_as_dict.keys(), df_as_dict.values()))
