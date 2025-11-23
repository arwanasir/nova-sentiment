import talib
import pandas as pd


class TechnicalIndicator:
    """
    Computes financial indicators using TA-Lib:
    SMA, RSI, MACD
    """

    def add_indicators(self, df: pd.DataFrame):
        """Add SMA, RSI, MACD to a stock DataFrame."""

        # Moving Averages
        df["SMA_20"] = talib.SMA(df["Close"], timeperiod=20)
        df["SMA_50"] = talib.SMA(df["Close"], timeperiod=50)

        # RSI
        df["RSI_14"] = talib.RSI(df["Close"], timeperiod=14)

        # MACD
        macd, signal, hist = talib.MACD(
            df["Close"],
            fastperiod=12,
            slowperiod=26,
            signalperiod=9
        )
        df["MACD"] = macd
        df["MACD_signal"] = signal
        df["MACD_hist"] = hist

        return df

    def apply_to_all(self, stocks: dict):
        """
        Apply indicators to ALL STOCK DATAFRAMES.
        Input: dict {"AAPL": df, "AMZN": df, ...}
        Output: dict with indicators added
        """
        result = {}

        for ticker, df in stocks.items():
            result[ticker] = self.add_indicators(df.copy())

        return result
