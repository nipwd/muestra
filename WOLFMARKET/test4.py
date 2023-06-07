"""views back up heatmap"""
"""
FUNCIONA

import ccxt
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

now = datetime.now()
symbol= 'BTC/USDT'
timeframe='5m'
Type ="heatmap"
binance = ccxt.binance()
bars = binance.fetchOHLCV(symbol, timeframe)
df3= pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
df3['timestamp'] = pd.to_datetime(df3['timestamp'], unit='ms')
useful_columns = ['timestamp','close']
df3 = df3.loc[:,useful_columns]

df2_2 =pd.read_csv('/home/main/WOLFMARKET/csv/BTC_DATA_HEAT_MAP.csv')
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Heatmap(
                z = df2_2['bid_volume'],
                x = df2_2['date'],
                y = df2_2['bid'],
                colorscale='Hot'))
        

y = df3['close']
fig.add_trace(go.Scatter(
mode='lines', 
x= df3['timestamp'], 
y=y, line=dict(color='steelblue',width=2)), secondary_y=True,)
       
       
fig.update_layout(
title='BTC bids HEATMAP 1H  ',
        xaxis_nticks=36)
fig['layout'].update(plot_bgcolor='black')
fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
fig.update_xaxes(visible=False)

fig.write_image("testheat.png",scale=25)
"""


import plotly.io as pio

import ccxt
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

now = datetime.now()
symbol= 'BTC/USDT'
timeframe='5m'
Type ="heatmap"
binance = ccxt.binance()
bars = binance.fetchOHLCV(symbol, timeframe)
df3= pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
df3['timestamp'] = pd.to_datetime(df3['timestamp'], unit='ms')
useful_columns = ['timestamp','close']
df3 = df3.loc[:,useful_columns]

df2_2 =pd.read_csv('/home/main/WOLFMARKET/csv/BTC_DATA_HEAT_MAP.csv')

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Heatmap(
    z = df2_2['bid_volume'],
    x = df2_2['date'],
    y = df2_2['bid'],
    colorscale='Hot'))
        
y = df3['close']
fig.add_trace(go.Scatter(
    mode='lines', 
    x= df3['timestamp'], 
    y=y, line=dict(color='steelblue',width=2)), secondary_y=True,)
       
fig.update_layout(
    title='BTC bids HEATMAP 1H  ',
    xaxis_nticks=36)
fig['layout'].update(plot_bgcolor='black')
fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
fig.update_xaxes(visible=False)

pio.write_html(fig, file='plotly_figure.html', auto_open=True)
