"""Idea basica de riesgo beneficio segun operaciones realizadas, recopilando datos historicos y datos del usuario"""

# Importar bibliotecas necesarias
import pandas as pd
from binance.client import Client

# Configurar la API de Binance
api_key = 'TU_API_KEY'
api_secret = 'TU_API_SECRET'
client = Client(api_key, api_secret)

# Obtener los datos de precios históricos de un activo específico
symbol = 'BTCUSDT'
klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, '30 days ago UTC')
df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df.drop(['close_time', 'quote_asset_volume', 'trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], axis=1, inplace=True)
df = df.astype(float)

# Calcular la media móvil de 30 días y la desviación estándar
df['MA30'] = df['close'].rolling(window=30).mean()
df['STD30'] = df['close'].rolling(window=30).std()

# Calcular los márgenes de riesgo-beneficio
df['upper_band'] = df['MA30'] + (df['STD30'] * 2)
df['lower_band'] = df['MA30'] - (df['STD30'] * 2)
df['profit_margin'] = df['upper_band'] - df['close']
df['stop_loss'] = df['close'] - df['lower_band']

# Dividir el monto total en unidades de trading y ajustar automáticamente según las operaciones
total_amount = 1000
units = 10
unit_amount = total_amount / units
df['unit_amount'] = unit_amount
df['position'] = None

for i in range(len(df)):
    if df['close'][i] > df['upper_band'][i]:
        df['position'][i] = 'SELL'
        units -= 1
        unit_amount = total_amount / units
        df['unit_amount'][i] = unit_amount
    elif df['close'][i] < df['lower_band'][i]:
        df['position'][i] = 'BUY'
        units += 1
        unit_amount = total_amount / units
        df['unit_amount'][i] = unit_amount

# Imprimir los resultados
print(df.tail())
