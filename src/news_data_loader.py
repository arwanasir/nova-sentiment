import pandas as pd


def load_news_data():
    news = pd.read_csv('../data/raw_analyst_ratings.csv')

    return news
