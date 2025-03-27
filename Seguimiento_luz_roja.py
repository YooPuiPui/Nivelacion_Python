from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time 

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", # argumento opcional para especificar la ruta de n video
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# Definimos los valores en los que estara nuestro rojo, en formato BGR
redLower = (161, 155, 84)
redUpper = (179, 255,255)
pts = deque(maxlen=args["buffer"])

# Iniciamos la captura de video y se crea un mask

if not args.get("video", False):
    vs = VideoStream(src=0).start() # Esto activa la camara
else:
    vs = cv2.VideoCapture(args["video"]) # Esto carga un video proporcionado.
# Tiempo asignado para que la camara cargue
time.sleep(2.0)

while True:
    
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    
    if frame is None:
        break
    frame = imutils.resize(frame, width=600) # Cambia el ancho para procesarlo mas rapido
    blurred = cv2.GaussianBlur(frame, (11,11), 0) # reduce el ruido de la imagen
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    

    # Encontrar el punto central de la pelota
    # (x,y)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # Se procede solo si se encuentra un contorno
    if len(cnts) > 0:
    
        # Encuentra el contorno mas grande y lo usa
        # Crea el menor contorno posible
        
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        # Procesa solo si el radio cumple con el valor minimo
        if radius > 10:
            # Dibuja el circulo y actualiza la lista de puntos rastreados
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0,255,255,), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # Actualiza la cola de puntos        
    pts.appendleft(center)
    
    for i in range(1, len(pts)):
        # Si no hay puntos ignora
        if pts[i-1] is None or pts[i] is None:
            continue
        # Calcular el grosor de la linea y la dibuja
        thickness = int(np.sqrt(args["buffer"] / float(i+1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        
    # Mostrar la ventana en pantalla
    cv2.imshow("Seguimiento de pelota roja", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # Cerrar el programa con la letra f
    if key == ord("f"):
        break
    
if not args.get("video", False):
    vs.stop()
else:
    vs.release()