from typing import Dict, Any
from dataclasses import dataclass, field

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

    @property
    def current_price(self) -> float:
        return self.pe_ratio * self.eps

class StockAnalyzer:
    @staticmethod
    def analyze_stock(stock: StockFormat) -> Dict[str, Any]:
        analysis = {}
        potential_score = 0

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
        if ratio > 1.5:
            return 'High'
        elif ratio < 0.5:
            return 'Low'
        return 'Normal'

    @staticmethod
    def _score_volume(ratio: float) -> int:
        if ratio > 2:
            return 1
        elif ratio < 0.3:
            return -1
        return 0

    @staticmethod
    def _analyze_pe_ratio(pe_ratio: float, industry_pe_ratio: float) -> tuple[str, int]:
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
        if beta < 0.8:
            return 'Low'
        elif beta < 1.2:
            return 'Moderate'
        return 'High'

    @staticmethod
    def _get_recommendation(score: int) -> str:
        if score >= 6:
            return 'Strong Buy'
        elif score >= 3:
            return 'Buy'
        elif score <= -4:
            return 'Strong Sell'
        elif score <= -2:
            return 'Sell'
        return 'Hold'