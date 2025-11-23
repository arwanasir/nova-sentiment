"""
Module for visualizing technical indicators and financial metrics for ALL stocks - FIXED
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict
import warnings
warnings.filterwarnings('ignore')


class StockVisualizer:
    """
    Creates visualizations for technical indicators and financial metrics for ALL stocks
    """

    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.fig_size = (15, 10)

    def plot_technical_indicators(self, df: pd.DataFrame, ticker: str):
        """
        Create comprehensive visualization for technical indicators
        """
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        fig.suptitle(
            f'TECHNICAL ANALYSIS - {ticker}', fontsize=16, fontweight='bold')

        # Plot 1: Price and Moving Averages
        axes[0].plot(df['Date'], df['Close'], label='Close Price',
                     linewidth=2, color='black')
        if 'SMA_20' in df.columns:
            axes[0].plot(df['Date'], df['SMA_20'],
                         label='SMA 20', alpha=0.7, color='blue')
        if 'SMA_50' in df.columns:
            axes[0].plot(df['Date'], df['SMA_50'],
                         label='SMA 50', alpha=0.7, color='red')
        axes[0].set_title('Price and Moving Averages')
        axes[0].set_ylabel('Price ($)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Plot 2: RSI
        if 'RSI_14' in df.columns:
            axes[1].plot(df['Date'], df['RSI_14'], label='RSI 14',
                         color='orange', linewidth=2)
            axes[1].axhline(y=70, color='r', linestyle='--',
                            alpha=0.7, label='Overbought (70)')
            axes[1].axhline(y=30, color='g', linestyle='--',
                            alpha=0.7, label='Oversold (30)')
            axes[1].axhline(y=50, color='gray', linestyle='-', alpha=0.3)
            axes[1].set_title('Relative Strength Index (RSI)')
            axes[1].set_ylabel('RSI')
            axes[1].set_ylim(0, 100)
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)

        # Plot 3: MACD
        if all(col in df.columns for col in ['MACD', 'MACD_signal']):
            axes[2].plot(df['Date'], df['MACD'], label='MACD',
                         color='blue', linewidth=2)
            axes[2].plot(df['Date'], df['MACD_signal'],
                         label='Signal Line', color='red', linewidth=2)
            # Plot histogram
            colors = ['green' if x >= 0 else 'red' for x in df['MACD_hist']]
            axes[2].bar(df['Date'], df['MACD_hist'], alpha=0.3, color=colors)
            axes[2].axhline(y=0, color='black', linestyle='-', alpha=0.5)
            axes[2].set_title('MACD Indicator')
            axes[2].set_ylabel('MACD')
            axes[2].legend()
            axes[2].grid(True, alpha=0.3)

        # Plot 4: Volume
        if 'Volume' in df.columns:
            axes[3].bar(df['Date'], df['Volume'], alpha=0.7,
                        color='purple', label='Volume')
            axes[3].set_title('Trading Volume')
            axes[3].set_ylabel('Volume')
            axes[3].legend()
            axes[3].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def plot_pynance_metrics(self, df: pd.DataFrame, ticker: str):
        """
        Create visualization for PyNance financial metrics
        """
        pynance_cols = [col for col in df.columns if col.startswith('Pn_')]

        if not pynance_cols:
            print(f"   No PyNance metrics found for {ticker}")
            return

        # Select key PyNance metrics for visualization
        key_metrics = []
        metric_priority = ['Pn_Volatility_30D', 'Pn_Sharpe_30D', 'Pn_Max_Drawdown',
                           'Pn_Cumulative_Returns', 'Pn_Returns', 'Pn_Rolling_Mean_20']

        for metric in metric_priority:
            if metric in df.columns:
                key_metrics.append(metric)
                if len(key_metrics) >= 4:  # Show max 4 metrics
                    break

        if not key_metrics:
            return

        n_plots = len(key_metrics)
        fig, axes = plt.subplots(n_plots, 1, figsize=(15, 3*n_plots))
        fig.suptitle(
            f'PYNANCE FINANCIAL METRICS - {ticker}', fontsize=16, fontweight='bold')

        if n_plots == 1:
            axes = [axes]

        colors = ['red', 'blue', 'green', 'orange']

        for i, metric in enumerate(key_metrics):
            ax = axes[i]
            color = colors[i % len(colors)]
            ax.plot(df['Date'], df[metric], linewidth=2,
                    label=metric, color=color)
            ax.set_title(f'{metric}')
            ax.set_ylabel('Value')
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Add zero line for metrics that can be positive/negative
            if any(x in metric for x in ['Returns', 'Sharpe', 'Drawdown']):
                ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)

        plt.tight_layout()
        plt.show()

    def create_summary_dashboard(self, stocks_dict: Dict, ticker: str):
        """
        Create a complete dashboard for a single stock
        """
        if ticker not in stocks_dict:
            print(f"Ticker {ticker} not found in data")
            return

        df = stocks_dict[ticker]

        print(f"🎯 TECHNICAL ANALYSIS DASHBOARD - {ticker}")
        print("=" * 60)

        # Plot technical indicators
        self.plot_technical_indicators(df, ticker)

        # Plot PyNance metrics if available
        self.plot_pynance_metrics(df, ticker)

        # Print latest values
        self.print_latest_values(df, ticker)

        print("\n" + "=" * 60 + "\n")

    def print_latest_values(self, df: pd.DataFrame, ticker: str):
        """
        Print latest indicator values with interpretations
        """
        latest = df.iloc[-1]

        print(f"📈 LATEST INDICATOR VALUES - {ticker}")
        print("-" * 40)

        # Price
        print(f"💰 Current Price: ${latest['Close']:.2f}")

        # Moving Averages
        if 'SMA_20' in df.columns and 'SMA_50' in df.columns:
            sma_signal = "BULLISH" if latest['SMA_20'] > latest['SMA_50'] else "BEARISH"
            print(f"📊 Moving Average Signal: {sma_signal}")
            print(f"   20-day SMA: ${latest['SMA_20']:.2f}")
            print(f"   50-day SMA: ${latest['SMA_50']:.2f}")

        # RSI
        if 'RSI_14' in df.columns:
            rsi_status = "OVERSOLD" if latest['RSI_14'] < 30 else "OVERBOUGHT" if latest['RSI_14'] > 70 else "NEUTRAL"
            print(f"🎯 RSI (14): {latest['RSI_14']:.1f} - {rsi_status}")

        # MACD
        if all(col in df.columns for col in ['MACD', 'MACD_signal']):
            macd_signal = "BULLISH" if latest['MACD'] > latest['MACD_signal'] else "BEARISH"
            print(f"📉 MACD Signal: {macd_signal}")
            print(
                f"   MACD: {latest['MACD']:.3f}, Signal: {latest['MACD_signal']:.3f}")

        # PyNance Metrics
        pynance_metrics = [col for col in df.columns if col.startswith('Pn_')]
        if pynance_metrics:
            print(f"📊 PYNANCE METRICS:")
            for metric in pynance_metrics[:4]:  # Show first 4
                if pd.notna(latest[metric]):
                    value = latest[metric]
                    if 'Returns' in metric:
                        print(f"   • {metric}: {value:.2%}")
                    elif 'Volatility' in metric:
                        print(f"   • {metric}: {value:.2%}")
                    else:
                        print(f"   • {metric}: {value:.4f}")

# FIXED: This function now explicitly processes ALL stocks


def create_visualizations(stocks_dict: Dict):
    """
    Create visualizations for ALL stocks in the dictionary - FIXED VERSION
    """
    tickers = list(stocks_dict.keys())

    print(f"📊 CREATING TECHNICAL ANALYSIS DASHBOARDS")
    print(f"🎯 PROCESSING ALL {len(tickers)} STOCKS")
    print("=" * 60)
    print(f"📋 STOCKS TO PROCESS: {', '.join(tickers)}")
    print("=" * 60)

    visualizer = StockVisualizer()

    # EXPLICITLY loop through ALL tickers
    for i, ticker in enumerate(tickers, 1):
        print(f"\n{'='*60}")
        print(f"📈 [{i}/{len(tickers)}] ANALYZING {ticker}...")
        print(f"{'='*60}")

        # Force the visualization for this specific ticker
        visualizer.create_summary_dashboard(stocks_dict, ticker)

        print(f"✅ COMPLETED: {ticker} dashboard created")

    print(f"\n{'='*60}")
    print(
        f"✅ COMPLETED: Technical analysis dashboards created for ALL {len(tickers)} stocks!")
    print(f"📋 Stocks analyzed: {', '.join(tickers)}")
    print(f"{'='*60}")
