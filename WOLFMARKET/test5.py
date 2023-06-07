import requests
import time
import locale
from tabulate import tabulate

# Configuración de parámetros
api_url = "https://blockchain.info/rawaddr/"
threshold_btc = 1000
time_window = 3600 # En segundos
ballena_alerta = 5
currency = "USD" # La moneda de referencia para el precio de BTC

# Configurar locale para la moneda
locale.setlocale(locale.LC_ALL, "")

# Diccionario para almacenar las direcciones de ballenas y su contador
ballenas_dict = {}

# Función para obtener datos de transacción de una dirección
def get_transactions(address):
    url = api_url + address
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["txs"]
    else:
        return None

# Función para obtener el precio de BTC
def get_btc_price():
    url = f"https://api.coindesk.com/v1/bpi/currentprice/{currency}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["bpi"][currency]["rate_float"]
    else:
        return None

# Función para formatear el valor de BTC como moneda
def format_btc_value(btc_value):
    return locale.currency(btc_value, grouping=True)

# Función para identificar ballenas en las transacciones
def detect_ballenas():
    while True:
        # Obtener transacciones recientes
        transactions = get_transactions("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

        if transactions is not None:
            btc_price = get_btc_price()

            for tx in transactions:
                for input_ in tx["inputs"]:
                    if input_["prev_out"]["value"] >= threshold_btc:
                        addr = input_["prev_out"]["addr"]
                        btc_value = input_["prev_out"]["value"] * 1e-8 * btc_price
                        if addr in ballenas_dict:
                            ballenas_dict[addr]["count"] += 1
                            ballenas_dict[addr]["total_btc_value"] += btc_value
                        else:
                            ballenas_dict[addr] = {"count": 1, "total_btc_value": btc_value}
                for output in tx["out"]:
                    if output["value"] >= threshold_btc:
                        addr = output["addr"]
                        btc_value = output["value"] * 1e-8 * btc_price
                        if addr in ballenas_dict:
                            ballenas_dict[addr]["count"] += 1
                            ballenas_dict[addr]["total_btc_value"] += btc_value
                        else:
                            ballenas_dict[addr] = {"count": 1, "total_btc_value": btc_value}

            # Ordenar las direcciones por valor total de BTC
            sorted_ballenas = sorted(ballenas_dict.items(), key=lambda x: x[1]["total_btc_value"], reverse=True)

            # Formatear el ranking de direcciones de ballenas como tabla
            table = []
            for i, (addr, info) in enumerate(sorted_ballenas):
                table.append([i+1,
            addr,
            info["count"],
            format_btc_value(info["total_btc_value"])
        ])

        # Calcular el valor total de BTC en posesión de las ballenas
        total_btc_value = sum([info["total_btc_value"] for _, info in ballenas_dict.items()])

        # Formatear el valor total de BTC como moneda
        formatted_total_btc_value = format_btc_value(total_btc_value)

        # Imprimir los resultados usando tabulate
        print(f"Valor total de BTC: {formatted_total_btc_value}\n")
        print(tabulate(table, headers=["Rank", "Dirección", "Cantidad de transacciones", f"Valor total en {currency}"], tablefmt="github"))

    # Esperar antes de revisar de nuevo
    time.sleep(time_window)
detect_ballenas()

