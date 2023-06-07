import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import subprocess
import os

# Función para convertir el archivo .cap a .hccapx
def convert_file():
    # Obtener la ruta del archivo .cap seleccionado
    cap_file = filedialog.askopenfilename(filetypes=[("Captura de paquetes", "*.cap")])

    # Crear el comando para convertir el archivo
    command = f"aircrack-ng {cap_file} -J CAP/output"

    # Ejecutar el comando
    subprocess.run(command, shell=True)

    # Obtener la ruta del archivo .hccapx generado
    hccapx_file = os.path.splitext(cap_file)[0] + ".hccapx"

    # Mostrar un mensaje al usuario
    message_label.config(text=f"Archivo convertido a {hccapx_file}")

# Crear la ventana
root = tk.Tk()
root.geometry("600x500+300+150")
root.resizable(width=True, height=True)
# Cargar la imagen GIF
imagen_gif = Image.open("image/hash.png")
imagen_gif= imagen_gif.resize((300,300))
# Convertir la imagen a un objeto PhotoImage de Tkinter
imagen_tk = ImageTk.PhotoImage(imagen_gif)

# Crear un botón para seleccionar el archivo .cap
select_button = tk.Button(root, text="Seleccionar archivo .cap", command=convert_file)
select_button.pack()

# Crear una etiqueta para mostrar el mensaje al usuario
message_label = tk.Label(root, text="")
message_label.pack()
etiqueta_imagen = tk.Label(root, image=imagen_tk)
etiqueta_imagen.pack()

# Iniciar la aplicación
root.mainloop()
