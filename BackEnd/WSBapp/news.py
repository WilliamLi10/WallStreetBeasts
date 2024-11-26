import os
from dotenv import load_dotenv
import json
import sys
from datetime import datetime
from pymongo import MongoClient
import finnhub
import time

def get_current_news():

    a = load_dotenv("api.env")

    api_key = os.getenv("API_KEY")

    if api_key is None:
        sys.exit(1)

    try:
        finnhub_client = finnhub.Client(api_key=api_key)

        print(finnhub_client)

        news = finnhub_client.general_news('general', min_id=0)
        time.sleep(5)
    except Exception as e:
        print("hello", e)
        return None


    return news
    
def get_news():
    client = MongoClient('localhost', 27017)
    database = client['wsbdb']
    collection = database['news']
    date = datetime.now().strftime("%Y%m%d")
    news_in_database = collection.find_one({'date':date})
    news = None
    if news_in_database is None:
        news = get_current_news()
        if news is None:
            return None
        news_data = {
            'date': date,
            'news': news
        }
        collection.insert_one(news_data)
    else:
        news = news_in_database['news']

    return news
def getstocknews(ticker):
    pass