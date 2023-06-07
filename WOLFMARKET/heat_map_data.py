logoscript= r"""

| | | |/__\| | | __|  V  |/  \| _ \ |/ / __|_   _| 
| 'V' | \/ | |_| _|| \_/ | /\ | v /   <| _|  | |   
!_/ \_!\__/|___|_| |_| |_|_||_|_|_\_|\_\___| |_|   
  __  ___ __  ___ ___ __  __   __  _  __           
 /__\| _ \ _\| __| _ \  \/__\ /__\| |/ /           
| \/ | v / v | _|| v / -< \/ | \/ |   <            
 \__/|_|_\__/|___|_|_\__/\__/ \__/|_|\_\           
/' _/ / _/ _ \ | _,\_   _|                         
`._`.| \_| v / | v_/ | |                           
|___/ \__/_|_\_|_|   |_|
"""
# font = stforek
# from http://www.patorjk.com/software/taag/#p=display&f=Stforek&t=stforek

import ccxt
import datetime
import pandas as pd
import time
import os.path
from tabulate import tabulate
import traceback

df2 = pd.DataFrame()

def BTC_DATA_HEAT_MAP():
    symbol= 'BTC/USDT'
    timeframe='1h'
    binance = ccxt.binance()
    bars = binance.fetchOHLCV(symbol, timeframe)
    df3= pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
    actual_price= int(df3['close'].iloc[-1])
    OR_BOOK = binance.fetch_bids_asks(symbol)
    bid = OR_BOOK['BTC/USDT']['bid']
    bid_volume = OR_BOOK['BTC/USDT']['bidVolume']
    ask = OR_BOOK['BTC/USDT']['ask']
    ask_volume = OR_BOOK['BTC/USDT']['askVolume']
    now = datetime.datetime.now()
    three_hours_later = now + datetime.timedelta(hours=3)
    date = three_hours_later.strftime("%Y-%m-%d %H:%M:%S")
    df2 = pd.DataFrame([[date, actual_price, bid_volume, actual_price, ask_volume]],
    columns=['date','bid','bid_volume','ask', 'ask_volume'])
    df2.to_csv('csv/BTC_DATA_HEAT_MAP.csv',index=False,header=False,mode='a')

while True:
    try:
        # Borrar la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        # Actualizar el DataFrame con nuevos datos
        df2 = pd.read_csv('csv/BTC_DATA_HEAT_MAP.csv')
        # Imprimir las últimas 5 filas del DataFrame
        print(logoscript)
        print(tabulate(df2.tail(5), headers='keys', tablefmt='github', showindex=False))
        BTC_DATA_HEAT_MAP()
        #time.sleep(1)
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")
        break
        
    except Exception as e:
        traceback.print_exc()
        time.sleep(5)


# run bash whit   ./heat_map_data.sh
