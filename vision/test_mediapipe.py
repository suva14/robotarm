import cv2
import mediapipe as mp
import os

# Réduction des logs TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialisation de MediaPipe pour la détection des visages et des mains
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Configuration de MediaPipe
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
hands = mp_hands.Hands(False)

# Configuration de la capture webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1260)  # Largeur
cap.set(4, 1080)  # Hauteur

while True:
    success, img = cap.read()
    if not success:
        break

    # Conversion en RGB pour MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Détection des visages
    face_results = face_detection.process(imgRGB)
    if face_results.detections:
        for detection in face_results.detections:
            # Dessiner les détections de visage
            mp_drawing.draw_detection(img, detection)

    # Suivi des mains
    hand_results = hands.process(imgRGB)
    if hand_results.multi_hand_landmarks:
        for handLms in hand_results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 0:  # Index 0 (poignet ou point spécifique)
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            # Dessin des connexions entre les points de la main
            mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Affichage de l'image
    cv2.imshow("Face and Hand Tracking", img)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libération des ressources
cap.release()
cv2.destroyAllWindows()


