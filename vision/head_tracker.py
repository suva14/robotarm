import cv2
import numpy as np
from picamera2 import Picamera2
import serial
import time

# Configuration UART
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

# Paramètres
CENTER_THRESHOLD = 50  # Tolérance en pixels autour du centre (à ajuster)
SERVO_SPEED = 10       # Vitesse de rotation (degrés par itération)

# Initialisation caméra
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# Classificateur de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def move_servo(direction):
    """ Envoie une commande à l'ESP32 """
    if direction == "left":
        ser.write(b"base_left\n")
    elif direction == "right":
        ser.write(b"base_right\n")
    else:
        ser.write(b"base_stop\n")

try:
    while True:
        # Capture d'image
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détection de visage
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            # Prendre le premier visage détecté
            (x, y, w, h) = faces[0]
            face_center_x = x + w//2

            # Calcul décalage par rapport au centre
            frame_center = frame.shape[1] // 2
            offset = face_center_x - frame_center

            # Déterminer la direction
            if offset < -CENTER_THRESHOLD:
                move_servo("left")
            elif offset > CENTER_THRESHOLD:
                move_servo("right")
            else:
                move_servo("stop")

        else:
            move_servo("stop")

        time.sleep(0.1)  # Réduire la charge CPU

except KeyboardInterrupt:
    ser.close()
    picam2.stop()