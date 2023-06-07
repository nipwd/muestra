import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style, rcParams
from datetime import datetime

df = pd.read_csv('historico.csv')
future_df = pd.read_csv('futuro.csv')

style.use('dark_background') 
rcParams['text.color'] = 'white' 
rcParams['axes.facecolor'] = 'black' 

fig = plt.figure(figsize=(10, 6))

df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
future_df['Date'] = future_df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

plt.plot(df['Date'], df['Price'])
plt.plot(future_df['Date'], future_df['Price'], color='y')
plt.title('Precio BTC', color='white')
plt.xlabel('Dia', color='white')
plt.ylabel('Precio', color='white')
plt.yticks([12000, 16000, 20000, 25000, 30000], ['12k', '16k', '20k', '25k', '30k'])

plt.grid(axis='y')
plt.show()
