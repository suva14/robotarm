#include <HardwareSerial.h>
#include <ESP32Servo.h>

HardwareSerial SerialPort(2); // UART2 sur GPIO16 (RX), GPIO17 (TX)
Servo pince; // Exemple avec un servo

void setup() {
  Serial.begin(115200);
  SerialPort.begin(115200, SERIAL_8N1, 3, 1); // 1=RX, 1=TX
  pince.attach(21); // Broche de la pince
}

void loop() {
  // Lire les commandes de la Raspberry Pi
  if (SerialPort.available()) {
    String command = SerialPort.readStringUntil('\n');
    command.trim();
    
    if (command == "open") {
      pince.write(0);
      SerialPort.println("Pince ouverte");
    } 
    else if (command == "close") {
      pince.write(85);
      SerialPort.println("Pince fermee");
    }
  }
}