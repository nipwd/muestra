import pandas as pd
import plotly.graph_objs as go
from prophet import Prophet
import prophet
import matplotlib.pyplot as plt

df = pd.read_csv('csv/hechos.csv')

# dayfirst=True == formato dd//mm//yy
df['fecha'] = pd.to_datetime(df['fecha'], format='mixed', dayfirst=True, errors='coerce')
filtro = (df['equipo_instalado'] != "Sin Instalado") & ((df['region_cliente'] == "CAPITAL FEDERAL") | (df['region_cliente'] == "OESTE"))
nuevo_df = df[filtro].groupby('fecha')['equipo_instalado'].count().reset_index()
nuevo_df.columns = ['fecha', 'total_equipos']

print(nuevo_df)
x_values = nuevo_df['fecha']
y_values = nuevo_df['total_equipos']
forecast_df = nuevo_df
forecast_df.rename(columns={'fecha':'ds','total_equipos':'y'},inplace=True)
forecast_df.head()
m = Prophet()
m = Prophet(daily_seasonality = True)
m = Prophet(weekly_seasonality=True)
m = Prophet(yearly_seasonality=True)
m.fit(forecast_df)
future = m.make_future_dataframe(periods=15)
forecast = m.predict(future)
fig1 = m.plot(forecast)
plt.savefig('fig1.jpg')

#figura HTML con Plotly
layout = go.Layout(title=f'Forecast Total de equipos', font={'color': 'black'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=1000, autosize=True,dragmode='pan',xaxis=dict(rangeslider=dict(visible=False)))
fig = go.Figure(layout=layout)
fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['y'],mode='lines',line=dict(color='#00c3ff', width=3),name='Valores'))
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicciones',line=dict(color='#f7d200', width=1)))
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Intervalo superior',line=dict(color='#1eff00', width=1)))
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Intervalo inferior',line=dict(color='#ff0808', width=1)))
fig.show()
