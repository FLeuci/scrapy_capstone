from rep_mak import ReportMaker
import pandas as pd
import os

list_of_authors = pd.read_json(f"{os.path.dirname(__file__)}/test_data/test-authors.json")
list_of_articlesJson = pd.read_json(f"{os.path.dirname(__file__)}/test_data/test-articles.json")
list_of_articles = list_of_articlesJson.drop_duplicates(subset='title')


def test_authors():
    """
    Tests the authors function
    """
    report_maker = ReportMaker()
    expected = [('Test 1', 2), ('Test 2', 1)]
    assert report_maker.authors(list_of_authors) == expected


def test_articles():
    """
    Tests the articles function
    """
    report_maker = ReportMaker()
    expected = [('title 1', 20200916), ('title 2', 20190916)]
    report_maker.articles(list_of_articles)
    assert report_maker.articles(list_of_articles) == expected


def test_tags():
    """
    Tests the plotting function
    """
    report_maker = ReportMaker()
    expected = [('tag1', 2), ('tag2', 2), ('tag3', 1), ('tag4', 1)]
    assert report_maker.plotting(list_of_articles) == expected
