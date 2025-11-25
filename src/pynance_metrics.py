import pandas as pd
import numpy as np


def calculate_finance_metrics(df):
    """
    Calculate financial metrics - tries PyNance first, falls back to manual calculation
    """
    # Try PyNance first
    try:
        import pynance as pn
        data = pn.data(df)

        metrics = {
            'volatility': data.volatility(),
            'sharpe_ratio': data.sharpe(),
            'max_drawdown': data.drawdown().min(),
            'cumulative_return': data.returns().cumsum().iloc[-1]
        }
        metrics['method'] = 'pynance'
        return metrics

    except:
        # Fallback: Calculate manually
        returns = df['Close'].pct_change().dropna()

        metrics = {
            'volatility': returns.std() * (252 ** 0.5),  # Annualized
            'sharpe_ratio': returns.mean() / returns.std() * (252 ** 0.5),
            'max_drawdown': (df['Close'] / df['Close'].cummax() - 1).min(),
            'cumulative_return': (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
        }
        metrics['method'] = 'manual'
        return metrics
