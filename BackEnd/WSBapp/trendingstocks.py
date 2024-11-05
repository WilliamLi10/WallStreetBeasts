import csv
import pandas as pd
from typing import List, Dict
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from stock_analyzer import StockAnalyzer,StockFormat
from StockData import StockData


class StockAnalyzer:
    def __init__(self, csv_file: str):
        """
        Initialize the StockAnalyzer with a CSV file containing stock information.

        Args:
            csv_file (str): Path to the CSV file containing stock information
        """
        self.csv_file = csv_file
        self.tickers: List[str] = []
        self.stock_data: Dict[str, StockData] = {}
        self._load_tickers()

    def _load_tickers(self) -> None:
        """Load ticker symbols from the CSV file."""
        try:
            with open(self.csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                self.tickers = [row['Ticker'] for row in csv_reader]
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find CSV file: {self.csv_file}")
        except KeyError:
            raise KeyError("CSV file must contain a 'Ticker' column")

    def _process_ticker(self, ticker: str) -> tuple[str, StockData]:
        """Process a single ticker symbol and return the ticker and its data."""
        try:
            stock_data = StockData(ticker)
            return ticker, stock_data
        except Exception as e:
            print(f"Error processing ticker {ticker}: {str(e)}")
            return ticker, None

    def load_stock_data(self, max_workers: int = 10) -> None:
        """
        Load stock data for all tickers using parallel processing.

        Args:
            max_workers (int): Maximum number of parallel workers
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(tqdm(
                executor.map(self._process_ticker, self.tickers),
                total=len(self.tickers),
                desc="Loading stock data"
            ))

        self.stock_data = {
            ticker: data for ticker, data in results
            if data is not None
        }

    def get_most_traded_stocks(self, n: int = 10) -> List[tuple[str, int]]:
        """
        Get the n most traded stocks by volume.

        Args:
            n (int): Number of stocks to return

        Returns:
            List[tuple[str, int]]: List of tuples containing (ticker, volume)
        """
        # Sort stocks by volume
        sorted_stocks = sorted(
            self.stock_data.items(),
            key=lambda x: x[1].volume if x[1] is not None else 0,
            reverse=True
        )

        # Return top n stocks
        return [(ticker, stock.volume)
                for ticker, stock in sorted_stocks[:n]
                if stock is not None]

    def print_most_traded_stocks(self, n: int = 10) -> None:
        """
        Print the n most traded stocks in a formatted way.

        Args:
            n (int): Number of stocks to print
        """
        most_traded = self.get_most_traded_stocks(n)

        print(f"\nTop {n} Most Traded Stocks:")
        print("-" * 50)
        print(f"{'Rank':<6}{'Ticker':<10}{'Volume':<15}")
        print("-" * 50)

        for i, (ticker, volume) in enumerate(most_traded, 1):
            print(f"{i:<6}{ticker:<10}{volume:,}<15")
if __name__ == "__main__":
    csv_file = "stock_info.csv"  # replace with your actual CSV file path
    analyzer = StockAnalyzer(csv_file)
    analyzer.load_stock_data()
    analyzer.print_most_traded_stocks(10)