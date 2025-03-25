// #include <HardwareSerial.h>
// #include <ESP32Servo.h>

// Servo base_servo;
// int base_angle = 90;  // Position centrale
// const int SPEED = 2;  // Degrés par loop

// void setup() {
//   Serial.begin(115200);
//   base_servo.attach(16);  // Broche du servo de base
//   base_servo.write(base_angle);
// }

// void loop() {
//   if (Serial.available()) {
//     String command = Serial.readStringUntil('\n');
//     command.trim();

//     if (command == "base_left" && base_angle > 0) {
//       base_angle -= SPEED;
//     } 
//     else if (command == "base_right" && base_angle < 180) {
//       base_angle += SPEED;
//     }

//     base_servo.write(base_angle);
//   }
//   delay(50);  // Contrôle fluide
// }