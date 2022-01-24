#include <AccelStepper.h>

#define dirPin1 2
#define stepPin1 3
#define enablePin1 4
#define dirPin2 5
#define stepPin2 6
#define enablePin2 7
#define dirPin3 8
#define stepPin3 9
#define enablePin3 10

#define motorInterfaceType 1
#define stepsPerRevolution (int)(200 * 1.02)

#define max_speed 150.0
#define max_acceleration 80.0
#define speed_coefficient 0.8

AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper2 = AccelStepper(motorInterfaceType, stepPin2, dirPin2);
AccelStepper stepper3 = AccelStepper(motorInterfaceType, stepPin3, dirPin3);


void enable_motor() {
  digitalWrite(enablePin1, LOW);
  digitalWrite(enablePin2, LOW);
  digitalWrite(enablePin3, LOW);
}

void disable_motor() {
  digitalWrite(enablePin1, HIGH);
  digitalWrite(enablePin2, HIGH);
  digitalWrite(enablePin3, HIGH);
}


void setup() {
  stepper1.setMaxSpeed(max_speed);
  stepper1.setAcceleration(max_acceleration);
  stepper1.setSpeed(max_speed * speed_coefficient);
  
  stepper2.setMaxSpeed(max_speed);
  stepper2.setAcceleration(max_acceleration);
  stepper2.setSpeed(max_speed * speed_coefficient);
  
  stepper3.setMaxSpeed(max_speed);
  stepper3.setAcceleration(max_acceleration);
  stepper3.setSpeed(max_speed * speed_coefficient);

  pinMode(enablePin1, OUTPUT);
  pinMode(enablePin2, OUTPUT);
  pinMode(enablePin3, OUTPUT);

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
    stepper1.setCurrentPosition(0);
    stepper1.moveTo(angleToRevolutions(angle));
    
    stepper2.setCurrentPosition(0);
    stepper2.moveTo(angleToRevolutions(angle));
    
    stepper3.setCurrentPosition(0);
    stepper3.moveTo(angleToRevolutions(angle));

    while (stepper1.distanceToGo() > 0 && stepper2.distanceToGo() > 0 && stepper3.distanceToGo() > 0) {
      stepper1.run();
      stepper2.run();
      stepper3.run();
    }
    
    disable_motor();

    Serial.println(angle, DEC);
  }
}
