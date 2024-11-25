import unittest
from unittest.mock import patch
from BackEnd.WSBapp.stock_analyzer import StockAnalyzer
from BackEnd.WSBapp.StockData import StockData
from BackEnd.WSBapp.stock_analyzer import StockFormat
class TestStockFormat(unittest.TestCase):
    def test_current_price_calculation(self):
        stock = StockFormat(
            ticker="AAPL",
            volume=1000000,
            avg_volume=800000,
            pe_ratio=20.0,
            industry_pe_ratio=15.0,
            target_est_1y=200.0,
            eps=10.0
        )
        self.assertEqual(stock.current_price, 200.0)

class TestStockData(unittest.TestCase):
    @patch("yfinance.Ticker")  # Mock yfinance.Ticker
    def test_initialization(self, mock_ticker):
        mock_info = {
            "volume": 1000000,
            "averageVolume": 800000,
            "trailingPE": 20.0,
            "trailingEps": 10.0,
            "targetMeanPrice": 200.0,
            "industry": "Technology",
        }
        mock_ticker.return_value.info = mock_info

        stock_data = StockData("AAPL")
        self.assertEqual(stock_data.volume, 1000000)
        self.assertEqual(stock_data.avg_volume, 800000)
        self.assertEqual(stock_data.pe_ratio, 20.0)
        self.assertEqual(stock_data.eps, 10.0)
        self.assertEqual(stock_data.target_est_1y, 200.0)
        self.assertEqual(stock_data.industry, "Technology")

    def test_get_industry_pe_ratio(self):
        industry = "Healthcare"
        pe_ratio = StockData._get_industry_pe_ratio(industry)
        self.assertEqual(pe_ratio, 18.3)

        unknown_industry = "Unknown Industry"
        pe_ratio = StockData._get_industry_pe_ratio(unknown_industry)
        self.assertEqual(pe_ratio, 15.0)  # Default value

class TestStockAnalyzer(unittest.TestCase):
    @patch("stock_module.StockData")
    def test_analyze_stock_format(self, MockStockData):
        stock = StockFormat(
            ticker="AAPL",
            volume=1000000,
            avg_volume=800000,
            pe_ratio=20.0,
            industry_pe_ratio=25.0,
            target_est_1y=200.0,
            eps=10.0,
            dividend_yield=1.5,
            debt_to_equity=0.8,
            current_ratio=2.0,
            price_to_book=1.5,
            return_on_equity=15.0,
            free_cash_flow=1.0,
            beta=1.1,
            industry="Technology"
        )
        analysis = StockAnalyzer.analyze_stock_format(stock)
        self.assertIn("growth_potential", analysis)
        self.assertIn("recommendation", analysis)

    @patch("stock_module.StockData")
    def test_analyze_stock(self, MockStockData):
        MockStockData.return_value.volume = 1000000
        MockStockData.return_value.avg_volume = 800000
        MockStockData.return_value.pe_ratio = 20.0
        MockStockData.return_value.eps = 10.0
        MockStockData.return_value.target_est_1y = 200.0
        MockStockData.return_value.industry = "Technology"

        analysis = StockAnalyzer.analyze_stock("AAPL")
        self.assertIn("potential_score", analysis)
        self.assertIn("recommendation", analysis)

if __name__ == "__main__":
    unittest.main()
