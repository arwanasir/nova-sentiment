import pandas as pd


def load_stock_data():
    apple_data = pd.read_csv('../data/AAPL.csv')
    amazon_data = pd.read_csv('../data/AMZN.csv')
    google_data = pd.read_csv('../data/GOOG.csv')
    meta_data = pd.read_csv('../data/META.csv')
    microsoft_data = pd.read_csv('../data/MSFT.csv')
    nvidia_data = pd.read_csv('../data/NVDA.csv')

    return {
        'AAPL': apple_data,
        'AMZN': amazon_data,
        'GOOG': google_data,
        'META': meta_data,
        'MSFT': microsoft_data,
        'NVDA': nvidia_data,
    }
