from textblob import TextBlob


def add_sentiments(news_df):
    news_df['sentiment'] = news_df['headline'].apply(
        lambda x: TextBlob(x).sentiment.polarity
    )

    return news_df
