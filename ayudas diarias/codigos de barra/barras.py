from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter
import os

# Leer los códigos de barras del archivo de texto
with open('codigos.txt', 'r') as f:
    codigos = [line.strip() for line in f]

# Ajustar el tamaño de la página y los códigos de barras
PAGE_WIDTH, PAGE_HEIGHT = A4
PAGE_WIDTH = 4* PAGE_WIDTH
BARCODE_WIDTH = 2.5 * PAGE_WIDTH / len(codigos)
BARCODE_HEIGHT = 50
X_MARGIN = 2 # Nuevo valor de margen horizontal
NUM_ROWS = (len(codigos) + 3) // 4 # Calcular el número de filas necesario

# Crear un objeto canvas para generar el PDF
pdf = canvas.Canvas("codigos_de_barras.pdf", pagesize=A4)

# Coordenadas de inicio para los códigos de barras y los códigos correspondientes
x, y = 20, PAGE_HEIGHT - BARCODE_HEIGHT - 40
code_x, code_y = 20, y - 20

# Dividir la página en filas según el número de códigos de barras
filas = [codigos[i:i+4] for i in range(0, len(codigos), 4)]

# Agregar los códigos de barras y sus códigos correspondientes en cada fila
# Inicializar el contador
num_codigos_pagina_actual = 0

# Agregar los códigos de barras y sus códigos correspondientes en cada fila
for fila in filas:
    for codigo in fila:
        # Generar una nueva página si se han agregado 32 códigos
        if num_codigos_pagina_actual == 32:
            pdf.showPage()
            num_codigos_pagina_actual = 0
            x, y = 20, PAGE_HEIGHT - BARCODE_HEIGHT - 40
            code_x, code_y = 20, y - 20
        barcode = Code128(codigo, writer=ImageWriter())
        archivo_imagen = barcode.save(codigo)
        pdf.drawImage(archivo_imagen, x, y, width=BARCODE_WIDTH, height=BARCODE_HEIGHT)
        

	# pdf.drawString(code_x, code_y, codigo) # Comentar o eliminar esta línea
        x += BARCODE_WIDTH + 20
        code_x += BARCODE_WIDTH + 40
        num_codigos_pagina_actual += 1
    # Reiniciar las coordenadas de inicio para la siguiente fila
    x, y = 20, y - BARCODE_HEIGHT - 40
    code_x, code_y = 20, y - 40

# Generar una nueva página si hay más de 32 códigos en la última página
if num_codigos_pagina_actual > 0:
    pdf.showPage()

# Eliminar los archivos de imagen generados
for codigo in codigos:
    os.remove(codigo + ".png")

# Guardar y cerrar el archivo PDF
pdf.save()

