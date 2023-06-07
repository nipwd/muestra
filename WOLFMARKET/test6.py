import pandas as pd
"""
# Lee el archivo csv como un dataframe
df = pd.read_csv('/home/main/WOLFMARKET/csv/BTC_DATA_HEAT_MAP.csv')

# Convierte la columna "date" a objetos datetime
df['date'] = pd.to_datetime(df['date'])

# Redondea los valores de fecha y hora a la unidad de minuto más cercana para eliminar los segundos
df['date'] = df['date'].dt.floor('min')
df.to_csv('csv/BTC_DATA_HEAT_MAP2.csv',index=False,header=False,mode='a')

# Imprime el dataframe resultante
print(df)


input("=========close==============")
import plotly.io as pio
"""
import plotly.graph_objs as go
df2_2 =pd.read_csv('/home/main/WOLFMARKET/csv/BTC_DATA_HEAT_MAP2.csv')
df2 =df2_2[-1000:]
df2['date'] = pd.to_datetime(df2['date'])
df2.set_index('date', inplace=True)
df2_min = df2.resample('5T').mean()
print(df2_min)
df_bid = pd.DataFrame(df2_min['bid_volume'])
df_ask = pd.DataFrame(df2_min['ask_volume'])


total_bid_volume = df2_2['bid_volume'].sum()
print(total_bid_volume)
total_ask_volume = df2_2['ask_volume'].sum()
print(total_ask_volume)
if total_bid_volume < total_ask_volume:
    print("+ venta")
if total_ask_volume < total_bid_volume:
    print("+ compra")

layout = go.Layout(title=f'Buyers and Sellers spread', font={'color': 'white'}, paper_bgcolor='#000000', plot_bgcolor='#000000', height=1000, autosize=True,dragmode='pan',xaxis=dict(rangeslider=dict(visible=False)))
fig = go.Figure(layout=layout)
fig.add_trace(go.Scatter(x=df2_min.index, y=df_ask['ask_volume'], mode='lines', name='Sellers',line=dict(color='#ff1e00', width=3)))
fig.add_trace(go.Scatter(x=df2_min.index, y=df_bid['bid_volume'], mode='lines', name='Buyers',line=dict(color='#07c700', width=3)))
fig.add_trace(go.Bar(x=df2_min.index, y=df_ask['ask_volume'], name='Sellers', marker_color='#ff1e00'))#BEAR
fig.add_trace(go.Bar(x=df2_min.index, y=df_bid['bid_volume'], name='Buyers', marker_color='#07c700'))#Bull
config = {'displayModeBar': False, 'scrollZoom': True,'modeBarButtons': [['drawline', 'drawopenpath','drawcircle', 'drawrect', 'eraseshape']]}
html_fig = fig.to_html(full_html=False,config=config)
fig.show()