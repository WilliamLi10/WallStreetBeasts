from typing import List
from django.contrib.auth.models import User
import news  # Assumed to be a module providing stock news

class Newsletter:
    def __init__(self, user: User):
        """
        Initializes the Newsletter class for a specific user.
        :param user: A Django user instance.
        """
        self.user = user
        self.ticker_list = self.get_user_ticker_list()
        self.newsletter = self.create_newsletter()

    def get_user_ticker_list(self) -> List[str]:
        """
        Retrieves the list of ticker symbols associated with the user.
        Assumes the user model has a `tickers` field or a related model for tickers.
        :return: A list of ticker symbols.
        """
        # Adjust based on your model implementation
        return list(self.user.profile.tickers.all().values_list('symbol', flat=True))

    def create_newsletter(self) -> str:
        """
        Creates a formatted newsletter with the top news for each stock in the user's list.
        :return: A formatted newsletter as a string.
        """
        if not self.ticker_list:
            return f"No stocks saved for {self.user.username} to generate a newsletter."

        # Dictionary to hold top news for each stock
        stock_news = {}

        for ticker in self.ticker_list:
            try:
                # Get top news for the stock
                top_news = self.get_stock_news(ticker)
                if top_news:
                    stock_news[ticker] = top_news[0]  # Assuming `get_stock_news` returns a list of news articles
                else:
                    stock_news[ticker] = "No recent news available."
            except Exception as e:
                stock_news[ticker] = f"Error fetching news: {str(e)}"

        # Format the newsletter
        newsletter = f"Portfolio News Digest for {self.user.username}\n\n"
        for ticker, news_item in stock_news.items():
            newsletter += f"Ticker: {ticker}\nTop News: {news_item}\n\n"

        return newsletter.strip()

    def get_stock_news(self, ticker: str) -> List[str]:
        """
        Fetches the top news for a given stock ticker.
        :param ticker: Stock ticker symbol.
        :return: A list of news headlines for the stock.
        """
        return news.get_stock_news(ticker)  # Assuming `get_stock_news` is a method in the `news` module

# Example usage:
# Assuming `user` is an instance of the Django User model
# newsletter = Newsletter(user)
# print(newsletter.newsletter)





