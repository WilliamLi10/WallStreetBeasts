import csv
from typing import List, Dict
import time
from tqdm import tqdm
from time import sleep
from datetime import datetime, timedelta
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from StockData import StockData
class StockAnalyzer:
    def __init__(self):
        # Initialization remains the same
        self.csv_file = 'stock_info.csv'
        self.tickers: List[str] = []
        self.stock_data: Dict[str, StockData] = {}
        self._load_tickers()

    def _load_tickers(self) -> None:
        # Ticker loading remains the same
        try:
            with open(self.csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                self.tickers = [row['Ticker'] for row in csv_reader]
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find CSV file: {self.csv_file}")
        except KeyError:
            raise KeyError("CSV file must contain a 'Ticker' column")

    def _process_ticker(self, ticker: str) -> StockData:
        """Process a single ticker and return its StockData object."""
        try:
            return StockData(ticker)
        except Exception as e:
            print(f"Error processing ticker {ticker}: {str(e)}")
            return None

    def load_stock_data(self) -> None:
        """Load stock data for all tickers."""
        for idx, ticker in enumerate(tqdm(self.tickers, desc="Loading stock data"), start=1):
            stock_data = self._process_ticker(ticker)
            if stock_data:
                self.stock_data[ticker] = stock_data
            if idx % 5 == 0:  # Add a delay every 7 stocks
                time.sleep(1)

    def get_most_traded_stocks(self, n: int = 10) -> List[tuple[str, int]]:
        """Get the n most traded stocks by volume."""
        # Load the stock data
        self.load_stock_data()

        # Sort and retrieve the top `n` stocks by volume
        sorted_stocks = sorted(
            self.stock_data.items(),
            key=lambda item: item[1].volume if item[1] else 0,
            reverse=True
        )
        # Return the top n tickers with their volumes
        return [(ticker, stock.volume) for ticker, stock in sorted_stocks[:n]]

    def _update_trending_json(self) -> None:
        """Update the trending_stocks.json file."""
        trending_data = self.get_most_traded_stocks(10)
        try:
            with open('trending_stocks.json', 'r') as file:
                existing_data = json.load(file)
            last_updated = datetime.strptime(existing_data.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
            if datetime.now() - last_updated < timedelta(hours=3):
                return
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            pass
        with open('trending_stocks.json', 'w') as file:
            json.dump({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data": trending_data}, file, indent=4)

if __name__ == "__main__":
    analyzer = StockAnalyzer()
    analyzer._update_trending_json()
