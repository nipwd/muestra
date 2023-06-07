import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
ventana = tk.Tk()
ventana.geometry("600x500+300+150")
ventana.resizable(width=True, height=True)
# Cargar la imagen GIF
imagen_gif = Image.open("image/hash.png")
imagen_gif= imagen_gif.resize((300,300))
# Convertir la imagen a un objeto PhotoImage de Tkinter
imagen_tk = ImageTk.PhotoImage(imagen_gif)

def abrir_archivo():
    ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos hccap", "*.hccap"), ("Todos los archivos", "*.*")])
    if ruta_archivo:
        with open(ruta_archivo, "rb") as archivo:
            ssid = archivo.read(32).decode('ascii').rstrip('\x00')
            archivo.read(4)  # Leer los primeros 4 bytes y descartarlos
            bssid = ':'.join('{:02x}'.format(b) for b in archivo.read(6))
            station= ':'.join('{:02x}'.format(b) for b in archivo.read(12))
            hash_password = archivo.read(16).hex()
   
            etiqueta_ssid.config(text=f"SSID: {ssid}")
            etiqueta_bssid.config(text=f"BSSID: {bssid}")
            etiqueta_hash.config(text=f"Hash del password: {hash_password}")
            boton_copiar_ssid.config(command=lambda: ventana.clipboard_append(ssid))
            boton_copiar_bssid.config(command=lambda: ventana.clipboard_append(bssid))
            boton_copiar_hash.config(command=lambda: ventana.clipboard_append(hash_password))

boton_abrir = tk.Button(ventana, text="Abrir archivo", command=abrir_archivo)
boton_abrir.pack()

etiqueta_informacion = tk.Label(ventana, text="Aquí se mostrará la información del archivo hccap")
etiqueta_informacion.pack()

etiqueta_ssid = tk.Label(ventana, text="SSID: ")
etiqueta_ssid.pack()

boton_copiar_ssid = tk.Button(ventana, text="Copiar", command=lambda: None)
boton_copiar_ssid.pack()

etiqueta_bssid = tk.Label(ventana, text="BSSID: ")
etiqueta_bssid.pack()

boton_copiar_bssid = tk.Button(ventana, text="Copiar", command=lambda: None)
boton_copiar_bssid.pack()

etiqueta_hash = tk.Label(ventana, text="Hash del password: ")
etiqueta_hash.pack()

boton_copiar_hash = tk.Button(ventana, text="Copiar", command=lambda: None)
boton_copiar_hash.pack()


# Agregar la imagen a una etiqueta
etiqueta_imagen = tk.Label(ventana, image=imagen_tk)
etiqueta_imagen.pack()

ventana.mainloop()
