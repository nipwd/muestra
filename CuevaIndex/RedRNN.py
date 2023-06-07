import tensorflow as tf
import pandas as pd
import numpy as np
import ccxt
from time import sleep
import sys
total=100

# Define la función que muestra la barra de progreso
def progress_bar(current, total,mensaje_txt, bar_length=50):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    mensaje = mensaje_txt
    sys.stdout.write(f'\r{mensaje}: [%s%s] %d%%' % (arrow, spaces, percent))
    sys.stdout.flush()




# Función para crear secuencias de precios históricos
def create_sequences(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:i + time_steps])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)


# Crear una instancia del exchange de Binance
exchange = ccxt.binanceusdm()

# Obtener los datos históricos de precios de Bitcoin en intervalos diarios
bars = exchange.fetch_ohlcv('BTC/USDT', '1d')

# Crear un DataFrame de pandas con los datos históricos
df = pd.DataFrame(bars, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

# Convertir la columna de marcas de tiempo a formato de fecha
df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')

# Seleccionar las columnas de precios
prices = ['Open', 'High', 'Low', 'Close']
df = df[['Date'] + prices]

# Crear una nueva columna con el precio futuro
df['Price_Future'] = df['Close'].shift(-1)

# Eliminar la última fila (ya que no tenemos el precio futuro)
df = df[:-1]

# Convertir los datos a numpy arrays
data = df[prices].values
target = df['Price_Future'].values

# Dividir los datos en conjuntos de entrenamiento y prueba
train_size = int(len(data) * 0.8)
test_size = len(data) - train_size
X_train, y_train = data[0:train_size,:], target[0:train_size]
X_test, y_test = data[train_size:len(data),:], target[train_size:len(target)]

# Crear secuencias de precios históricos
time_steps = 30
X_train, y_train = create_sequences(X_train, y_train, time_steps)
X_test, y_test = create_sequences(X_test, y_test, time_steps)

# Crear el modelo de RNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(time_steps, len(prices))),
    tf.keras.layers.LSTM(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001), return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])
#Compilar el modelo
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='mean_squared_error', optimizer=optimizer)

#Entrenar el modelo
history = model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1, validation_split=0.2)

#Crear un DataFrame con las predicciones para los próximos 30 días
future_dates = pd.date_range(start=df['Date'].iloc[-1], periods=30, freq='D')[1:]
future_df = pd.DataFrame({'Date': future_dates})

# Hacer las predicciones para los próximos 30 días
for i in range(len(future_dates)):
    # Predecir el precio futuro
    future_price = model.predict(np.expand_dims(X_test[-1], axis=0))[0][0]

    # Añadir la predicción al DataFrame
    future_df.loc[i, 'Price'] = future_price

    # Actualizar X_test con la nueva predicción
    X_test = np.concatenate([X_test, np.expand_dims(X_test[-1], axis=0)])[1:]

    # Actualizar y_test con la nueva predicción
    y_test = np.append(y_test, future_price)

# Calcular el error de las predicciones
rmse = np.sqrt(np.mean((future_df['Price'] - future_df['Price'].mean())**2))

# Crear un DataFrame con los resultados del modelo
print(len(y_test))
print(len(future_df['Price'].values[:-1]))

results_df = pd.DataFrame({'Actual': y_test[:28], 'Predicted': future_df['Price'].values[:-1]})

# Guardar los resultados en un archivo CSV
results_df.to_csv('results.csv', index=False)

import matplotlib.pyplot as plt
from matplotlib import style, rcParams
from datetime import datetime

style.use('dark_background') 
rcParams['text.color'] = 'white' 
rcParams['axes.facecolor'] = 'black' 
print(results_df.columns)
# Crear un gráfico con los resultados del modelo
plt.figure(figsize=(20, 8))
plt.plot(df['Date'], df['Close'], label='Actual')
plt.plot(future_df['Date'], future_df['Price'], label='Predicted')
plt.title('Precio de Bitcoin', fontsize=14)
plt.xlabel('Fecha', fontsize=12)
plt.ylabel('Precio (USD)', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=12)
plt.yticks([1000,5000,10000, 15000, 20000, 25000, 30000, 35000,40000, 45000, 50000,55000,60000,65000,70000], ['1k','5K','10k', '15k', '20k', '25k', '30k','35k','40k','45k','50k','55k','60k','65k','70k'])
plt.grid(axis='y')
plt.savefig('test_btc.png')
print("finish")

#progress bar 
for i in range(total):
    sleep(0.01)  # Tarea que lleva tiempo  === 20"segundos" / 100 "-"
    progress_bar(i + 1, total,mensaje_txt= "Generando imagen")

sys.stdout.write('\n')  # linea en blanco para evitar sobrescribir la barra de progreso
plt.show()