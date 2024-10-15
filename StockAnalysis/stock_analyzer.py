from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class StockData:
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

class StockAnalyzer:
    @staticmethod
    def analyze_stock(stock: StockData) -> Dict[str, Any]:
        analysis = {}
        potential_score = 0

        # Volume analysis
        volume_ratio = stock.volume / stock.avg_volume
        analysis['volume_status'] = 'High' if volume_ratio > 1.5 else 'Low' if volume_ratio < 0.5 else 'Normal'
        analysis['volume_ratio'] = f"{volume_ratio:.2f}"

        if volume_ratio > 2:
            potential_score += 1
        elif volume_ratio < 0.3:
            potential_score -= 1

        # PE Ratio analysis
        if stock.pe_ratio <= 0:
            analysis['pe_status'] = 'Negative (Caution)'
            potential_score -= 2
        elif stock.pe_ratio < stock.industry_pe_ratio * 0.7:
            analysis['pe_status'] = 'Significantly Undervalued'
            potential_score += 3
        elif stock.pe_ratio < stock.industry_pe_ratio * 0.9:
            analysis['pe_status'] = 'Slightly Undervalued'
            potential_score += 1
        elif stock.pe_ratio > stock.industry_pe_ratio * 1.3:
            analysis['pe_status'] = 'Significantly Overvalued'
            potential_score -= 2
        elif stock.pe_ratio > stock.industry_pe_ratio * 1.1:
            analysis['pe_status'] = 'Slightly Overvalued'
            potential_score -= 1
        else:
            analysis['pe_status'] = 'Fair valued'

        analysis['pe_ratio'] = f"{stock.pe_ratio:.2f}"
        analysis['industry_pe_ratio'] = f"{stock.industry_pe_ratio:.2f}"

        # Growth potential
        current_price = stock.pe_ratio * stock.eps
        growth_potential = (stock.target_est_1y - current_price) / current_price * 100
        analysis['growth_potential'] = f"{growth_potential:.2f}%"
        analysis['current_price'] = f"${current_price:.2f}"
        analysis['target_price'] = f"${stock.target_est_1y:.2f}"

        # Adjust potential score based on growth potential
        if growth_potential > 30:
            potential_score += 4
        elif growth_potential > 20:
            potential_score += 3
        elif growth_potential > 10:
            potential_score += 2
        elif growth_potential > 0:
            potential_score += 1
        elif growth_potential < -20:
            potential_score -= 3
        elif growth_potential < -10:
            potential_score -= 2
        elif growth_potential < 0:
            potential_score -= 1

        # Dividend analysis
        if stock.dividend_yield > 0:
            analysis['dividend_yield'] = f"{stock.dividend_yield:.2f}%"
            if stock.dividend_yield > 5:
                analysis['dividend_status'] = 'Very High'
                potential_score += 2
            elif stock.dividend_yield > 3:
                analysis['dividend_status'] = 'High'
                potential_score += 1
            elif stock.dividend_yield > 1:
                analysis['dividend_status'] = 'Moderate'
            else:
                analysis['dividend_status'] = 'Low'
        else:
            analysis['dividend_status'] = 'No dividend'

        # Financial health indicators
        if stock.debt_to_equity > 0:
            analysis['debt_to_equity'] = f"{stock.debt_to_equity:.2f}"
            if stock.debt_to_equity > 2:
                analysis['debt_status'] = 'High (Caution)'
                potential_score -= 2
            elif stock.debt_to_equity > 1:
                analysis['debt_status'] = 'Moderate'
                potential_score -= 1
            else:
                analysis['debt_status'] = 'Low'
                potential_score += 1

        if stock.current_ratio > 0:
            analysis['current_ratio'] = f"{stock.current_ratio:.2f}"
            if stock.current_ratio > 3:
                analysis['liquidity_status'] = 'Very Strong'
                potential_score += 2
            elif stock.current_ratio > 2:
                analysis['liquidity_status'] = 'Strong'
                potential_score += 1
            elif stock.current_ratio > 1:
                analysis['liquidity_status'] = 'Adequate'
            else:
                analysis['liquidity_status'] = 'Weak (Caution)'
                potential_score -= 1

        # Price to Book analysis
        if stock.price_to_book > 0:
            analysis['price_to_book'] = f"{stock.price_to_book:.2f}"
            if stock.price_to_book < 1:
                analysis['price_to_book_status'] = 'Potentially Undervalued'
                potential_score += 2
            elif stock.price_to_book < 3:
                analysis['price_to_book_status'] = 'Fair'
                potential_score += 1
            else:
                analysis['price_to_book_status'] = 'Potentially Overvalued'
                potential_score -= 1

        # Return on Equity analysis
        if stock.return_on_equity > 0:
            analysis['return_on_equity'] = f"{stock.return_on_equity:.2f}%"
            if stock.return_on_equity > 20:
                analysis['roe_status'] = 'Excellent'
                potential_score += 2
            elif stock.return_on_equity > 15:
                analysis['roe_status'] = 'Good'
                potential_score += 1
            elif stock.return_on_equity > 10:
                analysis['roe_status'] = 'Fair'
            else:
                analysis['roe_status'] = 'Poor'
                potential_score -= 1

        # Free Cash Flow analysis
        if stock.free_cash_flow > 0:
            analysis['free_cash_flow'] = f"${stock.free_cash_flow:.2f}B"
            analysis['fcf_status'] = 'Positive'
            potential_score += 1
        else:
            analysis['free_cash_flow'] = f"${stock.free_cash_flow:.2f}B"
            analysis['fcf_status'] = 'Negative (Caution)'
            potential_score -= 1

        # Beta analysis
        analysis['beta'] = f"{stock.beta:.2f}"
        if stock.beta < 0.8:
            analysis['volatility'] = 'Low'
        elif stock.beta < 1.2:
            analysis['volatility'] = 'Moderate'
        else:
            analysis['volatility'] = 'High'

        # Overall recommendation
        if potential_score >= 6:
            analysis['recommendation'] = 'Strong Buy'
        elif potential_score >= 3:
            analysis['recommendation'] = 'Buy'
        elif potential_score <= -4:
            analysis['recommendation'] = 'Strong Sell'
        elif potential_score <= -2:
            analysis['recommendation'] = 'Sell'
        else:
            analysis['recommendation'] = 'Hold'

        analysis['potential_score'] = potential_score
        return analysis
