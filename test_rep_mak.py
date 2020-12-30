from main.rep_mak import ReportMaker
import pandas as pd

list_of_authors = pd.read_json('/Users/fleuci/report/data/test-authors.json')
list_of_articlesJson = pd.read_json('/Users/fleuci/report/data/test-articles.json')
list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')


def test_authors():
    report_maker = ReportMaker()
    expected = [('Test 1', 2), ('Test 2', 1)]
    assert report_maker.authors(list_of_authors) == expected


def test_articles():
    report_maker = ReportMaker()
    expected = [('title 1', 20200916), ('title 2', 20190916)]
    report_maker.articles(list_of_articles)
    assert report_maker.articles(list_of_articles) == expected


def test_tags():
    report_maker = ReportMaker()
    expected = {'quantity': 1, 'tag': 'tag4'}
    assert report_maker.plotting(list_of_articles) == expected
