import dash
import dash_core_components as dcc
import dash_html_components as html
import ccxt
import io
from datetime import datetime
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State

# Example app.
app = dash.Dash(__name__, update_title=None, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div(style={'backgroundColor': '#303030', 'color': 'white'}, children=[
    dcc.Input(id='ticker-input', type='text', value='BTC/USDT', style={'backgroundColor': '#424242', 'color': 'white'}),
    dcc.Dropdown(id='timeframe-dropdown', options=[
        {'label': '1 minute', 'value': '1m'},
        {'label': '5 minutes', 'value': '5m'},
        {'label': '15 minutes', 'value': '15m'},
        {'label': '30 minutes', 'value': '30m'},
        {'label': '1 hour', 'value': '1h'},
        {'label': '4 hours', 'value': '4h'},
        {'label': '1 day', 'value': '1d'},
        {'label': '1 week', 'value': '1w'}
    ], value='1d', style={
        'color': '#fff', # Cambiar el color del texto a blanco
        'backgroundColor': '#000000' # Cambiar el color de fondo a un tono de gris oscuro
    }),
    dcc.Graph(id='graph', figure=dict(data=[dict(x=[], y=[], type='scatter')]), style={'height': 800, 'backgroundColor': '#000000', 'color': 'white'}),
    dcc.Interval(id="interval", interval=5000),
    dcc.Store(id='offset', data=0),
    dcc.Dropdown(id='chart-type-dropdown', options=[
        {'label': 'Line Chart', 'value': 'line'},
        {'label': 'Candlestick Chart', 'value': 'candlestick'}
    ], value='line', style={
        'color': '#fff', # Cambiar el color del texto a blanco
        'backgroundColor': '#000000' # Cambiar el color de fondo a un tono de gris oscuro
    })
])


exchange = ccxt.binance()

@app.callback(
    [Output('graph', 'figure'), Output('offset', 'data')],
    [Input('interval', 'n_intervals'), Input('timeframe-dropdown', 'value'), Input('chart-type-dropdown', 'value'), Input('ticker-input', 'value')],
    [State('offset', 'data')]
)

def update_graph(n, timeframe, chart_type, ticker_symbol, offset):
    ohlcv = exchange.fetch_ohlcv(ticker_symbol, timeframe=timeframe, limit=2000)
    valor = (str(ohlcv[-1]).split(",")[1])
    global datos_relevantes
    datos_relevantes =(valor,ticker_symbol)
    fx =pd.DataFrame(columns=["ticker_symbol", "valor"])
    fx.loc[len(datos_relevantes)] = [ticker_symbol, valor]
    fx.to_csv('csv/test.csv',index=False)
    ##########
    x = [datetime.fromtimestamp(ohlcv[i][0] / 1000) for i in range(len(ohlcv))]
    y = [ohlcv[i][1] for i in range(len(ohlcv))]
    offset = (offset + 1) % len(x)
    if chart_type == 'candlestick':
        chart_data = go.Candlestick(x=x[offset:], open=[ohlcv[i][1] for i in range(offset, len(ohlcv))], 
                                    high=[ohlcv[i][2] for i in range(offset, len(ohlcv))], 
                                    low=[ohlcv[i][3] for i in range(offset, len(ohlcv))], 
                                    close=[ohlcv[i][4] for i in range(offset, len(ohlcv))])
    else:
        chart_data = {'x': x[offset:], 'y': y[offset:], 'mode': 'lines'}
    return {
        'data': [chart_data], 
        'layout': dict(
            xaxis=dict(
                range=[min(x), max(x)],
                gridcolor='rgb(44, 49, 56)',
                linecolor='white',
                linewidth=2
            ), 
            yaxis=dict(
                range=[min(y), max(y)],
                gridcolor='rgb(44, 49, 56)',
                linecolor='white',
                linewidth=2
            ),
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            margin=dict(l=40, r=40, t=10, b=40),
            gridwidth=1,
            hovermode='x'
        )
    }, offset

if __name__ == '__main__':
    with open('/home/main/WOLFMARKET/templates/new_index.html', 'r') as file:
        html_string = file.read()

        app.index_string = html_string
        app.run_server(port=8080)
