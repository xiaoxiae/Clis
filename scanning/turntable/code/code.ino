#include <AccelStepper.h>

#define dirPin 2
#define stepPin 3
#define enablePin 4

#define motorInterfaceType 1
#define stepsPerRevolution (int)(200 * 1.02)

AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);


void enable_motor() {
  digitalWrite(enablePin, LOW);
}

void disable_motor() {
  digitalWrite(enablePin, HIGH);
}


void setup() {
  stepper.setMaxSpeed(200.0);
  stepper.setAcceleration(100.0);

  pinMode(enablePin, OUTPUT);
  disable_motor();

  Serial.begin(9600);
}

int angleToRevolutions(int angle) {
  return (int)((angle / 360.0) * stepsPerRevolution);
}

void loop() {
  if (Serial.available() > 0) {
    long angle = Serial.readString().toInt();

    enable_motor();
    stepper.setCurrentPosition(0);
    stepper.runToNewPosition(angleToRevolutions(angle));
    disable_motor();

    Serial.println(angle, DEC);
  }
}
