from django.test import TestCase
from typing import Dict, List, Optional
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from time import sleep
from stock_analyzer import StockAnalyzer,StockFormat
from StockData import StockData
from unittest.mock import patch, MagicMock
import csv
# Create your tests here.



class StockAnalyzerTestCase(TestCase):
    def setUp(self):
        self.stock_analyzer = StockAnalyzer('stock_info.csv')

    @patch('stock_analyzer.StockAnalyzer.analyze')
    def test_analyze(self, mock_analyze):
        mock_analyze.return_value = StockFormat(price=100, volume=1000)
        result = self.stock_analyzer.analyze('AAPL')
        self.assertEqual(result.price, 100)
        self.assertEqual(result.volume, 1000)

    @patch('stock_analyzer.StockAnalyzer._load_tickers')
    @patch('stock_analyzer.StockAnalyzer._process_ticker')
    def test_load_stock_data(self, mock_process_ticker, mock_load_tickers):
        mock_load_tickers.return_value = None
        mock_process_ticker.side_effect = lambda ticker: (ticker, StockData(ticker))
        self.stock_analyzer.tickers = ['AAPL', 'GOOGL']
        self.stock_analyzer.load_stock_data()
        self.assertIn('AAPL', self.stock_analyzer.stock_data)
        self.assertIn('GOOGL', self.stock_analyzer.stock_data)

    @patch('stock_analyzer.StockAnalyzer._load_tickers')
    @patch('stock_analyzer.StockAnalyzer._process_ticker')
    def test_get_most_traded_stocks(self, mock_process_ticker, mock_load_tickers):
        mock_load_tickers.return_value = None
        mock_process_ticker.side_effect = lambda ticker: (ticker, StockData(ticker))
        self.stock_analyzer.tickers = ['AAPL', 'GOOGL']
        self.stock_analyzer.load_stock_data()
        self.stock_analyzer.stock_data['AAPL'].volume = 2000
        self.stock_analyzer.stock_data['GOOGL'].volume = 1500
        most_traded_stocks = self.stock_analyzer.get_most_traded_stocks(1)
        self.assertEqual(most_traded_stocks, [('AAPL', 2000)])

class StockDataTestCase(TestCase):
    def setUp(self):
        self.stock_data = StockData()

    @patch('StockData.StockData.get_data')
    def test_get_data(self, mock_get_data):
        mock_get_data.return_value = {'AAPL': {'price': 150, 'volume': 2000}}
        result = self.stock_data.get_data('AAPL')
        self.assertEqual(result['price'], 150)
        self.assertEqual(result['volume'], 2000)