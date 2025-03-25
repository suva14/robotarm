# test_api.py - À SUPPRIMER APRÈS TESTS
from openai import OpenAI
import speech_recognition as sr
import cv2

client = OpenAI(api_key="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")
# ⚠️ À NE PAS VERSIONNER - Clé temporaire pour tests

ALLOWED_COMMANDS = ["gauche", "droite", "stop", "avance", "recule"]



# Initialisation reconnaissance vocale
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def get_voice_command():
    with microphone as source:
        print("\nÉcoute... (dites une commande)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
        
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit : {text}")
            return text
        except sr.UnknownValueError:
            print("Commande non reconnue")
            return None
        except sr.RequestError:
            print("Erreur API vocale")
            return None

def get_llm_command(phrase):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Réponds UNIQUEMENT par un mot parmi {', '.join(ALLOWED_COMMANDS)}"},
            {"role": "user", "content": phrase}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()

def test_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        cv2.imshow('Test Caméra (Appuyez sur ESC pour quitter)', frame)
        if cv2.waitKey(1) == 27:  # Touche ESC
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("=== Mode Test Local ===")
    print("1. Test Caméra")
    print("2. Test Reconnaissance Vocale + OpenAI")
    print("3. Quitter")
    
    choice = input("Choisissez un mode (1/2/3): ")
    
    if choice == "1":
        test_camera()
    elif choice == "2":
        while True:
            try:
                voice_text = get_voice_command()
                if voice_text:
                    command = get_llm_command(voice_text)
                    print(f"→ Commande générée : {command}")
            except KeyboardInterrupt:
                print("\nTest terminé")
                break