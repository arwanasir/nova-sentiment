import talib
import pandas as pd


def calculate_indicators(close_prices):
    close = close_prices

    MA_20 = talib.SMA(close, timeperiod=20)
    MA_50 = talib.SMA(close, timeperiod=50)
    RSI_14 = talib.RSI(close, timeperiod=14)
    MACD, MACD_Signal, MACD_Hist = talib.MACD(close)
    return {
        'MA_20': MA_20,
        'MA_50': MA_50,
        'RSI_14': RSI_14,
        'MACD': MACD,
        'MACD_Signal': MACD_Signal,
        'MACD_Hist': MACD_Hist}
