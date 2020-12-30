import json
import logging

import matplotlib.pyplot as plt
import pandas as pd

import main.utils as conf


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
        from main.utils import flatten, reduce_by_key

        all_tags = list(list_of_articles.loc[:, "tags"])

        tags_dict = reduce_by_key(flatten(all_tags, lambda single_tag: (single_tag, 1)))
        best_tags_dict_sorted = sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)[:7]
        with open(f"{conf.base_path}tags.json", "w") as f:
            f.write(json.dumps(best_tags_dict_sorted))
        plt.bar([kv[0] for kv in best_tags_dict_sorted], [kv[1] for kv in best_tags_dict_sorted])
        plt.xticks(fontsize=6)
        plt.xlabel('Tags')
        plt.ylabel("Tag's quantity")
        plt.title('Top 7 most popular tags')
        logging.info('Bar chart representing the 5 most popular tags')
        plt.savefig(f"{conf.base_path}plot.png")
        plt.show()

        return best_tags_dict_sorted

    def to_array(self, pandas_df):
        df_as_dict = pandas_df.to_dict()
        return list(zip(df_as_dict.keys(), df_as_dict.values()))
