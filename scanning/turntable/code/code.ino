#include <Stepper.h>

// TODO: the correct number
const int stepsPerRevolution = 200;

// TODO: correct pins
Stepper motor(stepsPerRevolution, 2, 3, 4, 5);


int angleToRevolutions(int angle) {
  return (int)((angle / 360.0) * stepsPerRevolution);
}

void setup() {
  motor.setSpeed(60);
  Serial.begin(9600);
}


void loop() {
  if (Serial.available() > 0) {
    byte angle = Serial.read();

    motor.step(angleToRevolutions(angle));
    
    Serial.println(angle, DEC);
  }
}
