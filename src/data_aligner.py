import pandas as pd


def align_dates(news_df, stock_dates):
    news_df['date'] = pd.to_datetime(news_df['date'])
    news_df['Trading_Day'] = news_df['date'].apply(
        lambda x: find_next_trading_day(x, stock_dates))

    return news_df


def find_next_trading_day(news_date, trading_dates):
    """
    Find next stock market day after news
    """
    for date in sorted(trading_dates):
        if date >= news_date:
            return date
    return trading_dates[-1]
