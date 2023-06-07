import tkinter as tk
from cryptography.fernet import Fernet

def decrypt_and_execute(code, key):
    # Generar el objeto Fernet con la clave
    f = Fernet(key)

    # Desencriptar el código
    decrypted_code = f.decrypt(code)

    # Ejecutar el código desencriptado
    exec(decrypted_code)

def show_image():
    # Cargar la imagen
    

    # Crear un widget de etiqueta para mostrar la imagen
    image_label = tk.Label(window)
    image_label.pack()

    # Programar la eliminación de la imagen después de 2 segundos
    window.after(2000, image_label.destroy)

def decrypt_with_key():
    # Obtener la clave desde el campo de entrada
    clave = key_entry.get()
    window.destroy()

    # Leer el archivo encriptado
    with open("ETA_V3.py.encrypted", 'rb') as file:
        encrypted_data = file.read()

    # Desencriptar y ejecutar el código, pasando la clave como parámetro
    decrypt_and_execute(encrypted_data, clave)

    # Mostrar la imagen durante 2 segundos antes de cerrar la ventana
    show_image()
    window.after(2000, window.destroy)

# Crear la ventana de tkinter
window = tk.Tk()
# Obtener las dimensiones de la pantalla
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calcular la posición para centrar la ventana
window_width = 400
window_height = 250
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Establecer la geometría de la ventana
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Crear un campo de entrada para la clave
key_label = tk.Label(window, text="Clave:")
key_label.pack()
key_entry = tk.Entry(window, show="*")
key_entry.pack()

# Crear un botón para iniciar el proceso de desencriptación
decrypt_button = tk.Button(window, text="Desencriptar y ejecutar", command=decrypt_with_key)
decrypt_button.pack()

# Iniciar el bucle principal de tkinter
window.mainloop()

# F1cDAOfI-zqfATYxldJMHxMnEV6yKjREJHabR8F9_EY=