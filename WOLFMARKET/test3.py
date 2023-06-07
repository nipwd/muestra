
import plotly.graph_objs as go
import fbprophet
from fbprophet import Prophet
from fbprophet.plot import plot
import ccxt
import pandas as pd

symbol= 'BTC/USDT'
timeframe='1h'
print('Prophet')
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
m = Prophet(yearly_seasonality = True)
m = Prophet(daily_seasonality=True)
m.fit(forecast_df)
future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)
fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['y'], mode='lines', name='Datos',line=dict(color='#00c3ff')))
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicciones',line=dict(color='#f7d200')))
fig.update_layout(title='Mi gráfico Prophet')

html_fig = fig.to_html(full_html=False, config={'displayModeBar': False})
print(html_fig)