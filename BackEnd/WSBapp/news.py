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

    finnhub_client = finnhub.Client(api_key=api_key)

    news = finnhub_client.general_news('general', min_id=0)
    news = str(news)
    time.sleep(5)

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
        if news['news'] is None:
            return None
        news_data = {
            'date': date,
            'news': news
        }
        collection.insert_one(news_data)
    else:
        news = news_in_database['news']

    return news

get_news()