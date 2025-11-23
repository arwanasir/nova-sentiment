"""
Financial Metrics for Task 2 Completion
"""
import pandas as pd
import numpy as np


class FinancialMetrics:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.metrics = {}

    def calculate_metrics(self):
        """Calculate essential financial metrics"""
        # Basic returns and volatility
        self.data['Returns'] = self.data['Close'].pct_change()
        self.data['Volatility_20D'] = self.data['Returns'].rolling(
            20).std() * np.sqrt(252)
        self.data['Cumulative_Returns'] = (
            1 + self.data['Returns']).cumprod() - 1
        self.data['Price_SMA_20'] = self.data['Close'].rolling(20).mean()

        self.metrics = {
            'Returns': 'Daily returns',
            'Volatility_20D': '20-day volatility',
            'Cumulative_Returns': 'Cumulative returns',
            'Price_SMA_20': '20-day price SMA'
        }
        return self.data


def calculate_financial_metrics(data):
    calculator = FinancialMetrics(data)
    return calculator.calculate_metrics()
