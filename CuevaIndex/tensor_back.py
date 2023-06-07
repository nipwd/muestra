import tensorflow as tf 
import pandas as pd
import numpy as np
import ccxt

# Crear una instancia del exchange de Binance
exchange = ccxt.binanceusdm()

# Obtener los datos históricos de precios de Bitcoin en intervalos diarios
bars = exchange.fetch_ohlcv('BTC/USDT', '1d')

# Crear un DataFrame de pandas con los datos históricos
df = pd.DataFrame(bars, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

# Convertir la columna de marcas de tiempo a formato de fecha
df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')

# Seleccionar solo la columna de fecha y precio
df = df[['Date', 'Close']]

# Renombrar la columna de precios a 'Price'
df = df.rename(columns={'Close': 'Price'})

# Crear una nueva columna con el precio desplazado hacia adelante un día
df['Price_Future'] = df['Price'].shift(-1)

# Eliminar la última fila (ya que no tenemos el precio futuro)
df = df[:-1]

# Convertir los datos a numpy arrays
X = df['Price'].values.reshape(-1, 1)
y = df['Price_Future'].values.reshape(-1, 1)

# Dividir los datos en conjuntos de entrenamiento y prueba
train_size = int(len(X) * 0.8)
test_size = len(X) - train_size
X_train, X_test = X[0:train_size,:], X[train_size:len(X),:]
y_train, y_test = y[0:train_size,:], y[train_size:len(y),:]

# Crear el modelo de regresión lineal
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(1,)),
    tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dense(1)
])

# Compilar el modelo
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='mean_squared_error', optimizer=optimizer)

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=100, batch_size=23, verbose=2, validation_split=0.2)

# Crear un DataFrame con las predicciones para los próximos 30 días
future_dates = pd.date_range(start=df['Date'].iloc[-1], periods=90, freq='D')[1:]
future_df = pd.DataFrame({'Date': future_dates})

# Hacer las predicciones para los próximos 30 días
for i in range(len(future_dates)):
    # Predecir el precio futuro
    future_price = model.predict(X_test[-1].reshape(-1, 1))[0][0]
    
    # Añadir la predicción al DataFrame
    future_df.loc[i, 'Price'] = future_price
    
    # Actualizar X_test con la nueva predicción
    X_test = np.append(X_test, future_price.reshape(-1, 1), axis=0)
    
    # Actualizar y_test con la nueva predicción
    y_test = np.append(y_test, future_price)

# Calcular el error de las predicciones
rmse = np.sqrt(np.mean((y_test - X_test)**2))
print("RMSE:", rmse)
print("Tamaño de X_test:", X_test.shape)
print("Tamaño de y_test:", y_test.shape)


# Crear un DataFrame con los resultados del modelo
results_df = pd.DataFrame({'Actual': y_test, 'Predicted': X_test.flatten()})

# Guardar los resultados en un archivo CSV
results_df.to_csv('results.csv', index=False)


import matplotlib.pyplot as plt
from matplotlib import style, rcParams
from datetime import datetime

style.use('dark_background') 
rcParams['text.color'] = 'white' 
rcParams['axes.facecolor'] = 'black' 

# Crear un gráfico con los resultados del modelo
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Price'], label='Actual')
plt.plot(future_df['Date'], future_df['Price'], label='Predicted')
plt.title('Precio de Bitcoin', fontsize=14)
plt.xlabel('Fecha', fontsize=12)
plt.ylabel('Precio (USD)', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=12)
plt.yticks([12000, 16000, 20000, 25000, 28000], ['12k', '16k', '20k', '25k', '28k'])
plt.grid(axis='y')
plt.savefig('test_btc.png')
plt.show()

