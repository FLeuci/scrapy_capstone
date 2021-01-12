import json
import logging

import matplotlib.pyplot as plt
import pandas as pd
from utils import flatten, count_by_key
import utils as conf



class ReportMaker:
    """
     This class creates a report containing:

    - Top-5 Authors,
    - Top-5 New Articles,
    - Plot with articles counter of 7 most popular tags
    """

    def authors(self, list_of_authors):
        """
        Return the top 5 authors by number of articles in the format list of tuple2
        """
        authors_counter = list_of_authors.groupby("name")["article_title"].count()
        top5_authors = authors_counter.sort_values(ascending=False)
        logging.info('List of 5 best author for number of written articles: \n{}'.format(top5_authors[:5]))
        return self.to_array(top5_authors)[:5]

    def articles(self, list_of_articles):
        """
        Return the top 5 most recent articles in the format list of tuple2
        """
        top5_articles = list_of_articles.loc[:, ['title', 'dateFormatted']]
        top5_articles_sorted = top5_articles.sort_values(by=['dateFormatted'], ascending=False)
        logging.info('List of 5 most recent articles: \n{}'.format(top5_articles_sorted[:5]))
        series = pd.Series(top5_articles_sorted['dateFormatted'].values, index=top5_articles_sorted['title'])
        return self.to_array(series[:5])

    def all_articles(self, list_of_articles):
        all_articles = list_of_articles.loc[:, ['title']]
        conf.write_in_data("all_articles.json", json.dumps(all_articles))

    @staticmethod
    def plotting(list_of_articles):
        """
        Return a list of the 7 most popular tags and save the plot with the relative bar chart under base_path
        """

        all_tags = list(list_of_articles.loc[:, "tags"])

        tags_dict = count_by_key(flatten(all_tags, lambda single_tag: (single_tag, 1)))
        best_tags_dict_sorted = sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)[:7]

        plt.bar([kv[0] for kv in best_tags_dict_sorted], [kv[1] for kv in best_tags_dict_sorted])
        plt.xticks(fontsize=6)
        plt.xlabel('Tags')
        plt.ylabel("Tag's quantity")
        plt.title('Top 7 most popular tags')
        logging.info('Bar chart representing the 5 most popular tags')
        plt.savefig(f"{conf.__file__}plot.png")

        return best_tags_dict_sorted

    @staticmethod
    def to_array(pandas_df):
        """
        - Transform a DataFrame into a dict
        - Return a dict in the format list of key, values
        """
        df_as_dict = pandas_df.to_dict()
        return list(zip(df_as_dict.keys(), df_as_dict.values()))
