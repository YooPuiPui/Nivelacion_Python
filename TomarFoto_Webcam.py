import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import imutils
import cv2

ventana = tk.Tk()
ventana.geometry("740x370")
ventana.resizable(0,0)
ventana.title("WEBCAM")

def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()

def iniciar():
    global capture
    if capture is not None:
        ret, frame = capture.read()
        if ret == True:
            frame = imutils.resize(frame, width=311) # es el ancho de la imagen
            frame = imutils.resize(frame, height=241) # la altura
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # que sea full a color
            im = Image.fromarray(ImagenCamara)
            img = ImageTk.PhotoImage(image= im)
            LImagen.configure(image= img)
            LImagen.image = img
            LImagen.after(1,iniciar)
        else:
            LImagen.image = ""
            capture.release()
            

# Funcion para tomar una foto y se muestre en la ventana

def Capturar():
    global Captura
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image= im)
    LImagenROI.configure(image= img)
    LImagenROI.image = img
    
# Botones

BCamara = tk.Button(ventana, text="Iniciar camara", command=camara) # command llama a la funcion, en este caso camara
BCamara.place(x=150, y=330, width=90, height=23)

BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar)
BCapturar.place(x=500, y=330, width=91, height=23)


# Cuadro de imagen donde se reproducira la webcam
LImagen = tk.Label(ventana, background="blue")
LImagen.place(x=50, y=50, width=300, height=240)

LImagenROI = tk.Label(ventana, background="blue")
LImagenROI.place(x=390, y=50, width=300, height=240)

ventana.mainloop()