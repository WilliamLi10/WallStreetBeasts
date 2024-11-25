import yfinance as yf
from typing import Optional, List, Union

from pandas import DataFrame, Series

class StockData:
    def __init__(self, ticker: str):
        self.ticker = yf.Ticker(ticker)
        try:
            self.info = self.ticker.info
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            self.info = {}

    def get_info(self) -> dict:
        """
        Get general information about the stock.

        Returns:
            dict: A dictionary containing stock information.
        """
        return self.ticker.info

    def get_history(self, period: str = "max") -> DataFrame:
        """
        Get historical market data for the stock.

        Args:
            period (str): The period for which to retrieve historical data.

        Returns:
            DataFrame: A DataFrame containing historical market data.
        """
        return self.ticker.history(period=period)

    def get_actions(self) -> DataFrame:
        """
        Get corporate actions data for the stock.

        Returns:
            DataFrame: A DataFrame containing corporate actions data.
        """
        return self.ticker.actions

    def get_dividends(self) -> Series:
        """
        Get dividend data for the stock.

        Returns:
            Series: A Series containing dividend data.
        """
        return self.ticker.dividends

    def get_splits(self) -> Series:
        """
        Get stock split data for the stock.

        Returns:
            Series: A Series containing stock split data.
        """
        return self.ticker.splits

    def get_capital_gains(self) -> Series:
        """
        Get capital gains data for the stock.

        Returns:
            Series: A Series containing capital gains data.
        """
        return self.ticker.capital_gains

    def get_shares_full(self, start: str = "2000-01-01", end: Optional[str] = None) -> dict:
        """
        Get full shares data for the stock.

        Args:
            start (str): The start date for the data.
            end (Optional[str]): The end date for the data.

        Returns:
            dict: A dictionary containing full shares data.
        """
        return self.ticker.get_shares_full(start=start, end=end)

    def get_calendar(self) -> dict:
        """
        Get the stock's calendar data.

        Returns:
            dict: A dictionary containing calendar data.
        """
        return self.ticker.calendar

    def get_sec_filings(self) -> dict:
        """
        Get SEC filings data for the stock.

        Returns:
            dict: A dictionary containing SEC filings data.
        """
        return self.ticker.sec_filings

    def get_income_stmt(self) -> DataFrame:
        """
        Get the income statement for the stock.

        Returns:
            DataFrame: A DataFrame containing the income statement.
        """
        return self.ticker.income_stmt

    def get_quarterly_income_stmt(self) -> DataFrame:
        """
        Get the quarterly income statement for the stock.

        Returns:
            DataFrame: A DataFrame containing the quarterly income statement.
        """
        return self.ticker.quarterly_income_stmt

    def get_balance_sheet(self) -> DataFrame:
        """
        Get the balance sheet for the stock.

        Returns:
            DataFrame: A DataFrame containing the balance sheet.
        """
        return self.ticker.balance_sheet

    def get_quarterly_balance_sheet(self) -> DataFrame:
        """
        Get the quarterly balance sheet for the stock.

        Returns:
            DataFrame: A DataFrame containing the quarterly balance sheet.
        """
        return self.ticker.quarterly_balance_sheet

    def get_cashflow(self) -> DataFrame:
        """
        Get the cash flow statement for the stock.

        Returns:
            DataFrame: A DataFrame containing the cash flow statement.
        """
        return self.ticker.cashflow

    def get_quarterly_cashflow(self) -> DataFrame:
        """
        Get the quarterly cash flow statement for the stock.

        Returns:
            DataFrame: A DataFrame containing the quarterly cash flow statement.
        """
        return self.ticker.quarterly_cashflow

    def get_major_holders(self) -> DataFrame:
        """
        Get the major holders of the stock.

        Returns:
            DataFrame: A DataFrame containing major holders data.
        """
        return self.ticker.major_holders

    def get_institutional_holders(self) -> DataFrame:
        """
        Get the institutional holders of the stock.

        Returns:
            DataFrame: A DataFrame containing institutional holders data.
        """
        return self.ticker.institutional_holders

    def get_mutualfund_holders(self) -> DataFrame:
        """
        Get the mutual fund holders of the stock.

        Returns:
            DataFrame: A DataFrame containing mutual fund holders data.
        """
        return self.ticker.mutualfund_holders

    def get_insider_transactions(self) -> DataFrame:
        """
        Get insider transactions for the stock.

        Returns:
            DataFrame: A DataFrame containing insider transactions data.
        """
        return self.ticker.insider_transactions

    def get_insider_purchases(self) -> DataFrame:
        """
        Get insider purchases for the stock.

        Returns:
            DataFrame: A DataFrame containing insider purchases data.
        """
        return self.ticker.insider_purchases

    def get_insider_roster_holders(self) -> DataFrame:
        """
        Get insider roster holders for the stock.

        Returns:
            DataFrame: A DataFrame containing insider roster holders data.
        """
        return self.ticker.insider_roster_holders

    def get_sustainability(self) -> DataFrame:
        """
        Get sustainability data for the stock.

        Returns:
            DataFrame: A DataFrame containing sustainability data.
        """
        return self.ticker.sustainability

    def get_recommendations(self) -> dict:
        """
        Get recommendations for the stock.

        Returns:
            dict: A dictionary containing recommendations data.
        """
        return self.ticker.recommendations

    def get_recommendations_summary(self) -> dict:
        """
        Get a summary of recommendations for the stock.

        Returns:
            dict: A dictionary containing recommendations summary data.
        """
        return self.ticker.recommendations_summary

    def get_upgrades_downgrades(self) -> dict:
        """
        Get upgrades and downgrades for the stock.

        Returns:
            dict: A dictionary containing upgrades and downgrades data.
        """
        return self.ticker.upgrades_downgrades

    def get_analyst_price_targets(self) -> dict:
        """
        Get analyst price targets for the stock.

        Returns:
            dict: A dictionary containing analyst price targets data.
        """
        return self.ticker.analyst_price_targets

    def get_earnings_estimate(self) -> DataFrame:
        """
        Get earnings estimates for the stock.

        Returns:
            DataFrame: A DataFrame containing earnings estimates.
        """
        return self.ticker.earnings_estimate

    def get_revenue_estimate(self) -> DataFrame:
        """
        Get revenue estimates for the stock.

        Returns:
            DataFrame: A DataFrame containing revenue estimates.
        """
        return self.ticker.revenue_estimate

    def get_earnings_history(self) -> DataFrame:
        """
        Get earnings history for the stock.

        Returns:
            DataFrame: A DataFrame containing earnings history.
        """
        return self.ticker.earnings_history

    def get_eps_trend(self) -> DataFrame:
        """
        Get EPS trend for the stock.

        Returns:
            DataFrame: A DataFrame containing EPS trend.
        """
        return self.ticker.eps_trend

    def get_eps_revisions(self) -> DataFrame:
        """
        Get EPS revisions for the stock.

        Returns:
            DataFrame: A DataFrame containing EPS revisions.
        """
        return self.ticker.eps_revisions

    def get_growth_estimates(self) -> DataFrame:
        """
        Get growth estimates for the stock.

        Returns:
            DataFrame: A DataFrame containing growth estimates.
        """
        return self.ticker.growth_estimates

    def get_earnings_dates(self) -> DataFrame:
        """
        Get earnings dates for the stock.

        Returns:
            DataFrame: A DataFrame containing earnings dates.
        """
        return self.ticker.earnings_dates

    def get_isin(self) -> str:
        """
        Get the ISIN for the stock.

        Returns:
            str: The ISIN of the stock.
        """
        return self.ticker.isin

    def get_options(self) -> tuple:
        """
        Get options data for the stock.

        Returns:
            tuple: A tuple containing options data.
        """
        return self.ticker.options

    def get_news(self) -> List[dict]:
        """
        Get news articles related to the stock.

        Returns:
            List[dict]: A list of dictionaries containing news articles.
        """
        return self.ticker.news

    @property
    def volume(self) -> int:
        """
        Get the current trading volume of the stock.

        Returns:
            int: The current trading volume.
        """
        return self.info.get('volume', -1)

    @property
    def avg_volume(self) -> int:
        """
        Get the average trading volume of the stock.

        Returns:
            int: The average trading volume.
        """
        return self.info.get('averageVolume', -1)

    @property
    def pe_ratio(self) -> float:
        """
        Get the price-to-earnings ratio of the stock.

        Returns:
            float: The price-to-earnings ratio.
        """
        return self.info.get('trailingPE', -1.0)

    @property
    def industry_pe_ratio(self) -> float:
        """
        Get the industry price-to-earnings ratio.

        Returns:
            float: The industry price-to-earnings ratio.
        """
        return self.info.get('trailingPeToIndustry', -1.0)

    @property
    def target_est_1y(self) -> float:
        """
        Get the 1-year target estimate for the stock.

        Returns:
            float: The 1-year target estimate.
        """
        return self.info.get('targetMeanPrice', -1.0)

    @property
    def eps(self) -> float:
        """
        Get the earnings per share of the stock.

        Returns:
            float: The earnings per share.
        """
        return self.info.get('trailingEps', -1.0)

    @property
    def dividend_yield(self) -> float:
        """
        Get the dividend yield of the stock.

        Returns:
            float: The dividend yield.
        """
        return self.info.get('dividendYield', -1.0)

    @property
    def debt_to_equity(self) -> float:
        """
        Get the debt-to-equity ratio of the stock.

        Returns:
            float: The debt-to-equity ratio.
        """
        return self.info.get('debtToEquity', -1.0)

    @property
    def current_ratio(self) -> float:
        """
        Get the current ratio of the stock.

        Returns:
            float: The current ratio.
        """
        return self.info.get('currentRatio', -1.0)

    @property
    def price_to_book(self) -> float:
        """
        Get the price-to-book ratio of the stock.

        Returns:
            float: The price-to-book ratio.
        """
        return self.info.get('priceToBook', -1.0)

    @property
    def return_on_equity(self) -> float:
        """
        Get the return on equity of the stock.

        Returns:
            float: The return on equity.
        """
        return self.info.get('returnOnEquity', -1.0)

    @property
    def free_cash_flow(self) -> float:
        """
        Get the free cash flow of the stock.

        Returns:
            float: The free cash flow.
        """
        return self.info.get('freeCashflow', -1.0)

    @property
    def beta(self) -> float:
        """
        Get the beta value of the stock.

        Returns:
            float: The beta value.
        """
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
        """
        String representation of the StockData object.

        Returns:
            str: A string representation of the StockData object.
        """
        return f"StockData for {self.ticker.ticker}"

    def __repr__(self) -> str:
        """
        Official string representation of the StockData object.

        Returns:
            str: A string representation of the StockData object.
        """
        return self.__str__()
# Example usage :

#if __name__ == "__main__":
    #apple = StockData("AAPL")
    #stock_metrics = apple.get_everything()

    # Validate that the stock metrics list is as expected
    # assert isinstance(stock_metrics, list)
    # assert len(stock_metrics) == 13

    # Example usage of the StockData class:
    # Uncomment the following to test and display Apple stock metrics:
    # print("Apple (AAPL) Stock Metrics:")
    # print(f"Volume: {stock_metrics[0]}")
    # print(f"Average Volume: {stock_metrics[1]}")
    # print(f"P/E Ratio: {stock_metrics[2]}")
    # print(f"Industry P/E Ratio: {stock_metrics[3]}")
    # print(f"1-Year Target Estimate: ${stock_metrics[4]}")
    # print(f"EPS: {stock_metrics[5]}")
    # print(f"Dividend Yield: {stock_metrics[6] * 100}%")
    # print(f"Debt to Equity: {stock_metrics[7]}")
    # print(f"Current Ratio: {stock_metrics[8]}")
    # print(f"Price to Book: {stock_metrics[9]}")
    # print(f"Return on Equity: {stock_metrics[10] * 100}%")
    # print(f"Free Cash Flow: {stock_metrics[11]}")
    # print(f"Beta: {stock_metrics[12]}")
