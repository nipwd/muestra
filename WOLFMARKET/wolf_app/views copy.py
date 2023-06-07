from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wolf_app.live import app
from django.http import HttpResponse
import pandas as pd
import feedparser
import ccxt
import json
import datetime


def mostrar_app(request):
    html = """
        <iframe src="http://localhost:8080/" width="100%" height="800px"></iframe>
    """
    return HttpResponse(html)

@csrf_exempt
def dash_graphic(request):
    """
    This view renders a template that includes a Dash app.
    """
    data= pd.read_csv('csv/test.csv')
    print(data)
    ticker_activo =str(data['ticker_symbol']).split("Name")
    ticker_activo= str(ticker_activo[0]).split("0")
    valor_Activo =int(data['valor'])
    ticker_activo =ticker_activo[1]
    ticker_activo.replace(" ","")
    ticker_noticias = ticker_activo.split('/USDT')
    ticker_noticias=ticker_noticias[0]
    noticias = get_news(ticker_noticias) # Call get_news function and store the returned value in noticias variable
    return render(request, 'templates/test.html', {'my_dash_app': app, 'ticker_activo': ticker_activo, 'valor_Activo': valor_Activo, 'noticias':noticias})

def get_news(ticker_noticias):
    url = f'https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker_noticias}'
    url = url.replace('/rss/2.0/headline?s=    ','/rss/2.0/headline?s=')
    feed = feedparser.parse(url)
    noticias = feed.entries[:25]
    noticias = [entry.description for entry in noticias]  # Extract titles from the news entries

    return noticias # Return the noticias variable


import ccxt
from django.shortcuts import render
 
def get_binance_data(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        if symbol =="":
            symbol= 'BTC/USDT'
            timeframe='1h'
        else:
            timeframe = request.POST.get('timeframe')
        
        binance = ccxt.binance()
        data = binance.fetch_ohlcv(symbol, timeframe)
 
        return render(request, 'templates/test2.html', {'data': data})
 
    return render(request, 'templates/test2.html')




def heatmap(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        if symbol =="":
            symbol= 'BTC/USDT'
            timeframe='1h'
        else:
            timeframe = request.POST.get('timeframe')
        
        binance = ccxt.binance()
        data = binance.fetch_ohlcv(symbol, timeframe)
        OR_BOOK = binance.fetch_bids_asks(symbol)
        bid = OR_BOOK[symbol]['bid']
        bid_volume = OR_BOOK[symbol]['bidVolume']
        ask = OR_BOOK[symbol]['ask']
        ask_volume = OR_BOOK[symbol]['askVolume']
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        my_list = [date,bid, bid_volume, ask, ask_volume]
        heat=pd.DataFrame(columns=['date','bid','bid_volume','ask', 'ask_volume'])
        heat.loc[len(my_list)] = [date, bid,bid_volume,ask,ask_volume]
        print(heat)
        return render(request, 'templates/heatmap.html', {'data': data})
 
    return render(request, 'templates/heatmap.html')

from django.shortcuts import render
import plotly.graph_objs as go

def my_view(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        if symbol =="":
            symbol= 'BTC/USDT'
            timeframe='1h'
            Type='Line'
        else:
            timeframe = request.POST.get('timeframe')
            Type= request.POST.get('Type')
            print(Type)
        if Type =="Line":
            binance = ccxt.binance()
            data = binance.fetchOHLCV(symbol, timeframe)
            data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close','volume'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            x_values = data['timestamp']
            y_values = data['close']
            trace = go.Scatter(x=x_values,y=y_values,mode='lines',line=dict(color='#00c3ff'))
            data = [trace]
            layout = go.Layout(title=f'{symbol}  {timeframe}',font={'color': 'white'},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=800,autosize=True,dragmode='pan')
            fig = go.Figure(data=data, layout=layout)
            config = {'displayModeBar': False, 'scrollZoom': True, 'modeBarButtons': [['drawline', 'drawopenpath','drawrect', 'eraseshape']]}
            plot_div = fig.to_html(full_html=False, config=config)
            return render(request, 'templates/prueba.html', {'plot_div': plot_div})
        
        if Type=="Candlestick":
            binance = ccxt.binance()
            data = binance.fetchOHLCV(symbol, timeframe)
            data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close','volume'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            x_values = data['timestamp']
            y_values = data['close']
            # Agregue el identificador de div "plot" y configure los gráficos de velas predeterminados
            trace = go.Candlestick(x=x_values, open=data['open'], high=data['high'], low=data['low'], close=data['close'], increasing=dict(line=dict(color='#00c3ff')), decreasing=dict(line=dict(color='#EF553B')))
            data = [trace]
            layout = go.Layout(title=f'{symbol}  {timeframe}', font={'color': 'white'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=800, autosize=True,dragmode='pan',xaxis=dict(rangeslider=dict(visible=False)))

            fig = go.Figure(data=data, layout=layout)
            config = {'displayModeBar': False, 'scrollZoom': True,'modeBarButtons': [['drawline', 'drawopenpath','drawcircle', 'drawrect', 'eraseshape']]}
            plot_div = fig.to_html(full_html=False, config=config)
            
            return render(request, 'templates/prueba.html', {'plot_div': plot_div})