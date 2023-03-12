from djitellopy import Tello
import cv2
import numpy as np
from opencv_utils import *
from control_utils import *

##################
using_tello = 0 # poner a 1 si se tiene el dron
tello_cam = 0 # poner a 1 si se tiene el dron y sólo se quiere usar la cámara
##################

# Image configuration
width = 640 
height = 480  
deadZone =100
frameWidth = width
frameHeight = height

# Variable global para la imagen
global imgContour

# Conectar dron
if using_tello or tello_cam:
    drone = Tello()
    drone.connect()
    drone.for_back_velocity = 0
    drone.left_right_velocity = 0
    drone.up_down_velocity = 0
    drone.yaw_velocity = 0
    drone.speed = 0
    print("Batería: ", drone.get_battery(), "%")

# Configuración de camara
if tello_cam == 0:
    cap = cv2.VideoCapture(0) 
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
else:
    drone.streamoff()
    drone.streamon()


# Crear ventana con trackbars
create_trackbar(empty)

# Bucle principal
while True:
    # Lectura de imagen
    if tello_cam == 1:
        frame_read = drone.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (width, height))
        pass
    else:
        _, img = cap.read()

    imgContour = img.copy()
    
    # Usar trackbars y filtros para preprocesamiento de imagen
    result, imgDil = procesamiento_imagen(img)

    # Detección de contornos
    cx,cy,object_detected = getContours(imgDil, imgContour, frameWidth, frameHeight, deadZone)
    display(imgContour, frameWidth, frameHeight, deadZone)
    print(cx, cy, object_detected)

    # Control de dirección
    dir = direction_control(cx,cy,object_detected, frameWidth, frameHeight, deadZone, imgContour)
    print("Movimiento:", dir)

    # Control de movimiento 
    if using_tello:
        # Despegar dron
        if startCounter == 0:
            drone.takeoff()
            startCounter = 1
        # Actuar según dirección del objeto detectado
        movement_control(drone, dir)

    # Display 
    stack = stackImages(0.9, ([img, result], [imgDil, imgContour]))
    cv2.imshow('Horizontal Stacking', stack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        if using_tello:
            # Aterrizaje de emergencia
            drone.land()
        break

# cap.release()
cv2.destroyAllWindows()