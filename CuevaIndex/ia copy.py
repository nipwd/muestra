import ccxt
import pandas as pd
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Obtener datos históricos
exchange = ccxt.binanceusdm()
bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1d')
df = pd.DataFrame(bars, columns=['timestamp','Open','High','Low','Close','Volume'])

# Convertir timestamp a fecha
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Seleccionar solo las columnas necesarias
df = df[['timestamp', 'Open', 'High', 'Low', 'Volume', 'Close']]

# Dividir los datos en entrenamiento y prueba
train_data = df[:-30]
test_data = df[-30:]

# Entrenar modelo SVR
regressor = SVR(kernel='linear', C=1e3)
regressor.fit(train_data[['Open', 'High', 'Low', 'Volume']], train_data['Close'])

# Generar lista de fechas de los próximos 30 días
start_date = test_data.iloc[-1]['timestamp']
end_date = start_date + timedelta(days=30)
date_list = pd.date_range(start=start_date, end=end_date, freq='D').tolist()

# Generar DataFrame con fechas y valores aleatorios para las columnas Open, High, Low y Volume
future_data = pd.DataFrame({'timestamp': date_list})
future_data['Open'] = np.random.rand(len(date_list))
future_data['High'] = np.random.rand(len(date_list))
future_data['Low'] = np.random.rand(len(date_list))
future_data['Volume'] = np.random.rand(len(date_list))
future_data['Price'] = np.nan

# Realizar predicciones para cada fecha en la lista
for i, date in enumerate(date_list):
    data = future_data.iloc[[i]]
    future_close = regressor.predict(data[['Open', 'High', 'Low', 'Volume']])
    future_data.loc[future_data['timestamp'] == date, 'Price'] = future_close[0]

# Agregar predicciones al DataFrame original
df = df.append(future_data, ignore_index=True)
df.to_csv('datos.csv', index=False)
print(df)

# Graficar resultados
plt.plot(df[-30:]['Close'], label='Actual')
plt.plot(df[-30:]['Close'].shift(-1), linestyle='--', label='Predicción')
plt.legend()
plt.show()