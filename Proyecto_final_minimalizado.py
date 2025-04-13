import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import imutils
import cv2
import numpy as np

# Crea ventana
ventana = tk.Tk()
ventana.geometry("1320x800")
ventana.resizable(0,0)
ventana.title("Proyecto Webcam minimalizado")

# mostrar coordenas 

def mostrar_coordenadas(event):
    coordenadas['text']=f'x = {event.x}    y = {event.y}'


#Variables globales

global Captura, CapturaG, ImgRec, UImagen, label_manchas, label_porcentaje, label_contornos, recortada, valor


#Inicia cámara web
def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()
    
def iniciar():
    global capture
    if capture is not None:

        ret, frame = capture.read()
        if ret == True:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ImagenCamara)
            img = ImageTk.PhotoImage(image= im)
            LImagen.configure(image= img)
            LImagen.image = img
            LImagen.after(10,iniciar)
        else:
            LImagen.image = ""
            capture.release()

def Capturar():
    global ImgRec, ImgCompleta
    camara = capture
    return_value, image = camara.read()

    if return_value:
        # Redimensionar imagen como antes
        frame = imutils.resize(image, width=301)
        frame = imutils.resize(frame, height=221)

        # Guardar imagen completa original en gris
        ImgCompleta = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Coordenadas fijas del recorte
        x1_fixed, y1_fixed = 110, 80
        x2_fixed, y2_fixed = 190, 145

        # Recortar la imagen
        ImgRec = ImgCompleta[y1_fixed:y2_fixed, x1_fixed:x2_fixed]

        # Mostrar la imagen recortada
        im_rec = Image.fromarray(ImgRec)
        img_rec = ImageTk.PhotoImage(image=im_rec)
        GImagenROI.configure(image=img_rec)
        GImagenROI.image = img_rec


    
'''    
def recortar():
    global ImgRec
    Vx1 = int(x1.get())
    Vy1 = int(y1.get())
    Vx2 = int(x2.get())
    Vy2 = int(y2.get())
    ImgRec = Captura[Vx1:Vx2, Vy1:Vy2]
    Im = Image.fromarray(ImgRec)
    ImRec = ImageTk.PhotoImage(image=Im)
    LImagenROI.configure(image= ImRec)
    LImagenROI.image = ImRec
'''

import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

def umbralizacion():
    global thresh1, mask
    valor = int(numeroUmbra.get())

    # Aplicar umbral sobre la imagen recortada
    ret, thresh1 = cv2.threshold(ImgRec, valor, 255, cv2.THRESH_BINARY)

    # Contar los píxeles de las manchas
    total_pixeles = thresh1.size
    pixeles_manchas = np.count_nonzero(thresh1 == 255)  # Píxeles blancos
    porcentaje_manchas = (pixeles_manchas / total_pixeles) * 100

    # Encontrar contornos
    contornos, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cantidad_contornos = len(contornos)

    # Convertir resultado a imagen de Tkinter
    Umbra1 = Image.fromarray(thresh1)
    Umbra1 = ImageTk.PhotoImage(image=Umbra1)

    # Mostrar resultado en UImagen
    UImagen.configure(image=Umbra1)
    UImagen.image = Umbra1

    # Mostrar información en LImagenROI
    info_manchas = f"Píxeles con manchas: {pixeles_manchas}\n" \
                   f"Porcentaje: {porcentaje_manchas:.2f}%\n" \
                   f"Contornos detectados: {cantidad_contornos}"

    LImagenROI.configure(text=info_manchas, font=("Arial", 12), fg="white", bg="blue", justify="left")



def Analizar_Patron():
    global ImgCompleta

    if ImgCompleta is None:
        return

    # Hacemos una copia de la imagen completa para dibujar sin modificar la original
    imagen_dibujo = ImgCompleta.copy()

    # Coordenadas del recorte (mismas que usaste en Capturar)
    x1, y1 = 110, 80
    x2, y2 = 190, 145

    # Dibujar rectángulo blanco en la zona recortada
    cv2.rectangle(imagen_dibujo, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # Convertir la imagen a formato de Tkinter y mostrarla
    pil_image = Image.fromarray(imagen_dibujo)
    tk_image = ImageTk.PhotoImage(image=pil_image)
    LImagenPatron.configure(image=tk_image)
    LImagenPatron.image = tk_image

    # También podrías agregar umbralización si necesitas analizarla después:
    valor = int(numeroUmbra.get())
    _, thresh = cv2.threshold(ImgCompleta, valor, 255, cv2.THRESH_BINARY_INV)

    # Porcentaje de blancos
    area_blanca = cv2.countNonZero(thresh)
    area_total = thresh.shape[0] * thresh.shape[1]
    porcentaje = (area_blanca / area_total) * 100

    # Mostrar texto
    CajaTexto2.configure(state='normal')
    CajaTexto2.delete(1.0, tk.END)
    CajaTexto2.insert(1.0, f"Porcentaje de actividad: {round(porcentaje, 2)}%")
    CajaTexto2.configure(state='disabled')


logo = tk.PhotoImage(file="LogoUBB.png")
logoUBB = tk.Label(image=logo)
logoUBB.place(x=1150, y=550)

alumna = tk.Label(ventana, text="Estudiante practicante\nFrancisca Huaique Garrido", font=("Arial", 11, "bold")).place(x=1075, y=670)
carrera = tk.Label(ventana, text="Ingenieria de Ejecucion\nen Computacion e Informatica", font=("Arial", 11, "bold")).place(x=1060, y=720)
profesor = tk.Label(ventana, text="LabCIM", font=("Arial", 11, "bold")).place(x=1250, y=780)



# SpinBox
numeroUmbra = tk.Spinbox(ventana, from_=0, to=255)
numeroUmbra.place(x=1180, y=310, width=42, height=22)


# Botones 
BCamara = tk.Button(ventana, text="Iniciar cámara", command= camara, font=("Arial", 11, "bold"))
BCamara.place(x=40, y=330, width=150, height=40)
BCapturar = tk.Button(ventana, text="Tomar foto", command= Capturar, font=("Arial", 12, "bold"))
BCapturar.place(x=270, y=330, width=150, height=40)
BBinary = tk.Button(ventana, text="Umbralizacion", command= umbralizacion, font=("Arial", 11, "bold"))
BBinary.place(x=1000, y=310, width=150, height=40), 

BPatron = tk.Button(ventana, text="Analizar patron", command= Analizar_Patron, font=("Arial", 11, "bold"))
BPatron.place(x=600, y=670, width=150, height=40)



# Cuadros de imagen 
LImagen = tk.Label(ventana, background="blue")
LImagen.place(x=100, y=50, width=300, height=240)

LImagenROI = tk.Label(ventana, background="blue")
LImagenROI.place(x=100, y=380, width=301, height=240)

GImagenROI = tk.Label(ventana, background="blue")
GImagenROI.place(x=510, y=50, width=301,  height=240)
GImagenROI.bind('<Button-1>', mostrar_coordenadas)



# Mostrar el patron
LImagenPatron = tk.Label(ventana, background= "blue")
LImagenPatron.place(x=510, y=380, width=301, height=240)

CajaTexto2 = tk. Text(ventana, height=2, width=30, state='disabled')
CajaTexto2.place(x=850, y=380)

UImagen = tk.Label(ventana, background="blue")
UImagen.place(x=930, y=50, width=301,  height=240)


# Label

coordenadasTitulo = tk.Label(ventana, text="Coordenadas", font=("Arial", 11, "bold"))
coordenadasTitulo.place(x=625, y=310)
coordenadas = tk.Label(ventana, text="")
coordenadas.place(x=625, y=340)




ventana.mainloop()