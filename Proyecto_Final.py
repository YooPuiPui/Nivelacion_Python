import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import imutils
import cv2

# Crea ventana, define tamaño y título
ventana = tk.Tk()
ventana.geometry("1320x800")
ventana.resizable(0,0)
ventana.title("Proyecto procesamiento de imagen con Webcam")

#Variables globales
global Captura, CapturaG

#Inicia cámara web
def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()
    
def iniciar():
    global capture
    if capture is not None:
        BCapturar.place(x=250,y=330,width=91,height=23)
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
    global valor, Captura, CapturaG
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    CapturaG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image= im)
    imG = Image.fromarray(CapturaG)
    imgG = ImageTk.PhotoImage(image= imG)
    GImagenROI.configure(image= imgG)
    GImagenROI.image = imgG
    LImagenRecorte.configure(image= img)
    LImagenRecorte.image = img


def rgb():
    global img_mask, img_aux, bin_imagen
    Minimos = (int(SRedI.get()),int(SGreenI.get()),int(SBlueI.get()))
    maximos = (int(SRedD.get()),int(SGreenD.get()),int(SBlueD.get()))
    img_mask = cv2.inRange(ImgRec, Minimos, maximos)
    img_aux = img_mask
    img_mask = Image.fromarray(img_mask)
    img_mask = ImageTk.PhotoImage(image= img_mask)
    LImagenManchas.configure(image=img_mask)
    LImagenManchas.image = img_mask
    _, bin_imagen = cv2.threshold(img_aux, 0, 255, cv2.THRESH_BINARY_INV)

def manchas():
    # Contar el número de píxeles con manchas
    num_pixels_con_manchas = cv2.countNonZero(bin_imagen)
    # Calcular el porcentaje de manchas
    porcentaje_manchas = 100 - (num_pixels_con_manchas / bin_imagen.size) * 100
    #Contornos
    contornos = cv2.findContours(img_aux, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    #Cantidad de contornos
    num_formas = len(contornos)
    Cadena = f"Cantidad de manchas blancas: {num_formas}\nPorcentaje área con manchas: {round(porcentaje_manchas,2)}%"
    CajaTexto2.configure(state='normal')
    CajaTexto2.delete(1.0, tk.END)
    CajaTexto2.insert(1.0, Cadena)
    CajaTexto2.configure(state='disabled')

def umbralizacion():
    global thresh1, mask
    valor = int(numeroUmbra.get())
    ret, thresh1 = cv2.threshold(CapturaG, valor, 255, cv2.THRESH_BINARY)
    Umbral = Image.fromarray(thresh1)
    Umbral = ImageTk.PhotoImage(image=Umbral)
    UImagen.configure(image = Umbral)
    UImagen.image = Umbral

    min = (valor, valor, valor)
    max = (255,255,255)
    mask = cv2.inRange(Captura, min, max)


def manchasG():
     # Contar el número de píxeles con manchas
    num_pixels_con_manchas = cv2.countNonZero(thresh1)
    # Calcular el porcentaje de manchas
    porcentaje_manchas = 100 - (num_pixels_con_manchas / thresh1.size) * 100
    #Contornos
    contornos = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
   
    #Cantidad de contornos
    manchas = len(contornos)
    Cadena = f"Cantidad de manchas blancas: {manchas}\nPorcentaje área sin manchas:{round(porcentaje_manchas,2)}%"
    CajaTexto.configure(state='normal')
    CajaTexto.delete(1.0, tk.END)
    CajaTexto.insert(1.0, Cadena)
    CajaTexto.configure(state='disabled')

def mostrar_coordenadas(event):
    coordenadas['text']=f'x = {event.x}    y = {event.y}'

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


#Botones
BCamara = tk.Button(ventana, text="Iniciar cámara", command=camara)
BCamara.place(x=60,y=330,width=90,height=23)
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar)
BCapturar.place(x=250,y=330,width=91,height=23)
BManchas = tk.Button(ventana, text="Umbralización", command=rgb)
BManchas.place(x=760,y=640,width=100,height=23)
#ManchasRGB = tk.Button(ventana, text="Análisis de manchas", command=manchas)
#ManchasRGB.place(x=880,y=640,width=120,height=23)
BBinary = tk.Button(ventana, text="Umbralización", command=umbralizacion)
BBinary.place(x=800,y=310,width=90,height=23)
##BManchasG = tk.Button(ventana, text="Análisis de Manchas", command=manchasG)
##BManchasG.place(x=1100,y=310,width=131,height=23)
BRecortar = tk.Button(ventana, text="Recortar", command=recortar)
BRecortar.place(x=155,y=700,width=80,height=23)


#SpinBox
numeroUmbra = tk.Spinbox(ventana, from_=0,to=255)
numeroUmbra.place(x=900, y=310, width=42, height=22)
x1 = tk.Spinbox(ventana, from_=0,to=298)
x1.place(x=140, y=630, width=42, height=22)
y1 = tk.Spinbox(ventana, from_=0,to=239)
y1.place(x=240, y=630, width=42, height=22)
x2 = tk.Spinbox(ventana, from_=1,to=298)
x2.place(x=140, y=660, width=42, height=22)
y2 = tk.Spinbox(ventana, from_=1,to=239)
y2.place(x=240, y=660, width=42, height=22)

#Label
LRed = tk.Label(ventana, text="R")
LRed.place(x=530,y=640,width=21,height=16)
LGreen = tk.Label(ventana, text="G")
LGreen.place(x=530,y=680,width=21,height=16)
LBlue = tk.Label(ventana, text="B")
LBlue.place(x=530,y=720,width=21,height=16)
coordenadasTitulo = tk.Label(ventana, text="Coordenadas")
coordenadasTitulo.place(x=505, y=310)
coordenadas = tk.Label(ventana, text="")
coordenadas.place(x=495, y=330)
Lx1 = tk.Label(ventana, text="x1")
Lx1.place(x=120, y=630)
Ly1 = tk.Label(ventana, text="y1")
Ly1.place(x=220, y=630)
Lx2 = tk.Label(ventana, text="x2")
Lx2.place(x=120, y=660)
Ly2 = tk.Label(ventana, text="y2")
Ly2.place(x=220, y=660)

# Logo de la u

logo = tk.PhotoImage(file="LogoUBB.png")
logoUBB = tk.Label(image=logo)
logoUBB.place(x=1250, y=615)

# datos
alumnas = tk.Label(ventana, text="Estudiante practicante\n\nFrancisca Huaique Garrido").place(x=1075, y=620)
carrera = tk.Label(ventana, text="Ingenieria de Ejecucio\nen Computacion e Informatica").place(x=1060, y=720)
profesor = tk.Label(ventana, text="Profesor\nLuis Vera").place(x=1250, y=700)
LabCIM = tk.Label(ventana, text="LabCIM").place(x=1250, y=740)

# Cuadros de imagen

LImagen = tk.Label(ventana, background="blue")
LImagen.place(x=50,y=50,width=300,height=240)
LImagenROI = tk.Label(ventana, background="blue")
LImagenROI.place(x=390,y=380,width=300,height=240)
GImagenROI = tk.Label(ventana, background="blue")
GImagenROI.place(x=390,y=50,width=300,height=240)
GImagenROI.bind('<Button-1>', mostrar_coordenadas)
UImagen = tk.Label(ventana, background="blue")
UImagen.place(x=730,y=50,width=301,height=240)
LImagenManchas = tk.Label(ventana, background="blue")
LImagenManchas.place(x=730,y=380,width=301,height=240)
LImagenRecorte = tk.Label(ventana, background="blue")
LImagenRecorte.place(x=50,y=380,width=301,height=240)

# Cuadro de texto

CajaTexto = tk.Text(ventana, state="disabled")
CajaTexto.place(x=1055,y=50,width=225,height=220)
CajaTexto2 = tk.Text(ventana, state="disabled")
CajaTexto2.place(x=1055,y=380,width=225,height=220)


# RGB 

#RGB se inicia en 1, ya que si no sale error de división por 0
SRedI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SRedI.place(x=400,y=620)
SGreenI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SGreenI.place(x=400, y= 660)
SBlueI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SBlueI.place(x=400, y= 700)

SRedD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SRedD.set(255)
SRedD.place(x=580,y=620)
SGreenD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SGreenD.set(255)
SGreenD.place(x=580, y= 660)
SBlueD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SBlueD.set(255)
SBlueD.place(x=580, y= 700)


# Pasos

paso1 = tk.Label(ventana, text="Paso1. Encender la camara y tomar una foto")
paso1.place(x=70, y=20)
paso2 = tk.Label(ventana, text="Paso2. Revisar las coordenadas para recortar la foto")
paso2.place(x=400, y=20)
paso3 = tk.Label(ventana, text="Paso3. Escribir las coordenadas para recortar la foto")
paso3.place(x=50, y=730)
paso4a = tk.Label(ventana, text="Paso4a. Elegir un numero entre 0 y 255 para umbralizar la\nimagen en escala de grises")
paso4a.place(x=720, y=10)
paso4b = tk.Label(ventana, text="Paso4b. Eligir un rango de numeros RGB para \numbralizar la imagen a color")
paso4b.place(x=750, y=700)
paso5 = tk.Label(ventana, text="Paso5. Analizar manchas")
paso5.place(x=1100, y=20)

ventana.mainloop()