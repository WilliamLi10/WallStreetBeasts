from typing import Dict, List, Optional
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from time import sleep
from .stock_analyzer import StockAnalyzer, StockFormat
from .StockData import StockData


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
            max_workers: Maximum number of concurrent threads for stock analysis
            retry_attempts: Number of times to retry failed API calls
            delay_between_calls: Delay between API calls to avoid rate limiting
        """
        self.max_workers = max_workers
        self.retry_attempts = retry_attempts
        self.delay_between_calls = delay_between_calls

    def _analyze_single_stock(self, ticker: str) -> AnalyzedStock:
        """Analyze a single stock with retry logic."""
        for attempt in range(self.retry_attempts):
            try:
                # Get stock data
                stock_data = StockData(ticker)
                metrics = stock_data.get_everything()

                # Convert to StockFormat
                stock = StockFormat(
                    ticker=ticker,
                    volume=metrics[0],
                    avg_volume=metrics[1],
                    pe_ratio=metrics[2],
                    industry_pe_ratio=metrics[3],
                    target_est_1y=metrics[4],
                    eps=metrics[5],
                    dividend_yield=metrics[6],
                    debt_to_equity=metrics[7],
                    current_ratio=metrics[8],
                    price_to_book=metrics[9],
                    return_on_equity=metrics[10],
                    free_cash_flow=metrics[11],
                    beta=metrics[12]
                )

                # Analyze the stock
                analysis = StockAnalyzer.analyze_stock(stock)

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
            tickers: List of stock tickers to analyze

        Returns:
            Dict mapping recommendation categories to lists of analyzed stocks
        """
        categorized_stocks = defaultdict(list)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all analysis tasks
            future_to_ticker = {
                executor.submit(self._analyze_single_stock, ticker): ticker
                for ticker in tickers
            }

            # Process results as they complete
            for future in as_completed(future_to_ticker):
                result = future.result()
                categorized_stocks[result.recommendation].append(result)
                sleep(self.delay_between_calls)  # Rate limiting

        # Sort stocks within each category by score
        for category in categorized_stocks:
            categorized_stocks[category].sort(key=lambda x: abs(x.score), reverse=True)

        return dict(categorized_stocks)

    def get_summary(self, analyzed_stocks: Dict[str, List[AnalyzedStock]]) -> str:
        """Generate a summary of the analysis results."""
        summary = []
        summary.append("=== Stock Analysis Summary ===\n")

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