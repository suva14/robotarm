import serial
import time
import speech_recognition as sr
from threading import Thread

class VoiceArmController:
    def __init__(self, port='COM11', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.running = True
        self.recognizer = sr.Recognizer()
        time.sleep(2)  # Initialisation
        
    def listen_loop(self):
        """Écoute continue des commandes vocales"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.running:
                try:
                    print("Dites une commande ('droite', 'gauche', 'ouvrir', 'fermer', 'stop')...")
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)
                    command = self.recognizer.recognize_google(audio, language='fr-FR').lower()
                    self.process_command(command)
                except (sr.UnknownValueError, sr.WaitTimeoutError):
                    continue
                except sr.RequestError as e:
                    print(f"Erreur API: {e}")
                    break

    def process_command(self, command):
        """Traduction des commandes vocales en signaux série"""
        cmd_map = {
            'droite': 'R',
            'gauche': 'L',
            'ouvrir': 'O',
            'ouvre': 'O',
            'fermer': 'C',
            'stop': 'S',
            'repos': 'S'
        }
        
        for word, code in cmd_map.items():
            if word in command:
                self.ser.write(code.encode())
                print(f"Commande: {command} -> Envoyé: {code}")
                return
                
        print(f"Commande non reconnue: {command}")

    def start(self):
        """Lance le thread d'écoute"""
        Thread(target=self.listen_loop, daemon=True).start()
        
    def stop(self):
        """Arrêt propre"""
        self.running = False
        self.ser.close()

if __name__ == "__main__":
    arm = VoiceArmController()
    arm.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        arm.stop()
        print("\nContrôle arrêté")
# import serial
# import time
# import speech_recognition as sr
# # Initialisation de la communication série
# ser = serial.Serial('COM11', 9600, timeout=1)  # Remplacez COM par le port série approprié
# ser.flush()

# def listen_command():
#     """Fonction pour écouter une commande vocale et la reconnaître."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Dites 'turn right' ou 'turn left' :")
#         try:
#             audio = recognizer.listen(source, timeout=5)
#             command = recognizer.recognize_google(audio)
#             return command.lower()
#         except sr.UnknownValueError:
#             print("Commande non reconnue, essayez encore.")
#         except sr.RequestError as e:
#             print(f"Erreur avec le service de reconnaissance vocale : {e}")
#         except sr.WaitTimeoutError:
#             print("Temps d'attente écoulé.")
#         return None

# def send_to_arduino(command):
#     """Envoie la commande au microcontrôleur via la liaison série."""
#     if command == "turn right":
#         ser.write(b'R')  # Envoie 'R' pour tourner à droite
#         print("Commande envoyée : Turn Right")
#     elif command == "turn left":
#         ser.write(b'L')  # Envoie 'L' pour tourner à gauche
#         print("Commande envoyée : Turn Left")
#     else:
#         print("Commande inconnue, aucune action envoyée.")

# if __name__ == "__main__":
#     print("Contrôle du servomoteur par commande vocale")
#     time.sleep(2)  # Attente pour l'initialisation de la connexion série

#     while True:
#         command = listen_command()
#         if command:
#             send_to_arduino(command)

#         # Quitte le programme si 'exit' est entendu
#         if command == "exit":
#             print("Arrêt du programme.")
#             break