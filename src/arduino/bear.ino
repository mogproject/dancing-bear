// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}


// variables
unsigned long previousMillis = 0;
unsigned long intervalMillis = 0;
int numBeats = 4;
int currentBeat = 0;


// the loop function runs over and over again forever
void loop() {
  if (intervalMillis == 0) return;
  
  unsigned long currentMillis = millis();

  // catch signal
  if (Serial.available() >= 2) {
    // read serial input
    byte x = Serial.read();
    byte y = Serial.read();

    // update variables
    previousMillis = currentMillis;
    intervalMillis = (60L * 1000) / (unsigned long)x;
    numBeats = (int)y;
    currentBeat = 0;

    flash_major_beat();
  } else {
    if (currentMillis - previousMillis >= intervalMillis) {
      previousMillis += intervalMillis;
      currentBeat = (currentBeat + 1) % numBeats;
      if (currentBeat == 0) {
        flash_major_beat();
      } else {
        flash_minor_beat();
      }
    }
  }
}

void flash_major_beat() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(300);
  digitalWrite(LED_BUILTIN, LOW);
}

void flash_minor_beat() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(150);
  digitalWrite(LED_BUILTIN, LOW);
}
