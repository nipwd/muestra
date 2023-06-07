from cryptography.fernet import Fernet

def encrypt_file(filename, key):
    # Leer el archivo
    with open(filename, 'rb') as file:
        file_data = file.read()

    # Generar el objeto Fernet con la clave
    f = Fernet(key)

    # Encriptar los datos del archivo
    encrypted_data = f.encrypt(file_data)

    # Escribir los datos encriptados en un nuevo archivo
    encrypted_filename = f"{filename}.encrypted"
    with open(encrypted_filename, 'wb') as file:
        file.write(encrypted_data)

    print(f"Archivo encriptado: {encrypted_filename}")

# Ruta del archivo a encriptar
archivo_a_encriptar = "ETA_V3.py"

# Clave que ya tienes (debes asegurarte de que sea una clave válida generada por Fernet)
clave = b''

# Encriptar el archivo
encrypt_file(archivo_a_encriptar, clave)
