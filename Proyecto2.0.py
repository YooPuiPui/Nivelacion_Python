import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import imutils
import cv2

# Variables globales
global img, Region,valor
imageToShow=None
Captura=None

# Ventana
ventana = tk.Tk()
ventana.geometry("1850x1000")
ventana.title("Analisis de patrones")

# Funciones
def archivo():
    try:
        # Lee la imagen
        path_image = filedialog.askopenfilename(filetype=[
            ("image", "jpg"),
            ("image", "jpeg"),
            ("image", "png")
        ])
        if len(path_image) > 0:
            global imagenFile, img, imageToShow, valor
            imagenFile = cv2.imread(path_image)
            imagenFile = imutils.resize(imagenFile, height=240)
            imagenFile = imutils.resize(imagenFile, width=300)
            imageToShow = cv2.cvtColor(imagenFile, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im)
            LImagen.configure(image=img)
            LImagen.image = img
            imageToShow = cv2.cvtColor(imagenFile, cv2.COLOR_BGR2GRAY)
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im)
            LImagen2.configure(image=img)
            LImagen2.image = img
            valor = 0
    except Exception as e:
        messagebox.showerror(message="El archivo seleccionado no es un tipo de imagen válido")
        imageToShow = None

# Define una variable global para mantener el estado de la cámara y la visibilidad del botón
camara_activada = False
boton_iniciar_visible = False

def camara():
    global capture, camara_activada, boton_iniciar_visible
    if not camara_activada:
        try:
            capture = cv2.VideoCapture(cv2.CAP_ANY)
            iniciar()
            camara_activada = True
            boton_iniciar_visible = True  # Mostrar el botón "Iniciar captura"
        except Exception as e:
            messagebox.showerror(message="Error al inicializar la cámara: " + str(e))
    else:
        # Si la cámara ya está activada, detén la captura y libera los recursos
        if capture is not None:
            capture.release()
            boton_iniciar_visible = False  # Ocultar el botón "Iniciar captura"
        LImagen.configure(image="")
        messagebox.showinfo(message="Cámara desactivada")
        camara_activada = False

def iniciar():
    global capture
    if capture is not None:
        ret, frame = capture.read()
        if ret == True:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ImagenCamara)
            img = ImageTk.PhotoImage(image=im)
            LImagen.configure(image=img)
            LImagen.image = img
            LImagen.after(10, iniciar)
        else:
            LImagen.image = ""
            capture.release()
            messagebox.showerror(message="No se pudo capturar ningún fotograma.")

def Capturar():
    global valor,Captura
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagen.configure(image=img)
    LImagen.image = img
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagen2.configure(image=img)
    LImagen2.image = img
    valor = 2

def actualizar_area_recorte(_=None):
    global imageToShow, valor, Captura
    if imageToShow is not None or Captura is not None:
        x = SX.get()
        y = SY.get()
        w = SW.get()
        h = SH.get()

        # Inicializar con un valor predeterminado
        imagen_recortada = None

        if valor == 0:
            imagen_recortada = imageToShow.copy()
        else:
            imagen_recortada = Captura.copy()

            # Crear una máscara negra del mismo tamaño que la imagen original
        mascara_negra = np.zeros_like(imagen_recortada)

            # Establecer el área seleccionada
        mascara_negra[y:h, x:w] = 255

            # Superponer la imagen original con el área seleccionada
        imagen_recortada = cv2.bitwise_and(imagen_recortada, mascara_negra)

        im = Image.fromarray(imagen_recortada)
        img_recortada = ImageTk.PhotoImage(image=im)
        LImagen2.configure(image=img_recortada)
        LImagen2.image = img_recortada

# Función para recortar imagen
def recortar_imagen():
    global imageToShow, valor,Captura
    x = SX.get()
    y = SY.get()
    w = SW.get()
    h = SH.get()
    if valor == 0:
        imagen_recortada = imageToShow[y:h, x:w]
    else:
        imagen_recortada = Captura[y:h, x:w]

    # Superponer la imagen recortada en la posición deseada
    im = Image.fromarray(imagen_recortada)
    img_recortada = ImageTk.PhotoImage(image=im)
    LImagen2.configure(image=img_recortada)
    LImagen2.image = img_recortada
    return(imagen_recortada)

def rgb():
    # Recortar la imagen antes de analizar las manchas
    recortada=recortar_imagen()

    # Luego proceder con el análisis de las manchas

    umb=int(SGray.get())
    img_mask=cv2.inRange(recortada,umb,255)
    #img_mask = cv2.inRange(recortada, Minimos, maximos)
    
    img_aux = 255 - img_mask
    img_mask = Image.fromarray(img_mask)
    img_mask = ImageTk.PhotoImage(image=img_mask)
    LImagenManchas.configure(image=img_mask)
    LImagenManchas.image = img_mask
    
    #_, bin_imagen = cv2.threshold(img_aux, 0, 255, cv2.THRESH_BINARY)
    _, bin_imagen = cv2.threshold(img_aux, umb, 255, cv2.THRESH_BINARY_INV)
    # Contar el número de píxeles con manchas
    num_pixels_con_manchas = cv2.countNonZero(bin_imagen)
    # Calcular el porcentaje de manchas
    porcentaje_manchas = 100 - (num_pixels_con_manchas / bin_imagen.size) * 100
    # Contornos
    contornos,_ = cv2.findContours(img_aux, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #contornos = cv2.findContours(img_aux, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    area = 0
    # Verificar si num_pixels_con_manchas es diferente de cero antes de dividir
    if num_pixels_con_manchas != 0:
        area = (bin_imagen.size / (num_pixels_con_manchas / bin_imagen.size))
    else:
        area = 0
    # Cantidad de contornos
    num_formas = len(contornos)
    Cadena = f"Cantidad de manchas detectada:{num_formas}\nArea Mancha: {area}\nPorcentaje de manchas negras:{round(porcentaje_manchas,2)}%"
    CajaTexto.configure(state='normal')
    CajaTexto.delete(1.0, tk.END)
    CajaTexto.insert(1.0, Cadena)
    CajaTexto.configure(state='disabled')
    return img_aux


def Analizar_Patron():
    recortada = rgb()

    if valor == 0:
        template = imageToShow.copy()
    else:
        template= Captura.copy()
    # Umbralizar la imagen
    ret, thresh = cv2.threshold(recortada, 0, 255, cv2.THRESH_BINARY_INV)

    res = cv2.matchTemplate(template, thresh, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    x1, y1 = min_loc
    x2, y2 = min_loc[0] + thresh.shape[1], min_loc[1] + thresh.shape[0]

    cv2.rectangle(template, (x1, y1), (x2, y2), (255, 255, 255), 3)

    pil_image = Image.fromarray(template)
    tk_image = ImageTk.PhotoImage(image=pil_image)

    LImagenPatron.configure(image=tk_image)
    LImagenPatron.image = tk_image

    # Calcular el área del umbralizado (thresh)
    area_thresh = cv2.countNonZero(thresh)
    # Calcular el área del patrón buscado
    area_patron = thresh.shape[0] * thresh.shape[1]
    # Calcular el porcentaje de precisión
    porcentaje_precision = (area_thresh / area_patron) * 100

    # Actualizar el texto con el porcentaje de precisión
    CajaTexto2.configure(state='normal')
    CajaTexto2.delete(1.0, tk.END)
    CajaTexto2.insert(1.0, f"Porcentaje de precisión: {round(porcentaje_precision, 2)}%")
    CajaTexto2.configure(state='disabled')




# Sliders para recorte de imagen
SX = tk.Scale(ventana, from_=0, to=300, orient='horizontal', command=actualizar_area_recorte)
SX.place(x=450,y=10, width=311)
SY = tk.Scale(ventana, from_=0, to=240, orient='vertical', command=actualizar_area_recorte)
SY.place(x=420,y=50, height=241)
SW = tk.Scale(ventana, from_=0, to=300, orient='horizontal', command=actualizar_area_recorte)
SW.place(x=450,y=345, width=311)
SW.set(300)
SH = tk.Scale(ventana, from_=0, to=240, orient='vertical', command=actualizar_area_recorte)
SH.place(x=815, y=50, height=241)
SH.set(240)



# Botones
BRecortar = tk.Button(ventana, text="Recortar Imagen", command=recortar_imagen, font=("Arial", 13, "bold"))
BRecortar.place(x=500, y=400, width=170, height=40)


BCamara = tk.Button(ventana, text="Camara", command=camara, font=("Arial", 15, "bold"))
BCamara.place(x=70,y=400,width=100,height=33)
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar, font=("Arial", 14, "bold"))
BCapturar.place(x=210, y=400, width=140, height=33)
BFormas = tk.Button(ventana, text="Buscar Formas", command=rgb, font=("Arial", 14, "bold"))
BFormas.place(x=1000,y=370,width=149,height=23)
#BPatrones = tk.Button(ventana, text="Analizar Patron", command=Analizar_Patron,  font=("Arial", 14, "bold"))
#BPatrones.place(x=1400,y=370,width=149,height=33)

umbralizacion = tk.Label(ventana, text="Umbralizacion", font=("Arial", 14, "bold")).place(x=500, y=450)


# Cuadros de Imagen
LImagen = tk.Label(ventana, background="blue")
LImagen.place(x=50,y=50,width=350,height=290)
LImagen2 = tk.Label(ventana, background="blue") 
LImagen2.place(x=460, y=50, width=350, height=290)
LImagenManchas = tk.Label(ventana, background="blue")
LImagenManchas.place(x=910,y=50,width=350,height=290)
#LImagenPatron = tk.Label(ventana, bg="blue")
#LImagenPatron.place(x=1300,y=50,width=350,height=290)

# Cuadro de Texto
CajaTexto = tk.Text(ventana, state="disabled")
CajaTexto.place(x=930,y=400,width=311,height=121)
#CajaTexto2 = tk.Text(ventana, state="disabled")
#CajaTexto2.place(x=1330,y=400,width=311,height=121)



SGray = tk.Scale(ventana, from_=0, to=255, orient='horizontal')
SGray.place(x=430, y= 490,width=300)

ventana.mainloop()
