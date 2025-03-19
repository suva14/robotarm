#include <ESP32Servo.h>

Servo servo1;
Servo servo2;

const int servoPin1 = 18;
const int servoPin2 = 19;


const int centerAngle2 = 105; // Nouvel angle central pour le second servomoteur
const int maxDeviation2 = 50; // Déviation maximale pour le second servomoteur
const int stepDelay2 = 50;    // Délai entre chaque incrémentation pour le second servomoteur

int angle1 = 90; // Angle initial (neutre) pour le premier servomoteur

void setup() {
  Serial.begin(9600);
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo1.write(angle1);
  servo2.write(centerAngle2);
}

void loop() {
  // Contrôle du second servomoteur (aller-retour)
  for (int angle = centerAngle2; angle <= centerAngle2 + maxDeviation2; angle++) {
    servo2.write(angle);
    delay(stepDelay2);
    if (Serial.available() > 0) break; // Vérifie s'il y a une commande série
  }

  for (int angle = centerAngle2 + maxDeviation2; angle >= centerAngle2 - maxDeviation2; angle--) {
    servo2.write(angle);
    delay(stepDelay2);
    if (Serial.available() > 0) break; // Vérifie s'il y a une commande série
  }

  for (int angle = centerAngle2 - maxDeviation2; angle <= centerAngle2; angle++) {
    servo2.write(angle);
    delay(stepDelay2);
    if (Serial.available() > 0) break; // Vérifie s'il y a une commande série
  }

  // Contrôle du premier servomoteur via des commandes série
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'R') {
      angle1 += 90;
      if (angle1 > 180) angle1 = 180;
    } else if (command == 'L') {
      angle1 -= 90;
      if (angle1 < 0) angle1 = 0;
    }
    servo1.write(angle1);
    Serial.print("Angle du premier servomoteur: ");
    Serial.println(angle1);
  }

  delay(1000);
}
