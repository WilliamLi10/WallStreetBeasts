import csv
from typing import List, Dict

from BackEnd.WSBapp.StockData import StockData


class UpdateStockInfo:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.stocks_to_keep: List[Dict[str, str]] = []

    def fetch_and_update_stocks(self):
        """Fetch stock data for each ticker in the CSV and remove entries with 404 errors."""
        self._read_csv()
        self._write_csv()
        print("CSV file has been updated.")

    def _read_csv(self):
        """Reads stocks from CSV and attempts to fetch their data."""
        with open(self.csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = row["Ticker"]
                if self._is_valid_stock(ticker):
                    self.stocks_to_keep.append(row)
                else:
                    print(f"Removing ticker {ticker} due to data retrieval error.")

    def _is_valid_stock(self, ticker: str) -> bool:
        stock = StockData(ticker)
        volume = stock.volume  # Attempt to access data to trigger potential errors
        if volume < 0:
            print(f"Invalid stock volume for ticker {ticker}: {volume}")
            return False
        return True
    def _write_csv(self):
        """Writes valid stocks back to the CSV file."""
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Ticker", "Name", "Exchange"])
            writer.writeheader()
            writer.writerows(self.stocks_to_keep)

if __name__ == "__main__":
    updater = UpdateStockInfo("stock_info.csv")
    updater.fetch_and_update_stocks()
