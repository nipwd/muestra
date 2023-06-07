import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import ccxt

# Cargar datos
symbol= 'BTC/USDT'
timeframe='1h'
binance = ccxt.binance()
data = binance.fetchOHLCV(symbol, timeframe)
data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close','volume'])

# Procesar datos
data['cuerpo'] = abs(data['open'] - data['close'])
data['mecha_sup'] = data['high'] - data[['open', 'close']].max(axis=1)
data['mecha_inf'] = data[['open', 'close']].min(axis=1) - data['low']
data['patron'] = np.nan

# Identificar patrones
data.loc[data['cuerpo'] < data['cuerpo'].shift(1), 'patron'] = 'martillo'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_sup'] > 2*data['cuerpo']), 'patron'] = 'estrella fugaz'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['mecha_inf'] > 2*data['cuerpo']), 'patron'] = 'palo colgado'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['mecha_inf'] <= 0.2*data['cuerpo']), 'patron'] = 'hombre colgado'
data.loc[(data['cuerpo'] > 2*data['cuerpo'].shift(1)) & (data['cuerpo'] > data['cuerpo'].shift(2)), 'patron'] = 'envolvente alcista'
data.loc[(data['cuerpo'] < 2*data['cuerpo'].shift(1)) & (data['cuerpo'] < data['cuerpo'].shift(2)), 'patron'] = 'envolvente bajista'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['cuerpo'].shift(1) < data['cuerpo'].shift(2)), 'patron'] = 'martillo invertido'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_sup'] <= 0.2*data['cuerpo']) & (data['mecha_inf'] > 2*data['cuerpo']), 'patron'] = 'lápida doji'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_sup'] <= 0.2*data['cuerpo']) & (data['mecha_inf'] <= 0.2*data['cuerpo']), 'patron'] = 'doji'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['mecha_inf'] < data['cuerpo']/2) & (data['mecha_sup'] < data['cuerpo']/2), 'patron'] = 'shooting star'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['mecha_inf'] < data['cuerpo']/2) & (data['mecha_sup'] > data['cuerpo']), 'patron'] = 'hammer'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_inf'] > data['cuerpo']) & (data['mecha_sup'] < data['cuerpo']/2), 'patron'] = 'inverted hammer'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_inf'] < data['cuerpo']/3) & (data['mecha_sup'] > data['cuerpo']/3), 'patron'] = 'doji dragonfly'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_inf'] > data['cuerpo']/3) & (data['mecha_sup'] < data['cuerpo']/3), 'patron'] = 'doji gravestone'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['mecha_inf'] < data['cuerpo']/3) & (data['mecha_sup'] > data['cuerpo']/3), 'patron'] = 'bullish doji star'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_inf'] < data['cuerpo']/3) & (data['mecha_sup'] > data['cuerpo']/3), 'patron'] = 'bearish doji star'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['cuerpo'].shift(1) < data['cuerpo'].shift(2)) & (data['cuerpo'] < data['cuerpo'].shift(2)), 'patron'] = 'morning star'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['cuerpo'].shift(1) > data['cuerpo'].shift(2)) & (data['cuerpo'] > data['cuerpo'].shift(2)), 'patron'] = 'evening star'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_inf'] > data['cuerpo']*2) & (data['mecha_sup'] < data['cuerpo']/2), 'patron'] = 'bearish harami cross'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['mecha_inf'] < data['cuerpo']/3) & (data['mecha_sup'] > data['cuerpo']*2), 'patron'] = 'bullish harami cross'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['mecha_inf'] > data['cuerpo']*2) & (data['mecha_sup'] < data['cuerpo']/2) & (data['cuerpo'].shift(1) > data['cuerpo'].shift(2)), 'patron'] = 'dark cloud cover'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['mecha_inf'] < data['cuerpo']/3) & (data['mecha_sup'] > data['cuerpo']*2) & (data['cuerpo'].shift(1) < data['cuerpo'].shift(2)), 'patron'] = 'piercing line'
data.loc[(data['cuerpo'] > data['cuerpo'].shift(1)) & (data['cuerpo'] > data['cuerpo'].shift(2)) & (data['cuerpo'] > data['cuerpo'].shift(3)) & (data['cuerpo'] > data['cuerpo'].shift(4)) & (data['mecha_inf'] > data['cuerpo']/2), 'patron'] = 'rising sun'
data.loc[(data['cuerpo'] < data['cuerpo'].shift(1)) & (data['cuerpo'] < data['cuerpo'].shift(2)) & (data['cuerpo'] < data['cuerpo'].shift(3)) & (data['cuerpo'] < data['cuerpo'].shift(4)) & (data['mecha_sup'] > data['cuerpo']/2), 'patron'] = 'falling star'



# Clasificación de patrones
X = data[['open', 'high', 'low', 'close', 'cuerpo', 'mecha_sup', 'mecha_inf']]
y = data['patron']
data.dropna(inplace=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
data.dropna(inplace=True)

data.to_csv('csv/patrones.csv')
clf = DecisionTreeClassifier(random_state=42)
# Encontrar índices de filas con valores faltantes en y_train
missing_indices = y_train[y_train.isnull()].index

# Eliminar filas con valores faltantes en ambos X_train y y_train
X_train.drop(index=missing_indices, inplace=True)
y_train.drop(index=missing_indices, inplace=True)

# Ajustar el modelo
clf.fit(X_train, y_train)


# Prueba del modelo
y_pred = clf.predict(X_test)
print(y_pred)
accuracy = accuracy_score(y_test, y_pred)
print("Precisión del modelo: {:.2f}%".format(accuracy*100))
