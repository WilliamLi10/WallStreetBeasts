import csv
from typing import List, Dict
import time
from datetime import datetime, timedelta
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from stock_analyzer import StockAnalyzer, StockFormat
from StockData import StockData


class StockAnalyzer:
    def __init__(self):
        """
        Initialize the StockAnalyzer with a hardcoded CSV file containing stock information.
        """
        self.csv_file = 'stock_info.csv'
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

        # Prepare data to write to JSON
        trending_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "most_traded": [
                {"ticker": ticker, "volume": stock.volume}
                for ticker, stock in sorted_stocks[:n]
                if stock is not None
            ]
        }

        # Check if the JSON file needs to be updated
        self._update_trending_json(trending_data)

        return [(ticker, stock.volume) for ticker, stock in sorted_stocks[:n]]

    def _update_trending_json(self, trending_data: dict) -> None:
        """Update the trending_stocks.json file if needed."""
        try:
            # Read the JSON file
            with open('trending_stocks.json', 'r') as file:
                existing_data = json.load(file)

            # Parse timestamp from existing data
            last_updated = datetime.strptime(existing_data["timestamp"], "%Y-%m-%d %H:%M:%S")

            # Check if the timestamp is within the last 3 hours
            if datetime.now() - last_updated < timedelta(hours=3):
                print("Trending stocks are already up-to-date.")
                return
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, proceed to update
            print("Updating trending_stocks.json...")

        # Write new data to the JSON file
        with open('trending_stocks.json', 'w') as file:
            json.dump(trending_data, file, indent=4)
            print("Trending stocks updated.")


if __name__ == "__main__":
    analyzer = StockAnalyzer()
    analyzer.load_stock_data()
    most_traded_stocks = analyzer.get_most_traded_stocks(10)
    for ticker, volume in most_traded_stocks:
        print(f"{ticker}: {volume}")
