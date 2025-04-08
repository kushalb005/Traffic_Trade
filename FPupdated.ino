#include <Arduino.h>

int nsRed = 2;
int nsYellow = 4;
int nsGreen = 5;
int ewRed = 18;
int ewYellow = 19;
int ewGreen = 21;

#define RIGHT_TURN_BUFFER 5  
#define PHASE_DELAY 2000     
#define YELLOW_DURATION 1800  

void fastBlinkLED(int ledPin, int durationSeconds) {
  unsigned long startTime = millis();
  while (millis() - startTime < durationSeconds * 1000UL) {
    digitalWrite(ledPin, HIGH);
    delay(300);
    digitalWrite(ledPin, LOW);
    delay(300);
  }
}

void setup() {
  Serial.begin(9600);
  
  pinMode(nsRed, OUTPUT);
  pinMode(nsYellow, OUTPUT);
  pinMode(nsGreen, OUTPUT);
  pinMode(ewRed, OUTPUT);
  pinMode(ewYellow, OUTPUT);
  pinMode(ewGreen, OUTPUT);
  
  digitalWrite(nsRed, HIGH);
  digitalWrite(ewRed, HIGH);
  digitalWrite(nsYellow, LOW);
  digitalWrite(nsGreen, LOW);
  digitalWrite(ewYellow, LOW);
  digitalWrite(ewGreen, LOW);
  
  Serial.println("ESP32 Traffic Light System Initialized...");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    Serial.println("Received Data: " + data);
    
    int ns_time, ew_time;
    if (sscanf(data.c_str(), "%d %d", &ns_time, &ew_time) == 2) {
      Serial.printf("Parsed NS Time: %d s, EW Time: %d s\n", ns_time, ew_time);
      
      digitalWrite(nsRed, LOW);
      digitalWrite(nsYellow, HIGH);
      digitalWrite(nsGreen, LOW);
      delay(YELLOW_DURATION);
      digitalWrite(nsYellow, LOW);
      
      int ns_green_duration = ns_time - RIGHT_TURN_BUFFER - 2;
      if(ns_green_duration < 0) ns_green_duration = 0;
      digitalWrite(nsGreen, HIGH);
      delay(ns_green_duration * 1000UL);
      digitalWrite(nsGreen, LOW);

      digitalWrite(nsYellow, HIGH);
      delay(YELLOW_DURATION);
      digitalWrite(nsYellow, LOW);
      
      fastBlinkLED(nsGreen, RIGHT_TURN_BUFFER);
  
      digitalWrite(nsRed, HIGH);
      
      delay(PHASE_DELAY);
      
      digitalWrite(ewRed, LOW);
      digitalWrite(ewYellow, HIGH);
      digitalWrite(ewGreen, LOW);
      delay(YELLOW_DURATION);
      digitalWrite(ewYellow, LOW);
      
      int ew_green_duration = ew_time - RIGHT_TURN_BUFFER - 2;
      if(ew_green_duration < 0) ew_green_duration = 0;
      digitalWrite(ewGreen, HIGH);
      delay(ew_green_duration * 1000UL);
      digitalWrite(ewGreen, LOW);
      
      digitalWrite(ewYellow, HIGH);
      delay(YELLOW_DURATION);
      digitalWrite(ewYellow, LOW);
      
      fastBlinkLED(ewGreen, RIGHT_TURN_BUFFER);
      
      digitalWrite(ewRed, HIGH);
      
      delay(PHASE_DELAY);
      
      Serial.println("Cycle complete. Waiting for new data...\n");
    } else {
      Serial.println("Error: Invalid data format received!");
    }
  }
}
