#include <ESP32Servo.h>

// Déclaration des objets Servo
Servo base;
Servo servo1;
Servo servo2;
Servo servo3;
Servo cou;
Servo pince;

// Définition des broches GPIO pour chaque servo
const int servoPinBase = 16;
const int servoPin1 = 14;
const int servoPin2 = 17;
const int servoPin3 = 18;
const int servoPinCou = 27;
const int servoPinPince = 21; // Pince

// Paramètres de vitesse et de pause
const int SPEED_DELAY = 15; // Délai entre chaque degré (en ms)
const int PAUSE_AFTER_MOVE = 500; // Pause après chaque mouvement (en ms)

void setup() {
  // Attache chaque servomoteur à son pin respectif avec un délai pour éviter les surtensions
  base.attach(servoPinBase);
  delay(50);
  servo1.attach(servoPin1);
  delay(50);
  servo2.attach(servoPin2);
  delay(50);
  servo3.attach(servoPin3);
  delay(50);
  cou.attach(servoPinCou);
  delay(50);
  pince.attach(servoPinPince);

  // Initialisation des positions des servomoteurs
  base.write(90);       // Base à 90°
  servo1.write(125);    // Servo1 à 125° (-90° vers l'avant)
  servo2.write(120);    // Servo2 à 120° (+90°)
  servo3.write(60);     // Servo3 à 60° (-90°)
  cou.write(90);        // Cou à 90°
  pince.write(85);      // Pince à 85°
}

void loop() {
  // Séquence de la base
  moveServoSlowly(base, 30);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(base, 150);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(base, 90);
  delay(PAUSE_AFTER_MOVE);

  // Séquence servo1
  moveServoSlowly(servo1, 140);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(servo1, 85);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(servo1, 125);
  delay(PAUSE_AFTER_MOVE);

  // Séquence servo2
  moveServoSlowly(servo2, 80);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(servo2, 150);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(servo2, 120);
  delay(PAUSE_AFTER_MOVE);

  // Séquence servo3
  moveServoSlowly(servo3, 0);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(servo3, 120);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(servo3, 60);
  delay(PAUSE_AFTER_MOVE);

  // Séquence du cou
  moveServoSlowly(cou, 0);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(cou, 180);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(cou, 90);
  delay(PAUSE_AFTER_MOVE);

  // Séquence pince
  moveServoSlowly(pince, 0);
  delay(PAUSE_AFTER_MOVE);
  moveServoSlowly(pince, 85);
  delay(PAUSE_AFTER_MOVE);

  // Pause finale avant de recommencer le cycle
  delay(3000);
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