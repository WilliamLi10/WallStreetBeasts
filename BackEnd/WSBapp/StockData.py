import yfinance as yf
from typing import Optional, List, Union

from pandas import DataFrame, Series


class StockData:
    def __init__(self, ticker: str):
        self.ticker = yf.Ticker(ticker)
        self.info = self.ticker.info


    def get_info(self) -> dict:
        return self.ticker.info

    def get_history(self, period: str = "max") -> DataFrame:
        return self.ticker.history(period=period)

    def get_actions(self) -> DataFrame:
        return self.ticker.actions

    def get_dividends(self) -> Series:
        return self.ticker.dividends

    def get_splits(self) -> Series:
        return self.ticker.splits

    def get_capital_gains(self) -> Series:
        return self.ticker.capital_gains

    def get_shares_full(self, start: str = "2000-01-01", end: Optional[str] = None) -> dict:
        return self.ticker.get_shares_full(start=start, end=end)

    def get_calendar(self) -> dict:
        return self.ticker.calendar

    def get_sec_filings(self) -> dict:
        return self.ticker.sec_filings

    def get_income_stmt(self) -> DataFrame:
        return self.ticker.income_stmt

    def get_quarterly_income_stmt(self) -> DataFrame:
        return self.ticker.quarterly_income_stmt

    def get_balance_sheet(self) -> DataFrame:
        return self.ticker.balance_sheet

    def get_quarterly_balance_sheet(self) -> DataFrame:
        return self.ticker.quarterly_balance_sheet

    def get_cashflow(self) -> DataFrame:
        return self.ticker.cashflow

    def get_quarterly_cashflow(self) -> DataFrame:
        return self.ticker.quarterly_cashflow

    def get_major_holders(self) -> DataFrame:
        return self.ticker.major_holders

    def get_institutional_holders(self) -> DataFrame:
        return self.ticker.institutional_holders

    def get_mutualfund_holders(self) -> DataFrame:
        return self.ticker.mutualfund_holders

    def get_insider_transactions(self) -> DataFrame:
        return self.ticker.insider_transactions

    def get_insider_purchases(self) -> DataFrame:
        return self.ticker.insider_purchases

    def get_insider_roster_holders(self) -> DataFrame:
        return self.ticker.insider_roster_holders

    def get_sustainability(self) -> DataFrame:
        return self.ticker.sustainability

    def get_recommendations(self) -> dict:
        return self.ticker.recommendations

    def get_recommendations_summary(self) -> dict:
        return self.ticker.recommendations_summary

    def get_upgrades_downgrades(self) -> dict:
        return self.ticker.upgrades_downgrades

    def get_analyst_price_targets(self) -> dict:
        return self.ticker.analyst_price_targets

    def get_earnings_estimate(self) -> DataFrame:
        return self.ticker.earnings_estimate

    def get_revenue_estimate(self) -> DataFrame:
        return self.ticker.revenue_estimate

    def get_earnings_history(self) -> DataFrame:
        return self.ticker.earnings_history

    def get_eps_trend(self) -> DataFrame:
        return self.ticker.eps_trend

    def get_eps_revisions(self) -> DataFrame:
        return self.ticker.eps_revisions

    def get_growth_estimates(self) -> DataFrame:
        return self.ticker.growth_estimates

    def get_earnings_dates(self) -> DataFrame:
        return self.ticker.earnings_dates

    def get_isin(self) -> str:
        return self.ticker.isin

    def get_options(self) -> tuple:
        return self.ticker.options

    def get_news(self) -> List[dict]:
        return self.ticker.news

    @property
    def volume(self) -> int:
        return self.info.get('volume', -1)

    @property
    def avg_volume(self) -> int:
        return self.info.get('averageVolume', -1)

    @property
    def pe_ratio(self) -> float:
        return self.info.get('trailingPE', -1.0)

    @property
    def industry_pe_ratio(self) -> float:
        return self.info.get('trailingPeToIndustry', -1.0)

    @property
    def target_est_1y(self) -> float:
        return self.info.get('targetMeanPrice', -1.0)

    @property
    def eps(self) -> float:
        return self.info.get('trailingEps', -1.0)

    @property
    def dividend_yield(self) -> float:
        return self.info.get('dividendYield', -1.0)

    @property
    def debt_to_equity(self) -> float:
        return self.info.get('debtToEquity', -1.0)

    @property
    def current_ratio(self) -> float:
        return self.info.get('currentRatio', -1.0)

    @property
    def price_to_book(self) -> float:
        return self.info.get('priceToBook', -1.0)

    @property
    def return_on_equity(self) -> float:
        return self.info.get('returnOnEquity', -1.0)

    @property
    def free_cash_flow(self) -> float:
        return self.info.get('freeCashflow', -1.0)

    @property
    def beta(self) -> float:
        return self.info.get('beta', -1.0)
    def get_everything(self) -> List[Union[int, float]]:
        """
        Returns a list containing all available stock metrics in a predefined order.

        Returns:
            List[Union[int, float]]: List containing the following metrics in order:
                [volume, avg_volume, pe_ratio, industry_pe_ratio, target_est_1y,
                eps, dividend_yield, debt_to_equity, current_ratio, price_to_book,
                return_on_equity, free_cash_flow, beta]
        """
        return [
            self.volume,
            self.avg_volume,
            self.pe_ratio,
            self.industry_pe_ratio,
            self.target_est_1y,
            self.eps,
            self.dividend_yield,
            self.debt_to_equity,
            self.current_ratio,
            self.price_to_book,
            self.return_on_equity,
            self.free_cash_flow,
            self.beta
        ]

    def __str__(self) -> str:
        return f"StockData for {self.ticker.ticker}"

    def __repr__(self) -> str:
        return self.__str__()
if __name__ == "__main__":
    apple = StockData("AAPL")
    stock_metrics = apple.get_everything()

    assert isinstance(stock_metrics, list)
    assert len(stock_metrics) == 13

    # Print the stock metrics
    print("Apple (AAPL) Stock Metrics:")
    print(f"Volume: {stock_metrics[0]}")
    print(f"Average Volume: {stock_metrics[1]}")
    print(f"P/E Ratio: {stock_metrics[2]}")
    print(f"Industry P/E Ratio: {stock_metrics[3]}")
    print(f"1-Year Target Estimate: ${stock_metrics[4]}")
    print(f"EPS: {stock_metrics[5]}")
    print(f"Dividend Yield: {stock_metrics[6] * 100}%")
    print(f"Debt to Equity: {stock_metrics[7]}")
    print(f"Current Ratio: {stock_metrics[8]}")
    print(f"Price to Book: {stock_metrics[9]}")
    print(f"Return on Equity: {stock_metrics[10] * 100}%")
    print(f"Free Cash Flow: {stock_metrics[11]}")
    print(f"Beta: {stock_metrics[12]}")