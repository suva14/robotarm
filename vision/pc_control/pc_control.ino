#include <ESP32Servo.h>

Servo base_servo;
int current_angle = 90; // Position centrale
const int BAUD_RATE = 115200;
const int SERVO_PIN = 16; // GPIO16

void setup() {
  Serial.begin(BAUD_RATE);
  base_servo.attach(SERVO_PIN);
  base_servo.write(current_angle);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd == "LEFT" && current_angle > 0) {
      current_angle -= 10;
    } else if (cmd == "RIGHT" && current_angle < 180) {
      current_angle += 10;
    } else if (cmd == "STOP") {
      current_angle = 90;
    }

    current_angle = constrain(current_angle, 0, 180);
    base_servo.write(current_angle);
    Serial.print("New angle: ");
    Serial.println(current_angle);
    delay(50);
  }
}