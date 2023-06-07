import requests
import time
import json
import time
import pandas as pd
import schedule  
# creo df
df = pd.DataFrame(columns=["fecha", "compra", "venta"])


def get_cotizacion():
    req3 = requests.get('https://api.bluelytics.com.ar/v2/latest')
    jsonarray3 = json.loads(req3.text)
    dict = str(jsonarray3).split("blue")
    dict= dict[1]
    dict = dict.split("oficial_euro")
    dict = dict[0]
    dict = dict.replace("':"," ").replace("value_sell"," ").replace("value_buy","").replace("}","").replace("'","").split(",")
    dolar_compra = dict[2]
    dolar_venta =  dict[1]
    # Obtener fecha actual
    fecha = time.strftime("%Y-%m-%d %H:%M:%S")
    # Agregar fila al DataFrame con los valores obtenidos
    df.loc[len(df)] = [fecha, dolar_compra, dolar_venta]
    #df.to_csv('csv/cotizacion.csv')
    # Mostrar el DataFrame resultante
    print(df)


while True:
    get_cotizacion()
    time.sleep(60)
