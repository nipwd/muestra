from flask import Flask, render_template
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib import style, rcParams
import feedparser

import pandas as pd
import requests
import json
import base64
from io import BytesIO

app = Flask(__name__)
current_price = None

API_KEY = '' # API de Alpha Vantage
symbol = 'AAPL'
def get_price_data(symbol):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=1min&apikey=' + API_KEY
    url = url.replace('= ', '=')

    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame.from_dict(data['Time Series (1min)'], orient='index')
    df.index = pd.to_datetime(df.index)
    df['4. close'] = pd.to_numeric(df['4. close'])
    return df['4. close']

def render_image():
    global current_price
    prices = get_price_data(symbol)
    current_price = prices[-1]
    fig = plt.figure(figsize=(10, 6))
    style.use('dark_background')
    rcParams['text.color'] = 'white' 
    rcParams['axes.facecolor'] = 'black'
    fig = plt.figure(figsize=(10, 6))
    plt.plot(prices)
    plt.title('Precio en tiempo real de ' + symbol , color='white')
    plt.xlabel('Hora', color='white') 
    plt.ylabel('Precio', color='white') 
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def get_news():
    url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=BTC'
    feed = feedparser.parse(url)
    return feed.entries[:25]

@app.route('/')
@app.route('/')
def index():
    image_data = render_image()
    news = get_news()
    return render_template('index.html', image_data=image_data, current_price=current_price, news=news)

if __name__ == '__main__':
    app.run(debug=True)
