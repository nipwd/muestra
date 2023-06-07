import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import threading
from time import sleep
from cryptography.fernet import Fernet
import json

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

def save_db():
    #subir db
    # Crea el cliente de Google Drive utilizando las credenciales de autenticación
    drive_service = build('drive', 'v3', credentials=creds)
    # ID del archivo que se actualizará
    file_id = ''
    import io
    # Nombre y ruta del archivo que se actualizará
    file_name = 'db.sqlite3'
    # Crea un objeto de archivo con el nombre y la ruta del archivo
    file_metadata = {'name': os.path.basename(file_name)}
    media = MediaIoBaseUpload(io.BytesIO(open(file_name, 'rb').read()), mimetype='application/octet-stream', chunksize=1024*1024, resumable=True)
    # Actualiza el archivo en Google Drive
    updated_file = drive_service.files().update(fileId=file_id, media_body=media).execute()
    # Verificar si la actualización fue exitosa
    if updated_file.get('name'):
        print(f'\nEl archivo {updated_file.get("name")} se ha actualizado correctamente')
    else:
        print('No se ha podido actualizar el archivo')


def db_sync_load_function():
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
