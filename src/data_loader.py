import os
import pandas as pd


class DataLoader:
    """
    Loads stock price CSV files from the nested directory /data/data.
    Prepares the data for quantitative analysis.
    """

    def __init__(self, data_dir="../data/data"):
        self.data_dir = data_dir

    def load_stock(self, filename: str) -> pd.DataFrame:
        """Load and clean a single stock CSV file."""
        file_path = os.path.join(self.data_dir, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")

        df = pd.read_csv(file_path)

        # Required columns for TA-Lib
        required = {"Date", "Open", "High", "Low", "Close", "Volume"}
        if not required.issubset(df.columns):
            raise ValueError(f"{filename} must contain columns: {required}")

        # Convert dates
        df["Date"] = pd.to_datetime(df["Date"])

        # Sort chronologically
        df = df.sort_values("Date").reset_index(drop=True)

        # Clean missing values
        df = df.fillna(method="ffill").fillna(method="bfill")

        return df

    def load_all_stocks(self, tickers=None) -> dict:
        """
        Loads all tickers into a dictionary of DataFrames.
        """
        if tickers is None:
            tickers = ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA"]

        data = {}

        for t in tickers:
            filename = f"{t}.csv"
            data[t] = self.load_stock(filename)

        return data
