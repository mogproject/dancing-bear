// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  if (Serial.available()) {
    switch (Serial.read()) {
      // Turn off
      case '0':
        digitalWrite(LED_BUILTIN, LOW);
        break;
      // Flash
      case '1':
        digitalWrite(LED_BUILTIN, HIGH);
        delay(200);
        digitalWrite(LED_BUILTIN, LOW);
        break;
      default:
        break;
    }
  }
}

