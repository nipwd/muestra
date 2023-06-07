import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from cryptography.fernet import Fernet
import json

def save_db():
    key =os.environ.get('NETLIFE_GDRIVE_KEY')
    # Crea un objeto Fernet con la llave
    cipher_suite = Fernet(key.encode())

    # Lee el archivo encriptado JSON
    with open('/home/dev/MUESTRA/netlife/keys_ECRIPTED.json', 'rb') as encrypted_json_file:
        encrypted_json = encrypted_json_file.read()

    # Descifra el contenido del archivo JSON
    decrypted_json = cipher_suite.decrypt(encrypted_json)
    json_str = decrypted_json.decode()

    # Convierte la cadena en formato JSON a un objeto Python
    json_data = json.loads(json_str)
    creds = service_account.Credentials.from_service_account_file(json_data)
    # Crea el cliente de GDrive
    drive_service = build('drive', 'v3', credentials=creds)
    # ID del archivo que se actualizara
    file_id = ''
    # Nombre y ruta del archivo que se actualizara
    file_name = '/home/dev/scrips/netlife/db.sqlite3'
    # Crea un objeto de archivo con el nombre y la ruta del archivo
    file_metadata = {'name': os.path.basename(file_name)}
    media = MediaIoBaseUpload(io.BytesIO(open(file_name, 'rb').read()), mimetype='application/octet-stream', chunksize=1024*1024, resumable=True)
    updated_file = drive_service.files().update(fileId=file_id, media_body=media).execute()
    if updated_file.get('name'):
        print(f'El archivo {updated_file.get("name")} se ha actualizado correctamente')
    else:
        print('No se ha podido actualizar el archivo')

save_db()
