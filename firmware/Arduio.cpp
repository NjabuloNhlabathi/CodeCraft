#include <Servo.h>

// Pin definitions matching your wiring
const int ledPin = 13;
const int trigPin = 6;  
const int echoPin = 7;  
const int gasPin = A0;  

Servo myServo;  

long duration;
int distance;
int gasValue;

// Threshold for gas detection (adjust if needed)
const int gasThreshold = 300; 

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(gasPin, INPUT);
  
  myServo.attach(8);    
  Serial.begin(9600);   
}

// Function to measure distance quickly
int getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long dur = pulseIn(echoPin, HIGH);
  return dur * 0.034 / 2;
}

void loop() {
  // Read both sensors
  distance = getDistance();
  gasValue = analogRead(gasPin);

  // Print values to Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" cm | Gas Level: ");
  Serial.println(gasValue);

  // Safety Check: Stop if object is 10cm or closer OR gas is detected
  bool hazardDetected = (distance > 0 && distance <= 10) || (gasValue > gasThreshold);

  if (hazardDetected) {
    // Stop movement and turn off LED if a hazard is present
    digitalWrite(ledPin, LOW);
    myServo.write(90);  
  } else {
    // Run normal sequence with quick safety checks in between steps
    
    digitalWrite(ledPin, HIGH); 
    myServo.write(0);
    delay(500);
    if ((getDistance() > 0 && getDistance() <= 10) || (analogRead(gasPin) > gasThreshold)) return;

    digitalWrite(ledPin, LOW); 
    myServo.write(90);
    delay(500);
    if ((getDistance() > 0 && getDistance() <= 10) || (analogRead(gasPin) > gasThreshold)) return;

    digitalWrite(ledPin, HIGH); 
    myServo.write(180);
    delay(500);
    if ((getDistance() > 0 && getDistance() <= 10) || (analogRead(gasPin) > gasThreshold)) return;

    digitalWrite(ledPin, LOW); 
    myServo.write(90);
    delay(500);
  }
}