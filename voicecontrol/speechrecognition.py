import serial
import time
import speech_recognition as sr
# Initialisation de la communication série
ser = serial.Serial('COM11', 9600, timeout=1)  # Remplacez COM par le port série approprié
ser.flush()

def listen_command():
    """Fonction pour écouter une commande vocale et la reconnaître."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dites 'turn right' ou 'turn left' :")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            print("Commande non reconnue, essayez encore.")
        except sr.RequestError as e:
            print(f"Erreur avec le service de reconnaissance vocale : {e}")
        except sr.WaitTimeoutError:
            print("Temps d'attente écoulé.")
        return None

def send_to_arduino(command):
    """Envoie la commande au microcontrôleur via la liaison série."""
    if command == "turn right":
        ser.write(b'R')  # Envoie 'R' pour tourner à droite
        print("Commande envoyée : Turn Right")
    elif command == "turn left":
        ser.write(b'L')  # Envoie 'L' pour tourner à gauche
        print("Commande envoyée : Turn Left")
    else:
        print("Commande inconnue, aucune action envoyée.")

if __name__ == "__main__":
    print("Contrôle du servomoteur par commande vocale")
    time.sleep(2)  # Attente pour l'initialisation de la connexion série

    while True:
        command = listen_command()
        if command:
            send_to_arduino(command)

        # Quitte le programme si 'exit' est entendu
        if command == "exit":
            print("Arrêt du programme.")
            break