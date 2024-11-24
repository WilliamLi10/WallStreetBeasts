import csv
import pandas as pd
from typing import List, Dict
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from stock_analyzer import StockAnalyzer,StockFormat
from StockData import StockData
import time


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
            results = []
            request_count = 0
            for result in tqdm(
                    executor.map(self._process_ticker, self.tickers),
                    total=len(self.tickers),
                    desc="Loading stock data"
            ):
                results.append(result)
                request_count += 1
                if request_count % 5 == 0:
                    time.sleep(1)  # Add a one-second break after every 5 requests

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

        # Save the current date and time to trending_stocks.json after deleting everything inside of it
        with open('trending_stocks.json', 'w') as file:
             file.write('')
             file.close()
        # Save the current date and time to trending_stocks.json
        with open('trending_stocks.json', 'a') as file:
            file.write(time.strftime("%Y-%m-%d %H:%M:%S") + '\n')
            file.close()
        # Return the n most traded stocks to trending_stocks.json
        with open('trending_stocks.json', 'a') as file:
            for ticker, stock in sorted_stocks[:n]:
                if stock is not None:
                    file.write(f"{ticker}: {stock.volume}\n")
            file.close()
        return [(ticker, stock.volume) for ticker, stock in sorted_stocks[:n]]
def main():
    csv_file = 'stock_info.csv'
    analyzer = StockAnalyzer(csv_file)
    analyzer.load_stock_data()
    most_traded_stocks = analyzer.get_most_traded_stocks(10)
    for ticker, volume in most_traded_stocks:
        print(f"{ticker}: {volume}")

if __name__ == "__main__":
    main()