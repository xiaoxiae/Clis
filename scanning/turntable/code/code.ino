#include <AccelStepper.h>
#define dirPin 2
#define stepPin 3
#define motorInterfaceType 1
// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);
void setup() {
  // Set the maximum speed in steps per second:
  stepper.setMaxSpeed(1000);
}
void loop() {
  // Set the speed in steps per second:
  stepper.setSpeed(400);
  // Step the motor with a constant speed as set by setSpeed():
  stepper.runSpeed();
}
/*
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
*/
