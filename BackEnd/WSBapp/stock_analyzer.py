from dataclasses import dataclass
from typing import Dict, Any
import yfinance as yf

# Industry PE ratios
INDUSTRY_PE_RATIOS = {
    "Technology": 25.4,
    "Healthcare": 18.3,
    "Consumer Discretionary": 22.1,
    "Energy": 15.2,
    "Financials": 14.7,
    "Industrials": 19.5,
    "Materials": 17.8,
    "Real Estate": 21.6,
    "Utilities": 16.3,
    "Telecommunication Services": 20.2,
    "Consumer Staples": 18.9,
}

@dataclass
class StockFormat:
    ticker: str
    volume: int
    avg_volume: int
    pe_ratio: float
    industry_pe_ratio: float
    target_est_1y: float
    eps: float
    dividend_yield: float = 0.0
    debt_to_equity: float = 0.0
    current_ratio: float = 0.0
    price_to_book: float = 0.0
    return_on_equity: float = 0.0
    free_cash_flow: float = 0.0
    beta: float = 1.0
    industry: str = "Unknown"

    @property
    def current_price(self) -> float:
        """
        Calculate the current price of the stock.

        Returns:
            float: The current price of the stock.
        """
        return self.pe_ratio * self.eps

class StockData:
    def __init__(self, ticker: str):
        """
        Fetch stock data using yfinance.

        Args:
            ticker (str): The stock ticker.
        """
        self.ticker = ticker
        stock_info = yf.Ticker(ticker).info

        self.volume = stock_info.get('volume', 0)
        self.avg_volume = stock_info.get('averageVolume', 0)
        self.pe_ratio = stock_info.get('trailingPE', 0.0)
        self.industry_pe_ratio = self._get_industry_pe_ratio(stock_info.get('industry', 'Unknown'))
        self.target_est_1y = stock_info.get('targetMeanPrice', 0.0)
        self.eps = stock_info.get('trailingEps', 0.0)
        self.dividend_yield = stock_info.get('dividendYield', 0.0) * 100 if stock_info.get('dividendYield') else 0.0
        self.debt_to_equity = stock_info.get('debtToEquity', 0.0)
        self.current_ratio = stock_info.get('currentRatio', 0.0)
        self.price_to_book = stock_info.get('priceToBook', 0.0)
        self.return_on_equity = stock_info.get('returnOnEquity', 0.0) * 100 if stock_info.get('returnOnEquity') else 0.0
        self.free_cash_flow = stock_info.get('freeCashflow', 0.0) / 1e9 if stock_info.get('freeCashflow') else 0.0
        self.beta = stock_info.get('beta', 1.0)
        self.industry = stock_info.get('industry', 'Unknown')

    @staticmethod
    def _get_industry_pe_ratio(industry: str) -> float:
        """
        Get the PE ratio for the given industry.

        Args:
            industry (str): The industry name.

        Returns:
            float: The industry PE ratio.
        """
        return INDUSTRY_PE_RATIOS.get(industry, 15.0)  # Default to 15 if industry is unknown

class StockAnalyzer:
    @staticmethod
    def analyze_stock(ticker: str) -> Dict[str, Any]:
        """
        Analyze a stock based on its ticker symbol.

        Args:
            ticker (str): The ticker symbol of the stock.

        Returns:
            Dict[str, Any]: A dictionary containing the analysis results.
        """
        stock_data = StockData(ticker)
        stock_format = StockFormat(
            ticker=ticker,
            volume=stock_data.volume,
            avg_volume=stock_data.avg_volume,
            pe_ratio=stock_data.pe_ratio,
            industry_pe_ratio=stock_data.industry_pe_ratio,
            target_est_1y=stock_data.target_est_1y,
            eps=stock_data.eps,
            dividend_yield=stock_data.dividend_yield,
            debt_to_equity=stock_data.debt_to_equity,
            current_ratio=stock_data.current_ratio,
            price_to_book=stock_data.price_to_book,
            return_on_equity=stock_data.return_on_equity,
            free_cash_flow=stock_data.free_cash_flow,
            beta=stock_data.beta,
            industry=stock_data.industry
        )
        return StockAnalyzer.analyze_stock_format(stock_format)

    @staticmethod
    def analyze_stock_format(stock: StockFormat) -> Dict[str, Any]:
        """
        Analyze a stock based on its formatted data.

        Args:
            stock (StockFormat): The formatted stock data.

        Returns:
            Dict[str, Any]: A dictionary containing the analysis results.
        """
        analysis = {}
        potential_score = 0

        # Include industry information in the analysis
        analysis['industry'] = stock.industry

        # Volume analysis
        volume_ratio = stock.volume / stock.avg_volume
        analysis['volume_status'] = StockAnalyzer._categorize_volume(volume_ratio)
        analysis['volume_ratio'] = f"{volume_ratio:.2f}"
        potential_score += StockAnalyzer._score_volume(volume_ratio)

        # PE Ratio analysis
        pe_status, pe_score = StockAnalyzer._analyze_pe_ratio(stock.pe_ratio, stock.industry_pe_ratio)
        analysis['pe_status'] = pe_status
        analysis['pe_ratio'] = f"{stock.pe_ratio:.2f}"
        analysis['industry_pe_ratio'] = f"{stock.industry_pe_ratio:.2f}"
        potential_score += pe_score

        # Growth potential
        growth_potential = (stock.target_est_1y - stock.current_price) / stock.current_price * 100
        analysis['growth_potential'] = f"{growth_potential:.2f}%"
        analysis['current_price'] = f"${stock.current_price:.2f}"
        analysis['target_price'] = f"${stock.target_est_1y:.2f}"
        potential_score += StockAnalyzer._score_growth_potential(growth_potential)

        # Dividend analysis
        analysis['dividend_status'], dividend_score = StockAnalyzer._analyze_dividend(stock.dividend_yield)
        if stock.dividend_yield > 0:
            analysis['dividend_yield'] = f"{stock.dividend_yield:.2f}%"
        potential_score += dividend_score

        # Financial health indicators
        analysis.update(StockAnalyzer._analyze_financial_health(stock))
        potential_score += analysis.pop('financial_health_score', 0)

        # Beta analysis
        analysis['beta'] = f"{stock.beta:.2f}"
        analysis['volatility'] = StockAnalyzer._categorize_volatility(stock.beta)

        # Overall recommendation
        analysis['recommendation'] = StockAnalyzer._get_recommendation(potential_score)
        analysis['potential_score'] = potential_score

        return analysis
    @staticmethod
    def _categorize_volume(ratio: float) -> str:
        """
        Categorize the volume ratio.

        Args:
            ratio (float): The volume ratio.

        Returns:
            str: The volume status.
        """
        if ratio > 1.5:
            return 'High'
        elif ratio < 0.5:
            return 'Low'
        return 'Normal'

    @staticmethod
    def _score_volume(ratio: float) -> int:
        """
        Score the volume ratio.

        Args:
            ratio (float): The volume ratio.

        Returns:
            int: The volume score.
        """
        if ratio > 2:
            return 1
        elif ratio < 0.3:
            return -1
        return 0

    @staticmethod
    def _analyze_pe_ratio(pe_ratio: float, industry_pe_ratio: float) -> tuple[str, int]:
        """
        Analyze the PE ratio.

        Args:
            pe_ratio (float): The PE ratio of the stock.
            industry_pe_ratio (float): The industry PE ratio.

        Returns:
            tuple[str, int]: The PE status and score.
        """
        if pe_ratio <= 0:
            return 'Negative (Caution)', -2
        elif pe_ratio < industry_pe_ratio * 0.7:
            return 'Significantly Undervalued', 3
        elif pe_ratio < industry_pe_ratio * 0.9:
            return 'Slightly Undervalued', 1
        elif pe_ratio > industry_pe_ratio * 1.3:
            return 'Significantly Overvalued', -2
        elif pe_ratio > industry_pe_ratio * 1.1:
            return 'Slightly Overvalued', -1
        return 'Fair valued', 0

    @staticmethod
    def _score_growth_potential(growth_potential: float) -> int:
        """
        Score the growth potential.

        Args:
            growth_potential (float): The growth potential.

        Returns:
            int: The growth potential score.
        """
        if growth_potential > 30:
            return 4
        elif growth_potential > 20:
            return 3
        elif growth_potential > 10:
            return 2
        elif growth_potential > 0:
            return 1
        elif growth_potential < -20:
            return -3
        elif growth_potential < -10:
            return -2
        elif growth_potential < 0:
            return -1
        return 0

    @staticmethod
    def _analyze_dividend(dividend_yield: float) -> tuple[str, int]:
        """
        Analyze the dividend yield.

        Args:
            dividend_yield (float): The dividend yield.

        Returns:
            tuple[str, int]: The dividend status and score.
        """
        if dividend_yield > 5:
            return 'Very High', 2
        elif dividend_yield > 3:
            return 'High', 1
        elif dividend_yield > 1:
            return 'Moderate', 0
        elif dividend_yield > 0:
            return 'Low', 0
        return 'No dividend', 0

    @staticmethod
    def _analyze_financial_health(stock: StockFormat) -> Dict[str, Any]:
        """
        Analyze the financial health of the stock.

        Args:
            stock (StockFormat): The formatted stock data.

        Returns:
            Dict[str, Any]: A dictionary containing the financial health analysis.
        """
        analysis = {}
        score = 0

        if stock.debt_to_equity > 0:
            analysis['debt_to_equity'] = f"{stock.debt_to_equity:.2f}"
            if stock.debt_to_equity > 2:
                analysis['debt_status'] = 'High (Caution)'
                score -= 2
            elif stock.debt_to_equity > 1:
                analysis['debt_status'] = 'Moderate'
                score -= 1
            else:
                analysis['debt_status'] = 'Low'
                score += 1

        if stock.current_ratio > 0:
            analysis['current_ratio'] = f"{stock.current_ratio:.2f}"
            if stock.current_ratio > 3:
                analysis['liquidity_status'] = 'Very Strong'
                score += 2
            elif stock.current_ratio > 2:
                analysis['liquidity_status'] = 'Strong'
                score += 1
            elif stock.current_ratio > 1:
                analysis['liquidity_status'] = 'Adequate'
            else:
                analysis['liquidity_status'] = 'Weak (Caution)'
                score -= 1

        if stock.price_to_book > 0:
            analysis['price_to_book'] = f"{stock.price_to_book:.2f}"
            if stock.price_to_book < 1:
                analysis['price_to_book_status'] = 'Potentially Undervalued'
                score += 2
            elif stock.price_to_book < 3:
                analysis['price_to_book_status'] = 'Fair'
                score += 1
            else:
                analysis['price_to_book_status'] = 'Potentially Overvalued'
                score -= 1

        if stock.return_on_equity > 0:
            analysis['return_on_equity'] = f"{stock.return_on_equity:.2f}%"
            if stock.return_on_equity > 20:
                analysis['roe_status'] = 'Excellent'
                score += 2
            elif stock.return_on_equity > 15:
                analysis['roe_status'] = 'Good'
                score += 1
            elif stock.return_on_equity > 10:
                analysis['roe_status'] = 'Fair'
            else:
                analysis['roe_status'] = 'Poor'
                score -= 1

        analysis['free_cash_flow'] = f"${stock.free_cash_flow:.2f}B"
        if stock.free_cash_flow > 0:
            analysis['fcf_status'] = 'Positive'
            score += 1
        else:
            analysis['fcf_status'] = 'Negative (Caution)'
            score -= 1

        analysis['financial_health_score'] = score
        return analysis

    @staticmethod
    def _categorize_volatility(beta: float) -> str:
        """
        Categorize the volatility based on the beta value.

        Args:
            beta (float): The beta value.

        Returns:
            str: The volatility status.
        """
        if beta < 0.8:
            return 'Low'
        elif beta < 1.2:
            return 'Moderate'
        return 'High'

    @staticmethod
    def _get_recommendation(score: int) -> str:
        """
        Get the recommendation based on the potential score.

        Args:
            score (int): The potential score.

        Returns:
            str: The recommendation.
        """
        if score >= 6:
            return 'Strong Buy'
        elif score >= 3:
            return 'Buy'
        elif score <= -4:
            return 'Strong Sell'
        elif score <= -2:
            return 'Sell'
        return 'Hold'
