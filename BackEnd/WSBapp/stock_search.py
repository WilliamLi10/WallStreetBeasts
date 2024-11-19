import csv


class stock_search:
    def __init__(self,stock_csv:str):
        self.stocks=[]
        self.stock_csv= stock_csv
        self._load_tickers()

    #yoinked from trendingstocks.py
    def _load_tickers(self) -> None:
        """Load ticker symbols from the CSV file."""
        try:
            with open(self.stock_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.stocks .append((row['Ticker'], row['Name']))
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find CSV file: {self.stock_csv}")
        except KeyError:
            raise KeyError("CSV file must contain a 'Ticker' column")
        
    #return set of stocks that contain term as a substring 
    def search(self, term):
        found=[]
        for stock in self.stocks:
            if term.upper() in stock[0].upper() or term.upper() in stock[1].upper():
                found.append(stock)
        return found


if __name__ == "__main__":
    search=stock_search("stock_info.csv")
    #print("seach using term [AA]\nResults: %s" % (temp.search("AA")))
