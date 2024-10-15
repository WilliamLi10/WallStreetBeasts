import yfinance as yf
from typing import Optional

class StockData:
    def __init__(self, ticker: str):
        self.ticker = yf.Ticker(ticker)
        self.info = self.ticker.info

    @property
    def volume(self) -> int:
        return self.info.get('volume', 0)

    @property
    def avg_volume(self) -> int:
        return self.info.get('averageVolume', 0)

    @property
    def pe_ratio(self) -> float:
        return self.info.get('trailingPE', 0.0)

    @property
    def industry_pe_ratio(self) -> float:
        return self.info.get('trailingPeToIndustry', 0.0)

    @property
    def target_est_1y(self) -> float:
        return self.info.get('targetMeanPrice', 0.0)

    @property
    def eps(self) -> float:
        return self.info.get('trailingEps', 0.0)

    @property
    def dividend_yield(self) -> float:
        return self.info.get('dividendYield', 0.0)

    @property
    def debt_to_equity(self) -> float:
        return self.info.get('debtToEquity', 0.0)

    @property
    def current_ratio(self) -> float:
        return self.info.get('currentRatio', 0.0)

    @property
    def price_to_book(self) -> float:
        return self.info.get('priceToBook', 0.0)

    @property
    def return_on_equity(self) -> float:
        return self.info.get('returnOnEquity', 0.0)

    @property
    def free_cash_flow(self) -> float:
        return self.info.get('freeCashflow', 0.0)

    @property
    def beta(self) -> float:
        return self.info.get('beta', 1.0)

    def __str__(self) -> str:
        return f"StockData for {self.ticker.ticker}"

    def __repr__(self) -> str:
        return self.__str__()