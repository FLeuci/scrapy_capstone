import main.spiders.report_crawler as rc
import main.utils as conf
import pandas as pd
import json
import collections
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    if conf.base_path_empty:
        crawler = rc.ReportCrawler()
        crawler.crawl()
        crawler.export_json()


    def removeduplicate(it):
        seen = set()
        for x in it:
            t = tuple(x.items())
            if t not in seen:
                yield x
                seen.add(t)


    list_of_authors = pd.read_json('/Users/fleuci/report/data/authors.json')
    list_of_articlesJson = pd.read_json('/Users/fleuci/report/data/articles.json')
    list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')


    # TOP 5 AUTHORS
    authorsCounter = list_of_authors.groupby("name")["article_title"].count()
    top5_authors = authorsCounter.sort_values(ascending=False)
    print(top5_authors[:5])

    # TOP 5 NEW ARTICLES
    top5_articles = pd.DataFrame(list_of_articles, columns=['title', 'dateFormatted'])
    top5_articles.sort_values(by=['dateFormatted'], inplace=True, ascending=False)
    print(top5_articles[:5])

    # Plot with counts of 7 popular tags:
    # it must be a bar chart (column plot) where each column is for one tag
    # Tag bar must have a name in the plot.
    # X-axis - counter with articles of tag theme
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
    graph = plt.bar(keys[:7], values[:7])
    plt.xticks(fontsize=6)
    plt.xlabel('Tags')
    plt.ylabel("Tag's quantity")
    plt.title('Top 7 most popular tags')
    plt.show()

    # list_of_tags = pd.read_json('/Users/fleuci/main/data/tags.json')
    # print(list_of_tags)

    # articles_authors = list_of_articles.merge(list_of_authors, left_on='author_key', right_on='keyUrl')
    # best_authors = articles_authors.groupby('author_key')['urlFullVersion'].count().sort_values(ascending=False)
    # print(best_authors[:5])

# do main
