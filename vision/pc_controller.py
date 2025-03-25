import cv2
import speech_recognition as sr
import serial
import threading

# Configuration série - MODIFIEZ LE PORT !
SER_PORT = 'COM11'  # Windows : 'COMX', Linux : '/dev/ttyUSB0'
ser = serial.Serial(SER_PORT, 115200, timeout=1)

# Paramètres communs
CENTER_THRESHOLD = 100  # Sensibilité du suivi
VOICE_CMDS = {"gauche": "LEFT", "droite": "RIGHT", "stop": "STOP"}

def vision_control():
    cap = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_center = x + w//2
            frame_center = frame.shape[1]//2
            
            if face_center < frame_center - CENTER_THRESHOLD:
                ser.write(b'RIGHT\n')
            elif face_center > frame_center + CENTER_THRESHOLD:
                ser.write(b'LEFT\n')
        
        cv2.imshow('Face Tracking', frame)
        if cv2.waitKey(1) == 27:  # Echap pour quitter
            break
    
    cap.release()
    cv2.destroyAllWindows()

def voice_control():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = r.listen(source, timeout=2)
                text = r.recognize_google(audio, language="fr-FR").lower()
                print("Commande vocale:", text)
                
                for cmd, code in VOICE_CMDS.items():
                    if cmd in text:
                        ser.write(f"{code}\n".encode())
                        
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Erreur API:", e)

if __name__ == "__main__":
    print("Démarrage du contrôleur...")
    threading.Thread(target=vision_control, daemon=True).start()
    threading.Thread(target=voice_control, daemon=True).start()
    
    # Garder le programme actif
    while True: 
        pass