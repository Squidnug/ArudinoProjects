// C++ code
//

int whiteLED1 = 12;
int redLED = 11;
int yellowLED = 10;
int greenLED = 9;
int whiteLED2 = 8;

int button1 = 7;
int button2 = 13;

bool buttonPressed = 0;


void setup()
{
  pinMode(whiteLED1, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(whiteLED2, OUTPUT);
  
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  randomSeed(analogRead(A0));
}

void loop() {
  digitalWrite(greenLED, HIGH);
  delay(1000);
  digitalWrite(greenLED, LOW);

  digitalWrite(yellowLED, HIGH);
  delay(1000);
  digitalWrite(yellowLED, LOW);

  digitalWrite(redLED, HIGH);
  delay(random(1000,5001));
  digitalWrite(redLED, LOW);

  while (buttonPressed == 0) {
    digitalWrite(whiteLED1, HIGH);
    digitalWrite(whiteLED2, HIGH);
    
    if (digitalRead(button1) == 0) {
      buttonPressed = 1;
      digitalWrite(whiteLED2, LOW);
    } else if (digitalRead(button2) == 0){
      buttonPressed = 1;
      digitalWrite(whiteLED1, LOW);
    }
  }
  delay(1500);
  digitalWrite(whiteLED1, LOW);
  digitalWrite(whiteLED2, LOW);
  buttonPressed = 0;
}
