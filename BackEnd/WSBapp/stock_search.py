import csv
from typing import List, Tuple


class stock_search:
    def __init__(self):
        """
               Initialize the StockSearch class with a hardcoded CSV file containing stock data.
               """
        self.stocks: List[Tuple[str, str]] = []
        self.stock_csv = 'stock_info.csv'
        self._load_tickers()

    #yoinked from trendingstocks.py
    def _load_tickers(self) -> None:
        """
                Load ticker symbols and stock names from the CSV file.

                Raises:
                    FileNotFoundError: If the CSV file does not exist.
                    KeyError: If the required columns ('Ticker', 'Name') are missing.
                """
        try:
            with open(self.stock_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                self.stocks = [(row['Ticker'], row['Name']) for row in csv_reader]
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find CSV file: {self.stock_csv}")
        except KeyError:
            raise KeyError("CSV file must contain 'Ticker' and 'Name' columns")

    #return set of stocks that contain term as a substring
    def search(self, term: str) -> List[Tuple[str, str]]:
        """
        Search for stocks where the ticker or name contains the given term.

        Args:
            term (str): The search term to look for.

        Returns:
            List[Tuple[str, str]]: List of stocks (ticker, name) that match the search term.
        """
        term = term.upper()
        return [
            stock for stock in self.stocks
            if term in stock[0].upper() or term in stock[1].upper()
        ]



if __name__ == "__main__":
    search = stock_search()
    # Example search term: "AA"
    results = search.search("AA")
    print(f"Search results for 'AA': {results}")
