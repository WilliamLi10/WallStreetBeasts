from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from time import sleep
from stock_analyzer import StockAnalyzer
import csv
from ratelimiting import yfinanceratelimiting,yfinancelongerratelimiting

@dataclass
class AnalyzedStock:
    ticker: str
    recommendation: str
    score: int
    analysis: Dict
    error: Optional[str] = None

class PortfolioAnalyzer:
    def __init__(self, max_workers: int = 5, retry_attempts: int = 3, delay_between_calls: float = 0.2):
        """
        Initialize the PortfolioAnalyzer.

        Args:
            max_workers (int): Maximum number of concurrent threads for stock analysis.
            retry_attempts (int): Number of times to retry failed API calls.
            delay_between_calls (float): Delay between API calls to avoid rate limiting.
        """
        self.max_workers = max_workers
        self.retry_attempts = retry_attempts
        self.delay_between_calls = delay_between_calls

    def _analyze_single_stock(self, ticker: str) -> AnalyzedStock:
        """
        Analyze a single stock with retry logic.

        Args:
            ticker (str): The ticker symbol of the stock to analyze.

        Returns:
            AnalyzedStock: An object containing the analysis results for the stock.
        """
        for attempt in range(self.retry_attempts):
            try:
                # Get stock data
                analysis = StockAnalyzer.analyze_stock(ticker)

                return AnalyzedStock(
                    ticker=ticker,
                    recommendation=analysis['recommendation'],
                    score=analysis['potential_score'],
                    analysis=analysis
                )
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    return AnalyzedStock(
                        ticker=ticker,
                        recommendation="Error",
                        score=0,
                        analysis={},
                        error=str(e)
                    )
                sleep(self.delay_between_calls)

    def analyze_stocks(self, tickers: List[str]) -> Dict[str, List[AnalyzedStock]]:
        """
        Analyze multiple stocks and categorize them by recommendation.

        Args:
            tickers (List[str]): List of stock tickers to analyze.

        Returns:
            Dict[str, List[AnalyzedStock]]: A dictionary mapping recommendation categories to lists of analyzed stocks.
        """
        categorized_stocks = {key: [] for key in ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell', 'Error']}
        processed_count = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_ticker = {
                executor.submit(self._analyze_single_stock, ticker): ticker
                for ticker in tickers
            }

            for future in as_completed(future_to_ticker):
                try:
                    result = future.result()
                    categorized_stocks[result.recommendation].append(result)
                except Exception as e:
                    # Handle any exceptions and categorize as 'Error'
                    ticker = future_to_ticker[future]
                    categorized_stocks['Error'].append(AnalyzedStock(ticker=ticker, recommendation='Error', score=0))

                processed_count += 1

                # Brief pause after every 2 stocks
                if processed_count % yfinanceratelimiting() == 0:
                    sleep(1)

                # Longer pause after every 50 stocks
                if processed_count % yfinancelongerratelimiting() == 0:
                    sleep(5)

                # Additional delay (if any) to manage rate limits
                if self.delay_between_calls > 0:
                    sleep(self.delay_between_calls)

        # Sort stocks within each category by score (absolute value, descending order)
        for category in categorized_stocks:
            categorized_stocks[category].sort(key=lambda x: abs(x.score), reverse=True)

        return categorized_stocks

    def get_summary(self, analyzed_stocks: Dict[str, List[AnalyzedStock]]) -> str:
        """
        Generate a summary of the analysis results.

        Args:
            analyzed_stocks (Dict[str, List[AnalyzedStock]]): A dictionary of analyzed stocks categorized by recommendation.

        Returns:
            str: A summary of the analysis results.
        """
        summary = ["=== Stock Analysis Summary ===\n"]
        categories = ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell', 'Error']

        for category in categories:
            if category in analyzed_stocks:
                stocks = analyzed_stocks[category]
                summary.append(f"{category}: {len(stocks)} stocks")
                for stock in stocks:
                    if stock.error:
                        summary.append(f"  {stock.ticker}: Error - {stock.error}")
                    else:
                        summary.append(f"  {stock.ticker}: Score {stock.score}")
                summary.append("")

        return "\n".join(summary)
if __name__ == "__main__":
    tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    portfolio_analyzer = PortfolioAnalyzer()
    analyzed_stocks = portfolio_analyzer.analyze_stocks(tickers)
    summary = portfolio_analyzer.get_summary(analyzed_stocks)
    print(summary)