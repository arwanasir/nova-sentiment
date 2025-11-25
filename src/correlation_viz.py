import matplotlib.pyplot as plt


def plot_correlation(news_sentiment, stock_returns, correlation_score):
    plt.figure(figsize=(10, 6))
    plt.scatter(news_sentiment, stock_returns, alpha=0.5)
    plt.xlabel('News Sentiment Score')
    plt.ylabel('Stock Daily Return %')
    plt.title(f'Correlation: {correlation_score:.3f}')
    plt.grid(True)
    plt.show()
