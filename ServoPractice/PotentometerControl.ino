#include <Servo.h>

Servo myservo;

int pot = A0;
int value;
int angle;

void setup() {
  // put your setup code here, to run once:
  myservo.attach(3);
  pinMode(pot, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  value = analogRead(pot);
  angle = map(value, 0, 1023, 0, 180);
  myservo.write(angle);
}
