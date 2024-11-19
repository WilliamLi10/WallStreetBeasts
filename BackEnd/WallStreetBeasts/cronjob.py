import schedule
import time
from BackEnd.WSBapp.StockData import StockData
from BackEnd.WSBapp.stock_analyzer import StockAnalyzer

def fetch_trending_stocks():
    # Example tickers for trending stocks
    trending_tickers = ['AAPL', 'TSLA', 'AMZN']  # Replace with actual logic to get trending stocks


# Schedule the job to run at noon every day
schedule.every().day.at("12:00").do(fetch_trending_stocks)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)