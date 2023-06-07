import os
import io
import csv
from datetime import datetime, timedelta
from time import sleep
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import Context, Template
from django.db.models import Sum
from decimal import Decimal
from pañol_app.forms import *
from pañol_app.models import *
import pandas as pd
import sqlite3
from sqlite3 import Error
from django.utils import timezone
import io
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build
import threading
from .models import Equipo
from .forms import IngresoDeEquipos
import plotly.graph_objects as go

os.system('cls' if os.name == 'nt' else 'clear')
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


import datetime
import json
from cryptography.fernet import Fernet

today = datetime.date.today()
ayer = today - datetime.timedelta(days=1)
ayer = ayer.strftime('%d-%m-%Y')
conn = sqlite3.connect('db.sqlite3'.format('pañol_app_equiposretirados'))
today2 = (today.strftime('%d-%m-%Y'))

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


def save_db():
    #subir db
    # Crea el cliente de GDrive usando las credenciales de autenticación
    drive_service = build('drive', 'v3', credentials=creds)
    # ID del archivo que se actualizará
    file_id = ''
    # Nombre y ruta del archivo que se actualizará
    file_name = 'db.sqlite3'
    # Crea un objeto de archivo con el nombre y la ruta del archivo
    file_metadata = {'name': os.path.basename(file_name)}
    media = MediaIoBaseUpload(io.BytesIO(open(file_name, 'rb').read()), mimetype='application/octet-stream', chunksize=1024*1024, resumable=True)
    # Actualiza el archivo en GDrive
    updated_file = drive_service.files().update(fileId=file_id, media_body=media).execute()
    # Verificar si se actualizo
    if updated_file.get('name'):
        print(f'\nEl archivo {updated_file.get("name")} se ha actualizado correctamente')
    else:
        print('No se ha podido actualizar el archivo')

df = pd.read_csv('csv/hechos.csv')
nombres_tecnicos = Tecnico.objects.values_list('name', flat=True)
df2 = df[(df['fecha'] == ayer) & (df['tecnico'].isin(nombres_tecnicos)) & (df['equipo_desinstalado'] != "Sin Retiro")]

datos = df2.to_dict(orient='records')

for registro in datos:
    filtros = {
        'fecha': registro['fecha'],
        'tecnico': registro['tecnico'],
        'equipo_instalado': registro['equipo_instalado'],
        'mac_instalado': registro['mac_instalado'],
        'equipo_desinstalado': registro['equipo_desinstalado'],
        'mac_desinstalado': registro['mac_desinstalado'],
        'numero_vt': registro['numero_vt'],
        'numero_cliente': registro['numero_cliente'],
        'nombre_cliente': registro['nombre_cliente'],
        'dni_cliente': registro['dni_cliente'],
        'direccion_cliente': registro['direccion_cliente'],
        'localidad_cliente': registro['localidad_cliente'],
        'partido_cliente': registro['partido_cliente'],
        'telefono_cliente': registro['telefono_cliente'],
        'region_cliente': registro['region_cliente']
    }

    if not EquiposRetirados.objects.filter(**filtros).exists():
        nuevo_objeto = EquiposRetirados.objects.create(**registro)

equipos_unicos = EquiposRetirados.objects.values('fecha', 'tecnico', 'equipo_instalado', 'mac_instalado', 'equipo_desinstalado', 'mac_desinstalado', 'numero_vt', 'numero_cliente', 'nombre_cliente', 'dni_cliente', 'direccion_cliente', 'localidad_cliente', 'partido_cliente', 'telefono_cliente', 'region_cliente').distinct()

os.system('cls' if os.name == 'nt' else 'clear')

def db_sync_load_function():
    print(logoscript)

    print("sincronizando base de datos")
    print("[                    ] 0%", end="")

    percent = 0
    save_executed = False

    for i in range(20):
        print("\r[", end="")
        for j in range(1, i + 1):
            print("█", end="")
        for j in range(i + 1, 20):
            print(" ", end="")
        percent = (i + 1) * 5
        print("] {}%".format(percent), end="")
        sleep(1.2)

        if not save_executed and i == 0:
            save_thread = threading.Thread(target=save_db)
            save_thread.start()
            save_executed = True

db_sync_load_function()
os.system('cls' if os.name == 'nt' else 'clear')
print("Ready -----")
print(logoscript)

def close_other_sessions(request, username):
    user = User.objects.get(username=username)

    # Obtener todas las sesiones activas del usuario
    sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Cerrar sesiones activas menos la sesión actual
    for session in sessions:
        session_data = session.get_decoded()
        if session_data.get('_auth_user_id') == str(user.id) and session.session_key != request.session.session_key:
            session.delete()

@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists())
def index(request):
    listatecnicos = Tecnico.objects.all().order_by("name")
    for tecnico_nombre in listatecnicos:
        name = tecnico_nombre
        return render(request,'templates/index.html')

@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists() or user.groups.filter(name='oficina').exists())
def tecnicos(request):
    listatecnicos = Tecnico.objects.all().order_by("name")
    # Obtener todos los registros del modelo EquiposRetirados
    registros = EquiposRetirados.objects.all().filter(fecha=ayer)
    nombres_barras = ['Deco_Cisco','Deco_Sagemcom','4K_362','4K_387','Alexa','2_0','3_0','3_1','Mesh']
    valores_barras = [
        registros.filter(equipo_instalado__icontains='Decodificador digital Cisco® PDS-2140').count(),
        registros.filter(equipo_instalado__icontains='Decodificador HD Sagemcom DCIW303 HD').count(),
        registros.filter(equipo_instalado__icontains='Decodificador Digital 4K BASICO DCIW362 - SagemCom').count(),
        registros.filter(equipo_instalado='Decodificador 4K Sagemcom DCIW387 UHD').count(),
        registros.filter(equipo_instalado='Video Sound Box Sagemcom 3930').count(),
        registros.filter(equipo_instalado__icontains='Modem Scientific').count()+registros.filter(equipo_instalado__icontains='Modem Technicolor').count(),
        registros.filter(equipo_instalado='Modem_3_0').count(),
        registros.filter(equipo_instalado__icontains='Docsis 3.1').count(),
        registros.filter(equipo_instalado__icontains='Extensor Wifi AIRTIES AIR4960X').count()]
    color_barras = '#00AEEF'
    layout = go.Layout(title=f'Equipos instalados', font={'color': 'black', 'size': 18}, paper_bgcolor='#fff', plot_bgcolor='#fff',width=1000,autosize=True,xaxis=dict(rangeslider=dict(visible=False)))
    textos_barras = [str(valor) for valor in valores_barras]
    fig = go.Figure(data=[go.Bar(x=nombres_barras, y=valores_barras, marker=dict(color=color_barras), text=textos_barras, textposition='auto')], layout=layout)
    fig.update_layout(
        title='Conteo de Equipos Instalados Ayer',
        yaxis_title='Cantidad',)
    config = {'displayModeBar': False, 'scrollZoom': False, 'modeBarButtons': [['drawline', 'drawopenpath','drawcircle', 'drawrect', 'eraseshape']]}
    html_fig = fig.to_html(full_html=False,config=config)
    context = {"name" : listatecnicos,"html_fig":html_fig}
    return render(request,'templates/tecnicos.html',context)


@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists())
def stock(request):
    listatecnicos = Tecnico.objects.all().order_by("name")
    context = {"name" : listatecnicos}
    return render(request,'templates/stock.html',context)

@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists() or user.groups.filter(name='oficina').exists())
def verTecnico(request,tecnico_name):
    from datetime import datetime
    listatecnicos = Tecnico.objects.all().order_by('name')
    tecnico= Tecnico.objects.get(name=tecnico_name)
    equipos= EquiposRetirados.objects.filter(tecnico=tecnico_name).filter(fecha=ayer).exclude(mac_instalado="Sin Instalado")
    listanueva =[]
    for x in listatecnicos:
        listanueva.append(x.name)
    posicion = listanueva.index(tecnico_name)
    siguiente = posicion + 1
    if siguiente ==  len(listanueva):
        siguiente = listanueva[0]
    else:
        siguiente = listanueva[siguiente]
    anterior = posicion -1
    anterior = listanueva[anterior]
    if request.GET.get('valor_data'):
        valor_data= request.GET.get('valor_data')
        valor_data = datetime.strptime(valor_data, '%Y-%m-%d')
        valor_data = (valor_data.strftime('%d-%m-%Y'))
        listatecnicos = Tecnico.objects.all()
        tecnico= Tecnico.objects.get(name=tecnico_name)
        equipos= EquiposRetirados.objects.filter(tecnico=tecnico_name).filter(fecha=valor_data).order_by('fecha')
        
        listanueva =[]
        for x in listatecnicos:
           listanueva.append(x.name)
        posicion = listanueva.index(tecnico_name)
        siguiente = posicion + 1
        if siguiente ==  len(listanueva):
            siguiente = listanueva[0]
        else:
            siguiente = listanueva[siguiente]
            anterior = posicion -1
            anterior = listanueva[anterior]
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        return render(request,'templates/test.html', {'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos})
    if request.GET.get('search'): # 
            search =  request.GET.get('search')
            try:
                if EquiposRetirados.objects.filter(tecnico=search).order_by("fecha").exists():
                    search =EquiposRetirados.objects.filter(tecnico=search)
                if EquiposRetirados.objects.filter(mac_instalado=search).order_by("fecha").exists():
                    search =EquiposRetirados.objects.filter(mac_instalado=search)
                if EquiposRetirados.objects.filter(mac_desinstalado=search).order_by("fecha").exists():
                    search =EquiposRetirados.objects.filter(mac_desinstalado=search)
                if EquiposRetirados.objects.filter(numero_vt=search).order_by("fecha").exists():
                    search =EquiposRetirados.objects.filter(numero_vt=search)
                if EquiposRetirados.objects.filter(numero_cliente=search).order_by("fecha").exists():
                    search =EquiposRetirados.objects.filter(numero_cliente=search)
                else:
                    pass
                
                return render(request,'templates/test.html', {"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,'search':search})
            except:
                return render(request,'templates/test.html', {"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,'search':search})

                
    else:
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        return render(request,'templates/test.html', {'formulario':form,'form2':form2,'form3': form3,'form2':form2,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,})

@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists())
def verStock(request,tecnico_name):
    listatecnicos = Tecnico.objects.all().order_by('name')
    tecnico= Tecnico.objects.get(name=tecnico_name)
    descu= Descuento.objects.filter(tecnico=tecnico_name)
    cable_bobina = int(Tecnico.objects.get(name=tecnico_name).metros)
    equipos= EquiposRetirados.objects.filter(tecnico=tecnico_name).filter(fecha=ayer).exclude(mac_instalado="Sin Instalado").order_by("fecha")
    equipos_dcisco= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador Cisco").order_by("fecha")
    equipos_dsagem= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Sagemcom_DCIW303").order_by("fecha")
    equipos_4k362= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_BASICO_DCIW362").order_by("fecha")
    equipos_4k387= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_387").order_by("fecha")
    equipos_alexa= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Video_Sound_Box_Sagemcom_393").order_by("fecha")
    equipos_2_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_2_0").order_by("fecha")
    equipos_3_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_0").order_by("fecha")
    equipos_3_1= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_1").order_by("fecha")
    equipos_mesh= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Extensor Wifi AIRTIES AIR4960X").order_by("fecha")
    listanueva =[]
    for x in listatecnicos:
        listanueva.append(x.name)
    posicion = listanueva.index(tecnico_name)
    siguiente = posicion + 1
    if siguiente ==  len(listanueva):
        siguiente = listanueva[0]
    else:
        siguiente = listanueva[siguiente]
    anterior = posicion -1
    anterior = listanueva[anterior]
    if request.GET.get('valor_data'):
        valor_data= request.GET.get('valor_data')
        valor_data = datetime.strptime(valor_data, '%Y-%m-%d')
        valor_data = (valor_data.strftime('%d-%m-%Y'))
        listatecnicos = Tecnico.objects.all()
        tecnico= Tecnico.objects.get(name=tecnico_name)
        equipos= EquiposRetirados.objects.filter(tecnico=tecnico_name).filter(fecha=valor_data)
        equipos_dcisco= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador Cisco")
        equipos_dsagem= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Sagemcom_DCIW303")
        equipos_4k362= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_BASICO_DCIW362")
        equipos_4k387= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_387")
        equipos_alexa= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Video_Sound_Box_Sagemcom_393")
        equipos_2_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_2_0")
        equipos_3_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_0")
        equipos_3_1= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_1")
        equipos_mesh= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Extensor Wifi AIRTIES AIR4960X")
        listanueva =[]
        for x in listatecnicos:
           listanueva.append(x.name)
        posicion = listanueva.index(tecnico_name)
        siguiente = posicion + 1
        if siguiente ==  len(listanueva):
            siguiente = listanueva[0]
        else:
            siguiente = listanueva[siguiente]
            anterior = posicion -1
            anterior = listanueva[anterior]
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        return render(request,'templates/verStock.html', {'form2':form2,'form3':form3,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"equipos_mesh":equipos_mesh,"cable_bobina":cable_bobina})
    
    if (request.method == "POST"):
        form= CargarEquiposAStock(request.POST, request.FILES)
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        if form.is_valid():
            form.cleaned_data
            text= request.POST.get('seriado')
            lista = []
            try:
                if text:
                    for line in text.split('\r\n'):
                       Equipo.objects.filter(seriado=line).distinct().update(estado=tecnico_name,fecha=today2)
                    form= CargarEquiposAStock()
                    form2= Bobina_consumoform()
                    form3= Bobina_hisotiralform()
                    return render(request,'templates/verStock.html', {'descu':descu,'form2':form2,'form3':form3,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina,"equipos_mesh":equipos_mesh})
            except:
                form= CargarEquiposAStock(request.POST, request.FILES)
                form2= Bobina_consumoform()
                form3= Bobina_hisotiralform()
                return render(request,'templates/verStock.html', {'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"equipos_mesh":equipos_mesh,'cable_bobina':cable_bobina})
    
    if (request.method == "POST"):
        form2= Bobina_consumoform(request.POST, request.FILES)
        form= CargarEquiposAStock()
        form3= Bobina_hisotiralform()
        if form2.is_valid():
            form2.cleaned_data
            text= request.POST.get('consumo')
            consumo = Bobina_consumo(consumo_bobina=text,tecnico=tecnico_name)
            consumo.save()
            agregar = (Tecnico.objects.get(name=tecnico_name)).metros - int(text)
            Tecnico.objects.filter(name=tecnico_name).update(metros= agregar)
            form= CargarEquiposAStock()
            form2= Bobina_consumoform()
            form3= Bobina_hisotiralform()
            cable_bobina = int(Tecnico.objects.get(name=tecnico_name).metros)
            return render(request,'templates/verStock.html', {'descu':descu,'formulario':form,'form3':form3,'form2': form2,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina,"equipos_mesh":equipos_mesh})
        
    if (request.method == "POST"):
        form3= Bobina_hisotiralform(request.POST, request.FILES)
        form3= Bobina_hisotiralform(request.POST, request.FILES)
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        if form3.is_valid():
            form3.cleaned_data
            text= request.POST.get('seriado_bobina')
            consumo = Bobina_hisotiral(seriado_bobina=text,tecnico=tecnico_name)
            consumo.save()
            agregar = (Tecnico.objects.get(name=tecnico_name)).metros + 305
            Tecnico.objects.filter(name=tecnico_name).update(metros= agregar)
            form= CargarEquiposAStock()
            form2= Bobina_consumoform()
            form3= Bobina_hisotiralform()
            cable_bobina = int(Tecnico.objects.get(name=tecnico_name).metros)
            return render(request,'templates/verStock.html', {'descu':descu,'form2':form2,'formulario':form,'form3': form3,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina,"equipos_mesh":equipos_mesh})
    else:
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        return render(request,'templates/verStock.html', {'form2':form2,'form3':form3,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"equipos_mesh":equipos_mesh,'cable_bobina':cable_bobina})

@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists())
def editar_equipo(request):
    seriado = request.GET.get('seriado')
    equipo = Equipo.objects.get(seriado=seriado)
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo.estado = form.cleaned_data['estado']
            equipo.nombre_equipo = form.cleaned_data['nombre_equipo']
            equipo.seriado = form.cleaned_data['seriado']
            equipo.fecha = form.cleaned_data['fecha']
            equipo.save()
            tecnico_name=equipo.estado
            verStock(request,tecnico_name)
    else:
        form = EquipoForm(initial={'estado': equipo.estado, 'nombre_equipo': equipo.nombre_equipo, 'seriado': equipo.seriado})
    return render(request, 'templates/editar_equipo.html', {'seriado': seriado, 'form': form})


@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists())
def Ingresos(request):
    if request.method == "POST":
        form = IngresoDeEquipos(request.POST)
        if form.is_valid():
            text = request.POST.get('seriado')
            if text:
                nombre_equipo = request.POST.get('nombre_equipo')
                estado = "pañol"
                seriales_existentes = Equipo.objects.filter(seriado__in=text.split('\r\n'))
                seriales_existentes.delete()
                for line in text.split('\r\n'):
                    cargar_equipos = Equipo(seriado=line, nombre_equipo=nombre_equipo, estado=estado, fecha=today2)
                    cargar_equipos.save()
                form = IngresoDeEquipos()
                return render(request, 'templates/Ingresos.html', {'formulario': form})
            else:
                form = IngresoDeEquipos()
                return render(request, 'templates/Ingresos.html', {'formulario': form})
    else:
        form = IngresoDeEquipos()
        return render(request, 'templates/Ingresos.html', {'formulario': form})
    return render(request, 'templates/Ingresos.html')


def login_request(request):
    if request.method == 'POST':
        form= AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password') 
            close_other_sessions(request, usuario)
            user = authenticate(username=usuario, password=contra)
            if user is not None:
                login(request,user)
                return render(request,'templates/index.html',{"form":form, "mensaje": f"Bienvenido {usuario}"})
            else:
                return render(request,'templates/login.html',{"form":form, "mensaje": f"Usuario o clave incorrectos"})
        else:
            return render(request,'templates/login.html',{"form":form, "mensaje": f"Formulario invalido"})
    else:
        form = AuthenticationForm()
        return render(request,'templates/login.html', {'form':form})


@login_required
def mistock(request):
    if request.method == 'POST':
        selected_button = request.POST.get('buttonContent')
        print(selected_button + "hey")
        first_name = request.user.first_name
        last_name = request.user.last_name
        nommbre = str(last_name +' '+first_name)
        equipos_dcisco= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador Cisco")
        equipos_dsagem= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador_Sagemcom_DCIW303")
        equipos_4k362= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador_Digital_4K_BASICO_DCIW362")
        equipos_4k387= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador_Digital_4K_387")
        equipos_alexa= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Video_Sound_Box_Sagemcom_393")
        equipos_2_0= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Modem_2_0")
        equipos_3_0= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Modem_3_0")
        equipos_3_1= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Modem_3_1")
        equipos_mesh= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Extensor Wifi AIRTIES AIR4960X")
        return render(request,'templates/mistock2.html', {"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"equipos_mesh":equipos_mesh})
    else:
        first_name = request.user.first_name
        last_name = request.user.last_name
        nommbre = str(last_name +' '+first_name)
        equipos_dcisco= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador Cisco")
        equipos_dsagem= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador_Sagemcom_DCIW303")
        equipos_4k362= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador_Digital_4K_BASICO_DCIW362")
        equipos_4k387= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Decodificador_Digital_4K_387")
        equipos_alexa= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Video_Sound_Box_Sagemcom_393")
        equipos_2_0= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Modem_2_0")
        equipos_3_0= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Modem_3_0")
        equipos_3_1= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Modem_3_1")
        equipos_mesh= Equipo.objects.filter(estado=nommbre).filter(nombre_equipo = "Extensor Wifi AIRTIES AIR4960X")
        return render(request,'templates/mistock2.html', {"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"equipos_mesh":equipos_mesh})

def handler404(request, exception):
    return render(request, 'templates/404.html', status=404)



@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists())
def devoluciones(request):
    equipos_devolucion =  Equipo.objects.filter(estado='Invenario_de_devolucion').order_by('nombre_equipo')
    if request.method == "POST":
        form = IngresoDeEquiposNoOperativos(request.POST)
        if form.is_valid():
            form.cleaned_data
            text = request.POST.get('seriado')
            if text:
                for line in text.split('\r\n'):
                    if EquiposRetirados.objects.filter(mac_desinstalado=line).exists():
                        nombre_equipo = EquiposRetirados.objects.get(mac_desinstalado=line).equipo_desinstalado
                        estado = 'Invenario_de_devolucion'
                        cargar_equipos = Equipo(seriado=line, nombre_equipo=nombre_equipo, estado=estado)
                        if EquiposRetirados.objects.filter(mac_desinstalado=line).exists():
                            nombre_equipo = EquiposRetirados.objects.get(mac_desinstalado=line).equipo_desinstalado
                            estado = 'Invenario_de_devolucion'
                            try:
                                Equipo.objects.get(seriado=line, estado=estado)
                            except ObjectDoesNotExist:
                                cargar_equipos = Equipo(seriado=line, nombre_equipo=nombre_equipo, estado=estado)
                                cargar_equipos.save()
                                EquiposRetirados.objects.filter(mac_desinstalado=line).delete()
                                Equipo.objects.filter(seriado='').delete()
                                form = IngresoDeEquiposNoOperativos()
                                Equipo.objects.filter(seriado=line).distinct().update(estado=estado,fecha=today2)
                    if Equipo.objects.filter(seriado=line).exists():
                        estado = 'Invenario_de_devolucion'
                        Equipo.objects.filter(seriado=line).distinct().update(estado=estado,fecha=today2)
                        EquiposRetirados.objects.filter(mac_desinstalado=line).delete()
                        Equipo.objects.filter(seriado='').delete()
                        form = IngresoDeEquiposNoOperativos()
                    if Descuento.objects.filter(mac=line).exists():
                        estado = 'Invenario_de_devolucion'
                        Equipo.objects.filter(seriado=line).distinct().update(estado=estado,fecha=today2)
                        Descuento.objects.filter(mac=line).delete()
                        Equipo.objects.filter(seriado='').delete()
                        form = IngresoDeEquiposNoOperativos()
                return render(request, 'templates/devoluciones.html', {'formulario': form, 'equipos_devolucion': equipos_devolucion})
            if not text:
                form = IngresoDeEquiposNoOperativos()
                return render(request, 'templates/devoluciones.html', {'formulario': form, 'equipos_devolucion': equipos_devolucion})
    else:
        form = IngresoDeEquiposNoOperativos()
        return render(request, 'templates/devoluciones.html', {'formulario': form, 'equipos_devolucion': equipos_devolucion})

    form = IngresoDeEquiposNoOperativos()
    return render(request, 'templates/devoluciones.html',{ 'formulario': form, 'equipos_devolucion': equipos_devolucion})





@login_required
@user_passes_test(lambda user: user.groups.filter(name='pañol').exists())
def descuentos(request):
    tecnicos= Tecnico.objects.all().order_by('name')
    for tecnico in tecnicos:
        retiros = EquiposRetirados.objects.filter(fecha=ayer).filter(tecnico=tecnico.name)
        for retiro in retiros:
            if Equipo.objects.filter(seriado=retiro.mac_desinstalado).filter(estado = "Invenario_de_devolucion"):
                continue
            else:
                if retiro.mac_desinstalado=="Sin Retiro":
                    pass
                if Descuento.objects.filter(mac=retiro.mac_desinstalado).exists():
                    pass

                if not Descuento.objects.filter(mac=retiro.mac_desinstalado).exists() and retiro.mac_desinstalado!="Sin Retiro":
                    cargar_equipos = Descuento(tecnico=retiro.tecnico,equipo=retiro.equipo_desinstalado,mac=retiro.mac_desinstalado,vt=retiro.numero_vt, cliente=retiro.numero_cliente,estado='descuento')
                    cargar_equipos.save()
        descu= Descuento.objects.all()
    return render(request,'templates/descuento.html',{'descu':descu})
    
