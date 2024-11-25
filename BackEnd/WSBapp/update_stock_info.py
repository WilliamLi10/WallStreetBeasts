import csv
import time
from typing import List, Dict

from BackEnd.WSBapp.StockData import StockData


class UpdateStockInfo:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.stocks_to_keep: List[Dict[str, str]] = []

    def fetch_and_update_stocks(self):
        """Fetch stock data for each ticker in the CSV and remove entries with errors."""
        self._read_csv()
        self._write_csv()

    def _read_csv(self):
        """Reads stocks from CSV and attempts to fetch their data."""
        with open(self.csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            counter = 0

            for row in reader:
                ticker = row["Ticker"]

                if self._is_valid_stock(ticker):
                    self.stocks_to_keep.append(row)
                    # Logging option: Log invalid tickers for debugging instead of printing
                    # Example: logger.info(f"Removing invalid ticker: {ticker}")

                counter += 1

                # Rate limiting to avoid API throttling
                if counter % 2 == 0:
                    time.sleep(1)
                if counter % 100 == 0:
                    # Optionally, log progress every 100 stocks
                    # Example: logger.info(f"Processed {counter} stocks...")
                    time.sleep(5)

    def _is_valid_stock(self, ticker: str) -> bool:
        """Validate stock data by checking if it can be retrieved."""
        try:
            stock = StockData(ticker)
            volume = stock.volume  # Attempt to access data to trigger potential errors
            return volume >= 0  # Return False for negative volumes
        except Exception:
            # Handle specific exceptions if needed
            return False

    def _write_csv(self):
        """Writes valid stocks back to the CSV file."""
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Ticker", "Name", "Exchange"])
            writer.writeheader()
            writer.writerows(self.stocks_to_keep)


if __name__ == "__main__":
    # Optionally, add command-line argument parsing to specify CSV file dynamically
    updater = UpdateStockInfo("stock_info.csv")
    updater.fetch_and_update_stocks()
