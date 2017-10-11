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
  unsigned long currentMillis = millis();

  // catch signal
  if (Serial.available() >= 2) {
    // read serial input
    byte x = Serial.read();
    byte y = Serial.read();

    // stop working if the first byte is zero
    if (x == 0) {
      intervalMillis = 0;
      return;
    }

    // update variables
    previousMillis = currentMillis;
    intervalMillis = (60L * 1000) / (unsigned long)x;
    numBeats = (int)y;
    currentBeat = 0;

    flash_beat(true);
  } else if (intervalMillis == 0) {
    digitalWrite(LED_BUILTIN, LOW);
    return; 
  } else {
    if (currentMillis - previousMillis >= intervalMillis) {
      previousMillis += intervalMillis;
      currentBeat = (currentBeat + 1) % numBeats;
      flash_beat(currentBeat == 0);
    }
  }
}

void flash_beat(bool is_major) {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(is_major ? 300 : 150);
  digitalWrite(LED_BUILTIN, LOW);
}
