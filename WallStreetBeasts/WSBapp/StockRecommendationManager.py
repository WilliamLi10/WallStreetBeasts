from typing import List, Dict
from stock_analyzer import StockAnalyzer,StockFormat

class StockRecommendationManager:
    def __init__(self, stocks: List[StockFormat]):
        self.stocks = stocks

    def get_recommendations(self) -> Dict[str, List[str]]:
        recommendations = {
            "Strong Buy": [],
            "Buy": [],
            "Hold": [],
            "Sell": [],
            "Strong Sell": [],
        }

        for stock in self.stocks:
            analysis = StockAnalyzer.analyze_stock(stock)
            recommendation = analysis['recommendation']
            recommendations[recommendation].append(stock.ticker)

        return recommendations

    def get_hold_stocks(self) -> List[str]:
        return self.get_recommendations().get("Hold", [])

    def get_buy_stocks(self) -> List[str]:
        return self.get_recommendations().get("Buy", [])

    def get_sell_stocks(self) -> List[str]:
        return self.get_recommendations().get("Sell", [])

    def get_strong_buy_stocks(self) -> List[str]:
        return self.get_recommendations().get("Strong Buy", [])

    def get_strong_sell_stocks(self) -> List[str]:
        return self.get_recommendations().get("Strong Sell", [])
