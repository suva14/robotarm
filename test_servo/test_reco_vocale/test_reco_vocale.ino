#include <ESP32Servo.h>

Servo base;
Servo pince;

const int servoPinBase = 16;
const int servoPinPince = 21;


// const int maxDeviation2 = 50; // Déviation maximale pour le second servomoteur
// const int stepDelay2 = 50;    // Délai entre chaque incrémentation pour le second servomoteur

int angle1 = 90; // Angle initial (neutre) pour le premier servomoteur
int angle2 = 90;
// Paramètres de mouvement
const int SPEED_DELAY = 15;
const int ANGLE_STEP = 30; // Incrément réduit pour plus de précision
void setup() {
  Serial.begin(115200);
  base.attach(servoPinBase);
  pince.attach(servoPinPince);
  base.write(angle1);
  pince.write(angle2);
}

void loop() {
 if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'R') {
      angle1 += 90;
      if (angle1 > 180) angle1 = 180;
    } else if (command == 'L') {
      angle1 -= 90;
      if (angle1 < 0) angle1 = 0;
    } else if (command == 'O') {
      angle2 -= 90;
      if (angle2 > 180) angle2 = 180;
    } else if (command == 'C') {
      angle2 += 90;
      if (angle2 < 0) angle2 = 0;
    }
    // servo1.write(angle1);
    moveServoSlowly(base, angle1);
    moveServoSlowly(pince, angle2);
    // servo2.write(angle2);
    Serial.print("Angle de la base: ");
    Serial.println(angle1);
    Serial.print("Angle de la pince: ");
    Serial.println(angle2);
  }

  delay(1000);
}
// Fonction de mouvement progressif
void moveServoSlowly(Servo &servo, int targetAngle) {
  int currentAngle = servo.read(); // Lit la position actuelle du servo
  int step = (targetAngle > currentAngle) ? 1 : -1; // Détermine la direction du mouvement

  // Boucle pour déplacer le servo degré par degré
  while (currentAngle != targetAngle) {
    currentAngle += step; // Incrémente ou décrémente l'angle
    servo.write(currentAngle); // Envoie la nouvelle position au servo
    delay(SPEED_DELAY); // Délai pour ralentir le mouvement
  }
}  
// void printPositions() {
//   Serial.print("Base:");
//   Serial.print(base.read());
//   Serial.print(" Pince:");
//   Serial.println(pince.read());
// }