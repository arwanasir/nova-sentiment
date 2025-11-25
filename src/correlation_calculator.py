import pandas as pd
from scipy.stats import pearsonr


def calculate_correlation(news_with_sentiment, stock_returns):
    merged = pd.merge(news_with_sentiment, stock_returns, on='Trading_Day')
    correlation, p_value = pearsonr(
        merged['Sentiment'], merged['Daily_Return'])

    return correlation, p_value
