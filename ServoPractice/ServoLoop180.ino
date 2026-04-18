#include <Servo.h>

Servo myservo;

void setup() {
  // put your setup code here, to run once:
  myservo.attach(3,500,2500);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int deg = 0; deg <= 180; deg++){
    myservo.write(deg);
    delay(20);
  }

  for(int deg = 180; deg >= 0; deg--){
    myservo.write(deg);
    delay(20);
  }

}
