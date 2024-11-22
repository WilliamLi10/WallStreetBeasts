import os
from dotenv import load_dotenv
import json
import sys
from datetime import datetime

def get_current_news():

    a = load_dotenv("api.env")

    print(a)

    api_key = os.getenv("API_KEY")

    print(api_key)

    if api_key is None:
        sys.exit(1)

    import http.client, urllib.parse

    conn = http.client.HTTPSConnection('api.marketaux.com')

    params = urllib.parse.urlencode({
        'api_token': api_key,
        'limit': 3,
    })

    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    decoded_data = data.decode('utf-8')

    news = json.loads(decoded_data)

    final = dict()

    final['datetime'] = datetime.now()

    final['news'] = news

    return final

get_current_news()
