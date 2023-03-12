import cv2 
import numpy as np



def direction_control(cx,cy,object_detected, frameWidth, frameHeight, deadZone, imgContour):
    if object_detected==1:
        if (cx <int(frameWidth/2)-deadZone):
            cv2.putText(imgContour, " GO LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
            cv2.rectangle(imgContour,(0,int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
            dir = 1
        elif (cx > int(frameWidth / 2) + deadZone):
            cv2.putText(imgContour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
            cv2.rectangle(imgContour,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(frameWidth,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
            dir = 2
        elif (cy < int(frameHeight / 2) - deadZone):
            cv2.putText(imgContour, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
            cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
            dir = 3
        elif (cy > int(frameHeight / 2) + deadZone):
            cv2.putText(imgContour, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
            cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)
            dir = 4
        else: 
            # Objeto centrado
            cv2.putText(imgContour, " GO FORWARD " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
            cv2.rectangle(imgContour,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
            dir=-1
    else:
        # Objeto no encontrado
        dir = 0

    return dir

def movement_control(drone, dir, contador_securidad, num_puertas):
    if contador_seguridad < 0:
        contador_seguridad = 0
    elif contador_seguridad > 11:
        contador_seguridad = 10
    
    if dir == -1:
        contador_seguridad +=1
        print("Contador seguridad: ", contador_seguridad)
        if contador_seguridad == 10:
            contador_seguridad = 0
            print("Atravesando puerta ...")
            num_puertas += 1 
            drone.left_right_velocity = 0; drone.for_back_velocity = 0;drone.up_down_velocity = 0; drone.yaw_velocity = 0
            drone.move_forward(100)
        else:
            drone.left_right_velocity = 0; drone.for_back_velocity = 0;drone.up_down_velocity = 0; drone.yaw_velocity = 0

    elif dir == 1:
        contador_seguridad -=1
        drone.yaw_velocity = -60
    elif dir == 2:
        contador_seguridad -=1
        drone.yaw_velocity = 60
    elif dir == 3:
        contador_seguridad -=1
        drone.up_down_velocity= 60
    elif dir == 4:
        contador_seguridad -=1
        drone.up_down_velocity= -60
    else:
        contador_seguridad -=1
        drone.left_right_velocity = 0; drone.for_back_velocity = 0;drone.up_down_velocity = 0; drone.yaw_velocity = 0

    # SEND VELOCITY VALUES TO TELLO
    if drone.send_rc_control:
        drone.send_rc_control(drone.left_right_velocity, drone.for_back_velocity, drone.up_down_velocity, drone.yaw_velocity)

    return contador_seguridad, num_puertas

def movement_control_sim(dir, contador_seguridad, num_puertas):
    if contador_seguridad < 0:
        contador_seguridad = 0
    elif contador_seguridad > 11:
        contador_seguridad = 10

    if dir == -1:
        contador_seguridad +=1
        print("Contador seguridad: ", contador_seguridad)
        if contador_seguridad > 10:
            contador_seguridad = 0
            print("Atravesando puerta ...")
            num_puertas+=1
        else:
            print("Dron quieto")
    elif dir == 1:
        contador_seguridad -=1
        print("Girando izquierda")
    elif dir == 2:
        contador_seguridad -=1
        print("Girando derecha")
    elif dir == 3:
        contador_seguridad -=1
        print("Subiendo")
    elif dir == 4:
        contador_seguridad -=1
        print("Bajando")
    else:
        contador_seguridad -=1
        print("Dron quieto")
    
    return contador_seguridad, num_puertas
