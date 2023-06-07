import time # type: ignore
from datetime import timedelta
from time import sleep
import csv
import datetime
import sqlite3
from sqlite3 import Error
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import telebot
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
import selenium
import os
import pickle
from tabulate import tabulate
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json 
from cryptography.fernet import Fernet




start_time = time.time()
logoscript= r"""

    ,]╦Ñ╦,
    ]░░░░░░Nw
    ]╙********"╦,    ╓▄▄▄▄▄▄┌      ╔▄∩                               ,
    ],,,,   ,,,░░░N  ╙▀▀██▀▀└,▄▄▄  ║█▌  ,▄▄▄    ▄▄▄▄  ▄▄▄▄  ▄▄▄▄▄  ▄██▄, ▄▄▄▄  ▄▄▄ç
    ]░░░∩   ░░░░░░░     ██  ▄█▌⌠██Γ║█▌ ▄█▀⌠██∩╓██└╙└ ██▀▀██ ██"▀██ ╙██╙`▐██▀╙╓██└▀██
    ]░░░∩   ░░░░Ñ╙      ██  ███▀▀▀ ║█▌ ██▌▀▀▀ ║█▌    ██▀▀▀▀ ██  ██⌐ ██  ▐██  ║█▌ ,██
    ]░░░U   ░╩^         ██   ▀███▀ ╙██▌ ▀███▀  ▀███▀ ╙▀██▀Γ ██  ▀█  ▀███ █▀   ▀███▀
    ]░░░░Ñ╨`

"""
print(logoscript)

#descargar csv
# Carga las credenciales desde el archivo JSON
key =os.environ.get('NETLIFE_GDRIVE_KEY')
# Crea un objeto Fernet con la llave
cipher_suite = Fernet(key.encode())

# Lee el archivo encriptado JSON
with open('keys_ECRIPTED.json', 'rb') as encrypted_json_file:
    encrypted_json = encrypted_json_file.read()

# Descifra el contenido del archivo JSON
decrypted_json = cipher_suite.decrypt(encrypted_json)
json_str = decrypted_json.decode()

# Convierte la cadena en formato JSON a un objeto Python
json_data = json.loads(json_str)
creds = service_account.Credentials.from_service_account_info(json_data)

# Continúa con el resto del código
drive_service = build('drive', 'v3', credentials=creds)

# Crea el cliente de GDrive usando las credenciales de autenticación
drive_service = build('drive', 'v3', credentials=creds)
# ID del archivo que se descarga
file_id = ''
# Nombre y ruta del archivo output
output_file = 'csv/hechos.csv'
# Descarga el archivo de GDrive
request = drive_service.files().get_media(fileId=file_id)
fh = io.FileIO(output_file, mode='wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
# Verificar si se descargo
if done:
    print('El archivo CSV se ha descargado correctamente')
else:
    print('No se ha podido descargar el archivo')

#descargar db
# ID del archivo que se descargará
file_id = ''
# Nombre y ruta del archivo output
output_file = 'db.sqlite3'

# Descarga el archivo de GDrive
request = drive_service.files().get_media(fileId=file_id)
fh = io.FileIO(output_file, mode='wb')
downloader = MediaIoBaseDownload(fh, request)
done = False

while done is False:
    status, done = downloader.next_chunk()

# Verificar si se descargo
if done:
    print('El archivo se descargo correctamente')
else:
    print('No se pudo descargar el archivo')


bot = telebot.TeleBot('')
today = datetime.date.today()
today = (today.strftime('%d-%m-%Y'))
page = ""
chrome_driver_binary = '/home/dev/scrips/telecentro/driver/chromedriver' #cambiar ruta especifica segun
homedir = os.path.expanduser("~")
webdriver_service = Service("chromedriver")
chrome_options = Options()
#chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
actionChains = ActionChains(driver)
driver.get(page)
title = driver.title
final_url = driver.current_url
print(final_url)
print("Empezando el scrap en: ",title,final_url)

def print_last_five():  #imprimir los ultimos 5 de la lista hechos
    df = pd.read_csv("csv/hechos.csv") # reemplaza "ruta/del/archivo.csv" con la ruta de tu archivo CSV
    df['tecnico'] = df['tecnico'].str.split().str[0]
    last_five = df[['tecnico', 'equipo_instalado', 'numero_vt', 'numero_cliente']].tail(5)
    last_five_list = last_five.values.tolist()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logoscript)
    print(tabulate(last_five_list, headers=['tecnico', 'equipo_instalado', 'numero_vt', 'numero_cliente'], tablefmt='psql'))

def extract_vt_data():  #funcion para extraer todos los datos luego de hacer click en la ruta del tecnico
    numero_vt = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[11]/div[1]/div/div[2]')))
    numero_vt= numero_vt.text
    numero_cliente = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[15]/div[1]/div/div[2]')))
    numero_cliente = numero_cliente.text
    nombre_cliente = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[16]/div[1]/div/div[2]')))
    nombre_cliente=  nombre_cliente.text
    try:
        if driver.find_elements(By.XPATH,"/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[17]/div[1]/div/div[2]"):
            dni_cliente = driver.find_element(By.XPATH, "/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[17]/div[1]/div/div[2]")
            dni_cliente = dni_cliente.text
        else:
            dni_cliente= "sin dni"
    except:
        dni_cliente= "sin dni"
        pass
    direccion_cliente = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[1]/div[1]/div/div[2]')))
    direccion_cliente = direccion_cliente.text
    try:
        if driver.find_elements(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[4]/div[1]/div/div[2]'):
            localidad_cliente = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[4]/div[1]/div/div[2]')))
            localidad_cliente = localidad_cliente.text
        else:
            localidad_cliente = "Cambio de Domicilio" 
    except:
        localidad_cliente = "Cambio de Domicilio" 
        pass
    partido_cliente =   WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[6]/div[1]/div/div[2]')))
    partido_cliente = partido_cliente.text
    if driver.find_elements(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[7]/div[1]/div/div[2]'):
        telefono_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[7]/div[1]/div/div[2]').text
    else:
        telefono_cliente = "sin telefono"
    region_cliente = "ZONA GENERICA"
    try:
        if driver.find_element(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]').text == '1':
            region_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[15]/div[1]/div/div[2]').text
            raise Exception
        if driver.find_element(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]').text == '2':
            region_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[14]/div[1]/div/div[2]').text
            raise Exception
        if driver.find_element(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]').text == '3':
            region_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[14]/div[1]/div/div[2]').text
            raise Exception
    except:
        pass
    lista_datos= numero_vt,numero_cliente, nombre_cliente,dni_cliente,direccion_cliente,localidad_cliente,partido_cliente,telefono_cliente,region_cliente
    return lista_datos

def guardar_datos_sin_instalado(numero_vt, tecnico_nombre, numero_cliente, nombre_cliente, dni_cliente, direccion_cliente, localidad_cliente, partido_cliente, telefono_cliente, region_cliente): # guardar a csv las ordenes que no se instalan equipos
    equipo_instalado = "Sin Instalado"
    mac_instalado = "Sin Instalado"
    equipo_desinstalado = "Sin Retiro"
    mac_desinstalado = "Sin Retiro"
    datos = [today, tecnico_nombre, equipo_instalado, mac_instalado, equipo_desinstalado, mac_desinstalado, numero_vt, numero_cliente, nombre_cliente, dni_cliente, direccion_cliente, localidad_cliente, partido_cliente, telefono_cliente, region_cliente]
    df = pd.DataFrame([datos], columns=['fecha', 'tecnico', 'equipo_instalado', 'mac_instalado', 'equipo_desinstalado', 'mac_desinstalado', 'numero_vt', 'numero_cliente', 'nombre_cliente', 'dni_cliente', 'direccion_cliente', 'localidad_cliente', 'partido_cliente', 'telefono_cliente', 'region_cliente'])
    print_last_five()
    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)

def guardar_datos_sin_retiro(numero_vt, tecnico_nombre, numero_cliente, nombre_cliente, dni_cliente, direccion_cliente, localidad_cliente, partido_cliente, telefono_cliente, region_cliente): # guardar al csv las ordenes que se instalan equipos pero no se retira
    equipo_instalado = "Sin Instalado"
    mac_instalado = "Sin Instalado"
    equipo_desinstalado = "Sin Retiro"
    mac_desinstalado = "Sin Retiro"
    datos = [today, tecnico_nombre, equipo_instalado, mac_instalado, equipo_desinstalado, mac_desinstalado, numero_vt, numero_cliente, nombre_cliente, dni_cliente, direccion_cliente, localidad_cliente, partido_cliente, telefono_cliente, region_cliente]
    df = pd.DataFrame([datos], columns=['fecha', 'tecnico', 'equipo_instalado', 'mac_instalado', 'equipo_desinstalado', 'mac_desinstalado', 'numero_vt', 'numero_cliente', 'nombre_cliente', 'dni_cliente', 'direccion_cliente', 'localidad_cliente', 'partido_cliente', 'telefono_cliente', 'region_cliente'])
    print_last_five()
    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)

username_key =os.environ.get('NETLIFE_USERNAME_KEY')
pass_key =os.environ.get('NETLIFE_PASSWORD_KEY')

#formulario de inicio de sesion
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(username_key)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pass_key)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-in"))).click()
#if driver.find_element(By.ID,'delsession'):
    #driver.find_element(By.ID,'delsession').click()
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pass_key)
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-in"))).click()
#else:
    #pass
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*/span[contains(text(),'Vista de lista')]")))
actionChains.double_click(driver.find_element(By.XPATH, "//*/span[contains(text(),'Vista de lista')]")).perform()
input("seleccionar fecha")
#Abrir csv y comenzar scrap a partir del nombre del tecnico
with open("csv/lista_tecnicos.csv") as listatecnicos:
    reader = csv.reader(listatecnicos)
    amr_csv = [line[0] for line in reader]
    for tecnico_nombre in amr_csv:
        print("Buscando ordenes de: ",tecnico_nombre)
        buscar_tecnicos = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[14]/div[1]/main/div/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/table/tr/td[2]/div/table/tr/td[2]/input")))
        buscar_tecnicos.send_keys(Keys.CONTROL, 'a')
        buscar_tecnicos.send_keys(Keys.BACKSPACE)
        buscar_tecnicos.send_keys(f"{tecnico_nombre}" + "\n")
        boton_ruta = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, f'//*/span[contains(text(),"{tecnico_nombre}")]')))
        boton_ruta.click()  ### apreta en el nombre del tecnico y muestra ruta
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME,'tr')))
        sleep(1)
        if not driver.find_elements(By.XPATH, ("//*/td[contains(text(),'Reparación')or (contains(text(),'Cambio de Domicilio'))]") ):       # si no ecnuentra ordenes de reparacion seguir
            print(tecnico_nombre, "No Trabajo")
            pass
        if driver.find_elements(By.XPATH, "//*/div[contains(text(),'No hay actividades con fecha de referencia')]"):  # no trabajo
            print(tecnico_nombre, "No Trabajo")
            pass
        else:
            total =len(driver.find_elements(By.XPATH, ("//*/td[contains(text(),'Reparación')or (contains(text(),'Cambio de Domicilio'))]"))) #selecionar la orden y entrar al sub-menu
            print(total)
            count = 0
# Entrar en el bucle de ordenes previo conteo
            while count != total:  #cuenta el total de ordenes a recorrer y no sale del loop hasta terminar
                try:
                    ordenes = driver.find_elements(By.XPATH, ("//*/td[contains(text(),'Reparación')or (contains(text(),'Cambio de Domicilio'))]"))
                    vt = ordenes[count]
                    vt.click()
                    lista_datos =extract_vt_data()
                    numero_vt=lista_datos[0]
                    numero_cliente=lista_datos[1]
                    nombre_cliente=lista_datos[2]
                    dni_cliente=lista_datos[3]
                    direccion_cliente=lista_datos[4]
                    localidad_cliente=lista_datos[5]
                    partido_cliente=lista_datos[6]
                    telefono_cliente=lista_datos[7]
                    region_cliente=lista_datos[8]
                    if ((driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[7]/div[1]/div/div[2]')).text != "Completado"):
                        count = count + 1
                        boton_atras2 = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,"//*/span[contains(text(),'Consola de despacho')]")))
                        boton_atras2.click()
                    if driver.find_elements(By.XPATH, "//*/span[contains(text(),'Inventario')]"):   #si encuentra inventario entrar
                        datos_inv = driver.find_elements(By.XPATH, "//*/span[contains(text(),'Inventario')]")
                        lista = []
                        for e in datos_inv:
                            e.click()
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr/td/div/div[2]')))
                            if ((driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr/td/div/div[2]')).text == "Recurso"):
                                break
                            try:
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr[1]/td/div/div[2]')))
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr[3]/td/div/div[2]')))
# cuando  "instalacion" no esta presente                                                              
                                if not ((driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr[1]/td/div/div[2]')).text == "Instalado") and not ((driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr[3]/td/div/div[2]')).text == "Instalado"):
                                    guardar_datos_sin_instalado(numero_vt, tecnico_nombre, numero_cliente, nombre_cliente, dni_cliente, direccion_cliente, localidad_cliente, partido_cliente, telefono_cliente, region_cliente)
# cuando  "instalacion" esta en la primera tabla
                                if (driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr[1]/td/div/div[2]')).text == "Instalado": # INSTALACIONES
                                    elements = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr')
                                    sum_elemts= 1
                                    for element in elements:
                                        lista = []
                                        instalado = element.text.split("\n")
                                        lista.append(today)
                                        lista.append(tecnico_nombre)
                                        lista.append(instalado[0])
                                        lista.append(instalado[1])
                                        if driver.find_elements(By.XPATH, f'//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[{sum_elemts}]'):  # 1 desinstalado
                                            desinstalados = driver.find_elements(By.XPATH, f'//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[{sum_elemts}]')
                                            for x in desinstalados:
                                                desinsta_ = x.text.split("\n")
                                                if desinsta_[0] and desinsta_[1]:  # Verificar si las cadenas no están vacías
                                                    lista.append(desinsta_[0])
                                                    lista.append(desinsta_[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    sum_elemts= sum_elemts + 1
                                                    lista.pop()
                                                    print_last_five()
                                                else:
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    sum_elemts= sum_elemts + 1
                                                    lista.pop()
                                                    print_last_five()
                                        if not driver.find_elements(By.XPATH, f'//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[{sum_elemts}]'): # si no hay 1 desinstalado
                                            sum_elemts= sum_elemts + 1
                                            guardar_datos_sin_retiro(numero_vt, tecnico_nombre, numero_cliente, nombre_cliente, dni_cliente, direccion_cliente, localidad_cliente, partido_cliente, telefono_cliente, region_cliente)

# cuando  "instalacion" esta en la segunda tabla 
                                if (driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/tr[3]/td/div/div[2]')).text == "Instalado":
                                    elements = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr')
                                    sum_elemts= 1
                                    for element in elements:
                                        lista = []
                                        instalado = element.text.split("\n")
                                        lista.append(today)
                                        lista.append(tecnico_nombre)
                                        lista.append(instalado[0])
                                        lista.append(instalado[1])
                                        if driver.find_elements(By.XPATH, f'//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[{sum_elemts}]'):  # 1 desinstalado
                                            desinstalados = driver.find_elements(By.XPATH, f'//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[{sum_elemts}]')
                                            for x in desinstalados:
                                                desinsta_ = x.text.split("\n")
                                                if desinsta_[0] and desinsta_[1]:  # Verificar si las cadenas no están vacías
                                                    lista.append(desinsta_[0])
                                                    lista.append(desinsta_[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    sum_elemts= sum_elemts + 1
                                                    lista.pop()
                                                    print_last_five()
                                                else:
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    sum_elemts= sum_elemts + 1
                                                    lista.pop()
                                                    print_last_five()
                                        if not driver.find_elements(By.XPATH, f'//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[{sum_elemts}]'): # si no hay 1 desinstalado
                                            sum_elemts= sum_elemts + 1
                                            guardar_datos_sin_retiro(numero_vt, tecnico_nombre, numero_cliente, nombre_cliente, dni_cliente, direccion_cliente, localidad_cliente, partido_cliente, telefono_cliente, region_cliente)
                            except:
                                pass
                    count = count + 1
                    boton_atras = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,"//*/span[contains(text(),'Detalles de actividad')]"))) #vuelve a la lisa de ordenes 
                    boton_atras.click()
                    boton_atras2 = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,"//*/span[contains(text(),'Consola de despacho')]")))#vuelve a la lisa de ordenes
                    boton_atras2.click()
                except Exception:
                    sleep(2)

conn = sqlite3.connect('db.sqlite3'.format('pañol_app_equiposretirados'))
df = pd.read_csv('csv/hechos.csv')
print_last_five()
#bot.send_message(chat_id='291172710', text="Scrap completado con Exito") ----CHAT PRIVADO
conn.close()

sec =(time.time() - start_time)
td = timedelta(seconds=sec)
print('Tiempo de Ejecucion', td)  # Time == hh:mm:ss:
driver.close()
driver.quit()
bot.send_message(chat_id='', text="Programa finalizado, Tiempo de Ejecucion: {}".format(td))
total = df[(df["fecha"]==today)].count() # total de ordenes  en el dia
t_ordenes_oeste = df[(df["fecha"]==today) & (df["region_cliente"]!='SUR')].count() # total oeste 
t_ordenes_oeste_equipos = df[(df["fecha"]==today) & (df["region_cliente"]!='SUR') & (df["mac_instalado"]!='Sin Instalado')].count() # total de oeste con equipos 
t_ordenes_sur = df[(df["fecha"]==today) & (df["region_cliente"]=='SUR')].count() # total sur 
t_ordenes_sur_equipos = df[(df["fecha"]==today) & (df["region_cliente"]=='SUR') & (df["mac_instalado"]!='Sin Instalado')].count() # total de sur con equipos 
bot.send_message(chat_id='-', text="total de ordenes en el dia: {}".format(total[0]))
bot.send_message(chat_id='-', text="total ordenes en oeste: {}".format(t_ordenes_oeste[0]))
bot.send_message(chat_id='-', text="total equipos intalados en oeste: {}".format(t_ordenes_oeste_equipos[0]))
bot.send_message(chat_id='-', text="total equipos intalados en sur: {}".format(t_ordenes_sur_equipos[0]))



##############
#cargar csv hechos.csv
# Crea el cliente de Grive utilizando las credenciales de autenticación
drive_service = build('drive', 'v3', credentials=creds)
# ID del archivo que se actualizara
file_id = ''
# Nombre y ruta del archivo que se actualizara
file_name = 'csv/hechos.csv'
# Crea un objeto de archivo con el nombre y la ruta del archivo
file_metadata = {'name': os.path.basename(file_name)}
media = MediaIoBaseUpload(io.BytesIO(open(file_name, 'rb').read()), mimetype='application/octet-stream', chunksize=1024*1024, resumable=True)
# Actualiza el archivo en GDrive
updated_file = drive_service.files().update(fileId=file_id, media_body=media).execute()
# Verificar si se actualizo
if updated_file.get('name'):
    print(f'El archivo {updated_file.get("name")} se ha actualizado correctamente')
    bot.send_message(chat_id='-', text="Actualizado en drive ☁️")
else:
    print('No se ha podido actualizar el archivo')
    bot.send_message(chat_id='', text="ERROR ❗")


print("break")
print("[                    ] 0%", end="")
percent = 0
for i in range(20):
    print("\r[", end="")
    for j in range(1, i + 1):
        print("█", end="")
    for j in range(i + 1, 20):
        print(" ", end="")
    percent = (i + 1) * 5
    print("] {}%".format(percent), end="")
    time.sleep(0.5)

print("\nabriendo la planilla")
import planilla_automatica
planilla_automatica()
print(logoscript)
