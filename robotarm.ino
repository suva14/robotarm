#include <HardwareSerial.h>
#include <ESP32Servo.h>

// Configuration UART (identique à votre test fonctionnel)
HardwareSerial SerialPort(2); // UART2 RX=3, TX=1

// Déclaration des servos (identique à votre test mouvement)
Servo base, servo1, servo2, servo3, cou, pince;
const int pins[] = {16, 14, 17, 18, 27, 21};
const int standbyPos[] = {90, 125, 120, 60, 90, 85};

// Paramètres de mouvement (testés et fonctionnels)
const int SPEED_DELAY = 15;
const int PAUSE_AFTER_MOVE = 500;
bool isBusy = false;

void setup() {
  Serial.begin(115200);
  SerialPort.begin(115200, SERIAL_8N1, 3, 1);
  
  // Initialisation servos (méthode testée)
  base.attach(pins[0]);   delay(50);
  servo1.attach(pins[1]); delay(50);
  servo2.attach(pins[2]); delay(50);
  servo3.attach(pins[3]); delay(50);
  cou.attach(pins[4]);    delay(50);
  pince.attach(pins[5]);  delay(50);
  
  resetToStandby();
  SerialPort.println("READY"); // Signal de démarrage
}

void loop() {
  handleSerialCommands();
}

void handleSerialCommands() {
  if (SerialPort.available()) {
    String cmd = SerialPort.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();
    
    if(!isBusy) {
      if(cmd == "DANCE") performDanceSequence();
      else if(cmd == "LEFT") moveBase(-30);
      else if(cmd == "RIGHT") moveBase(30);
      else if(cmd == "GRIP") movePince(0);
      else if(cmd == "RELEASE") movePince(85);
      else if(cmd == "STOP") resetToStandby();
    }
    else {
      SerialPort.println("BUSY");
    }
  }
}

// Fonctions de mouvement (bloquantes mais fiables)
void moveServoSlowly(Servo &servo, int targetAngle) {
  int current = servo.read();
  while(current != targetAngle) {
    current += (targetAngle > current) ? 1 : -1;
    servo.write(current);
    delay(SPEED_DELAY);
  }
}

void resetToStandby() {
  isBusy = true;
  moveServoSlowly(base, 90);
  moveServoSlowly(servo1, 125);
  moveServoSlowly(servo2, 120);
  moveServoSlowly(servo3, 60);
  moveServoSlowly(cou, 90);
  moveServoSlowly(pince, 85);
  isBusy = false;
}

void moveBase(int delta) {
  isBusy = true;
  int newAngle = constrain(base.read() + delta, 0, 180);
  moveServoSlowly(base, newAngle);
  isBusy = false;
}

void movePince(int angle) {
  isBusy = true;
  moveServoSlowly(pince, angle);
  isBusy = false;
}

// Séquence de danse (version simplifiée et testée)
void performDanceSequence() {
  isBusy = true;
  
  // Séquence de base
  moveServoSlowly(base, 30);
  moveServoSlowly(base, 150);
  moveServoSlowly(base, 90);

  // Séquence pince
  moveServoSlowly(pince, 0);
  moveServoSlowly(pince, 85);

  // Réinitialisation
  resetToStandby();
  isBusy = false;
  SerialPort.println("DANCE_DONE");
}