import dash
from dash import html
from dash import dcc
import ccxt
import io
from datetime import datetime
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, update_title=None)
app.layout = html.Div([
    dcc.Input(id='ticker-input', type='text', value='BTC/USDT'),

    dcc.Graph(id='graph', figure=dict(data=[dict(x=[], y=[], type='scatter')]), style={'height': 600}),
    dcc.Interval(id="interval", interval=5000),
    dcc.Store(id='offset', data=0),
    dcc.Dropdown(id='timeframe-dropdown', options=[
        {'label': '1 minute', 'value': '1m'},
        {'label': '5 minutes', 'value': '5m'},
        {'label': '15 minutes', 'value': '15m'},
        {'label': '30 minutes', 'value': '30m'},
        {'label': '1 hour', 'value': '1h'},
        {'label': '4 hours', 'value': '4h'},
        {'label': '1 day', 'value': '1d'},
        {'label': '1 week', 'value': '1w'}
    ], value='1d'),
    dcc.Dropdown(id='chart-type-dropdown', options=[
        {'label': 'Line Chart', 'value': 'line'},
        {'label': 'Candlestick Chart', 'value': 'candlestick'}
    ], value='line')
])

exchange = ccxt.binance()

@app.callback(
    [Output('graph', 'figure'), Output('offset', 'data')],
    [Input('interval', 'n_intervals'), Input('timeframe-dropdown', 'value'), Input('chart-type-dropdown', 'value'), Input('ticker-input', 'value')],
    [State('offset', 'data')]
)

def update_graph(n, timeframe, chart_type, ticker_symbol, offset):
    ohlcv = exchange.fetch_ohlcv(ticker_symbol, timeframe=timeframe, limit=2000)
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
    return {'data': [chart_data], 
            'layout': dict(xaxis=dict(range=[min(x), max(x)]), yaxis=dict(range=[min(y), max(y)]))}, offset

html_file = io.StringIO()
html_file.write(str(app.index_string))
html_file.seek


with open('index.html', 'w') as file:
    file.write(html_file.read())

if __name__ == '__main__':
    app.run_server()
