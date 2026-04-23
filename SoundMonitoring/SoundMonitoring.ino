int soundPin = A0;
int ledPin = 9;
int base = 204;

const int numSamples = 10;
int samples[numSamples];
int index = 0;
int total = 0;
int average = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

  for (int i = 0; i < numSamples; i++){
    samples[i] = 0;
  }
}

void loop() {
  int soundValue = analogRead(soundPin);
  int amplitude = abs(soundValue - base);

  total = total - samples[index];
  samples[index] = amplitude;
  total = total + samples[index];
  index++;
  if(index >= numSamples){
    index = 0;
  }

  average = total / numSamples;
  
  amplitude = round(average);

  int brightness = map(amplitude, 0, 50, 0, 255);
  brightness = constrain(brightness, 0, 255);
  analogWrite(ledPin, brightness);

  Serial.println(amplitude);
  
  delay(50);
}
