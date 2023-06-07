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
from plotly.subplots import make_subplots
from django.views.decorators.http import require_http_methods


def get_news(ticker_noticias):
    url = f'https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker_noticias}'
    url = url.replace('/rss/2.0/headline?s=    ','/rss/2.0/headline?s=')
    feed = feedparser.parse(url)
    noticias = feed.entries[:25]
    noticias = [entry.description for entry in noticias]  # Extract titles from the news entries

    return noticias # Return the noticias variable
 
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



import plotly.graph_objs as go
from prophet import Prophet
from prophet.plot import plot

def my_view(request):
    # establecer el tiempo de espera en segundos
    request._streaming = True
    request._read_started = True
    response = HttpResponse()
    response['Keep-Alive'] = 'timeout=300, max=300'
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        if symbol =="":
            symbol= 'BTC/USDT'
            timeframe='1h'
            Type='Line'
        else:
            timeframe = request.POST.get('timeframe')
            Type= request.POST.get('Type')
        if Type =="Line":
            binance = ccxt.binance()
            data = binance.fetchOHLCV(symbol, timeframe)
            data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close','volume'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            x_values = data['timestamp']
            y_values = data['close']
            trace = go.Scatter(x=x_values,y=y_values,mode='lines',line=dict(color='#00c3ff'))
            data = [trace]
            layout = go.Layout(title=f'{symbol}  {timeframe}',font={'color': 'white'},paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=1000,autosize=True,dragmode='pan')
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
            layout = go.Layout(title=f'{symbol}  {timeframe}', font={'color': 'white'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=1000, autosize=True,dragmode='pan',xaxis=dict(rangeslider=dict(visible=False)))
            fig = go.Figure(data=data, layout=layout)
            config = {'displayModeBar': False, 'scrollZoom': True,'modeBarButtons': [['drawline', 'drawopenpath','drawcircle', 'drawrect', 'eraseshape']]}
            plot_div = fig.to_html(full_html=False, config=config)
            return render(request, 'templates/prueba.html', {'plot_div': plot_div})
        
        if Type=="Prophet":
            binance = ccxt.binance()
            data = binance.fetchOHLCV(symbol, timeframe)
            data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close','volume'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            x_values = data['timestamp']
            y_values = data['close']
            forecast_df = data
            forecast_df.rename(columns={'timestamp':'ds','close':'y'},inplace=True)
            forecast_df.head()
            m = Prophet()
            m = Prophet(daily_seasonality = True)
            m = Prophet(weekly_seasonality=True)
            m = Prophet(yearly_seasonality=True)
            m.fit(forecast_df)
            future = m.make_future_dataframe(periods=30)
            forecast = m.predict(future)
            # Crear una figura HTML con Plotly
            layout = go.Layout(title=f'Time-series Forecasting {symbol}  {timeframe}', font={'color': 'white'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=1000, autosize=True,dragmode='pan',xaxis=dict(rangeslider=dict(visible=False)))
            fig = go.Figure(layout=layout)
            fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['y'],mode='lines',line=dict(color='#00c3ff', width=3),name='Valores'))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicciones',line=dict(color='#f7d200', width=1)))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Intervalo superior',line=dict(color='#1eff00', width=1)))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Intervalo inferior',line=dict(color='#ff0808', width=1)))
            # Convertir la figura en HTML
            config = {'displayModeBar': False, 'scrollZoom': True,'modeBarButtons': [['drawline', 'drawopenpath','drawcircle', 'drawrect', 'eraseshape']]}
            html_fig = fig.to_html(full_html=False,config=config)
            return render(request, 'templates/prueba.html', {'plot_div': html_fig})
        
        if Type == "heatmap-bids":
            df = pd.read_csv('csv/BTC_DATA_HEAT_MAP.csv')
            # Convierte la columna "date" a objetos datetime
            df['date'] = pd.to_datetime(df['date'])
            # Redondea los valores de fecha y hora a la unidad de minuto más cercana para eliminar los segundos
            df['date'] = df['date'].dt.floor('4H')
            df['bid'] = df['bid'].apply(lambda x: int(round(float(x)/10)*10))
            df['ask'] = df['ask'].apply(lambda x: int(round(float(x)/10)*10))

            df_bid = df.groupby(['date', 'bid'])['bid_volume'].sum().reset_index()
            df_ask = df.groupby(['date', 'ask'])['ask_volume'].sum().reset_index()
            df = df_bid.merge(df_ask, on='date')

            df.to_csv('csv/BTC_DATA_HEAT_MAP2.csv',index=False, columns=['date','bid','bid_volume','ask', 'ask_volume'])
            binance = ccxt.binance()
            bars = binance.fetchOHLCV(symbol, timeframe)
            df3= pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
            actual_price= int(df3['close'].iloc[-1])
            df3['timestamp'] = pd.to_datetime(df3['timestamp'], unit='ms')
            useful_columns = ['timestamp','close']
            df3 = df3.loc[:,useful_columns]
            df2_2 =pd.read_csv('csv/BTC_DATA_HEAT_MAP2.csv')
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Heatmap(z=df2_2['bid_volume'], x=df2_2['date'], y=df2_2['bid'], colorscale='YlOrRd'))

            y_heatmap = df2_2['bid'].tolist()
            y_scatter = df3['close'].tolist()
            y_range = [min(min(y_heatmap), min(y_scatter)), max(max(y_heatmap), max(y_scatter))]

            fig.add_trace(go.Scatter(mode='lines', x=df3['timestamp'], y=y_scatter, line=dict(color='#4DC3FF', width=5), yaxis='y2'))

            fig.update_layout(yaxis=dict(range=y_range), yaxis2=dict(range=y_range, side='right'))
            fig.update_layout(plot_bgcolor='black')

            fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_xaxes(visible=True)
            fig.update_layout(title=f'heatmap-bids {symbol}  {timeframe} ${actual_price}', font={'color': 'white'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=1000, autosize=True, dragmode='pan', xaxis=dict(rangeslider=dict(visible=False)))
            #fig.write_image(file="lastheat.jpg", width=6000)
            config = {'displayModeBar': False, 'scrollZoom': True, 'modeBarButtons': [['drawline', 'drawopenpath','drawcircle', 'drawrect', 'eraseshape']]}
            plot_div = fig.to_html(full_html=False, config=config)
            #segundo grafico
            df2 =df2_2
            df2['date'] = pd.to_datetime(df2['date'])
            df2.set_index('date', inplace=True)
            df2_min = df2.resample('4H').sum()
            df_bid = pd.DataFrame(df2_min['bid_volume'])
            df_ask = pd.DataFrame(df2_min['ask_volume'])
            layout = go.Layout(title=f'Buyers and Sellers spread', font={'color': 'white'}, paper_bgcolor='#000000', plot_bgcolor='#000000', height=1000, autosize=True,dragmode='pan',xaxis=dict(rangeslider=dict(visible=False)))
            fig = go.Figure(layout=layout)
            fig.add_trace(go.Scatter(x=df2_min.index, y=df_ask['ask_volume'], mode='lines', name='Sellers ask Orders',line=dict(color='#ff1e00', width=3)))#BEAR
            fig.add_trace(go.Scatter(x=df2_min.index, y=df_bid['bid_volume'], mode='lines', name='Buyers bid Orders',line=dict(color='#07c700', width=3)))#BULL
            html_fig = fig.to_html(full_html=False,config=config)
            return render(request, 'templates/prueba.html', {'plot_div': plot_div,'html_fig':html_fig})
            
        if Type == "heatmap-asks":
            df = pd.read_csv('csv/BTC_DATA_HEAT_MAP.csv')
            # Convierte la columna "date" a objetos datetime
            df['date'] = pd.to_datetime(df['date'])
            # Redondea los valores de fecha y hora a la unidad de minuto más cercana para eliminar los segundos
            df['date'] = df['date'].dt.floor('4H')
            df['bid'] = df['bid'].apply(lambda x: int(round(float(x)/10)*10))
            df['ask'] = df['ask'].apply(lambda x: int(round(float(x)/10)*10))

            df_bid = df.groupby(['date', 'bid'])['bid_volume'].sum().reset_index()
            df_ask = df.groupby(['date', 'ask'])['ask_volume'].sum().reset_index()
            df = df_bid.merge(df_ask, on='date')

            df.to_csv('csv/BTC_DATA_HEAT_MAP2.csv',index=False, columns=['date','bid','bid_volume','ask', 'ask_volume'])
            binance = ccxt.binance()
            bars = binance.fetchOHLCV(symbol, timeframe)
            df3= pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
            actual_price= int(df3['close'].iloc[-1])
            df3['timestamp'] = pd.to_datetime(df3['timestamp'], unit='ms')
            useful_columns = ['timestamp','open','high','low','close','volume']
            df3 = df3.loc[:,useful_columns]
            df2_2 =pd.read_csv('csv/BTC_DATA_HEAT_MAP2.csv')
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Heatmap(z=df2_2['ask_volume'], x=df2_2['date'], y=df2_2['ask'], colorscale='YlOrRd'))

            y_heatmap = df2_2['bid'].tolist()
            y_scatter = df3['close'].tolist()
            y_range = [min(min(y_heatmap), min(y_scatter)), max(max(y_heatmap), max(y_scatter))]

            fig.add_trace(go.Scatter(mode='lines', x=df3['timestamp'], y=y_scatter, line=dict(color='#4DC3FF', width=5), yaxis='y2'))
            #fig.add_trace(go.Candlestick(x=df3['timestamp'],open=df3['open'],high=df3['high'],low=df3['low'],close=df3['close'], yaxis='y2'))

            # Update the layout
            fig.update_layout(title='Historical stock prices',
                            xaxis_rangeslider_visible=False)
            fig.update_layout(yaxis=dict(range=y_range), yaxis2=dict(range=y_range, side='right'))
            fig.update_layout(plot_bgcolor='black')

            fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_xaxes(visible=True)
            fig.update_layout(title=f'heatmap-asks {symbol}  {timeframe} ${actual_price}', font={'color': 'white'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=1000, autosize=True, dragmode='pan', xaxis=dict(rangeslider=dict(visible=False)))
            #fig.write_image(file="lastheat.jpg", width=6000)
            config = {'displayModeBar': False, 'scrollZoom': True, 'modeBarButtons': [['drawline', 'drawopenpath','drawcircle', 'drawrect', 'eraseshape']]}
            plot_div = fig.to_html(full_html=False, config=config)
            #segundo grafico
            df2 =df2_2
            df2['date'] = pd.to_datetime(df2['date'])
            df2.set_index('date', inplace=True)
            df2_min = df2.resample('4H').sum() #1H
            df_bid = pd.DataFrame(df2_min['bid_volume'])
            df_ask = pd.DataFrame(df2_min['ask_volume'])
            layout = go.Layout(title=f'Buyers and Sellers spread', font={'color': 'white'}, paper_bgcolor='#000000', plot_bgcolor='#000000', height=1000, autosize=True,dragmode='pan',xaxis=dict(rangeslider=dict(visible=False)))
            fig = go.Figure(layout=layout)
            fig.add_trace(go.Scatter(x=df2_min.index, y=df_ask['ask_volume'], mode='lines', name='Sellers ask Orders',line=dict(color='#ff1e00', width=3)))#BEAR
            fig.add_trace(go.Scatter(x=df2_min.index, y=df_bid['bid_volume'], mode='lines', name='Buyers bid Orders',line=dict(color='#07c700', width=3)))#BULL
            html_fig = fig.to_html(full_html=False,config=config)
            return render(request, 'templates/prueba.html', {'plot_div': plot_div,'html_fig':html_fig})
    else:
        return render(request, 'templates/prueba.html')