// define pins
#define BLUE 3
#define GREEN 5
#define RED 6

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
}


// variables
unsigned long previous_millis = 0;
unsigned long interval_millis = 0;
int num_beats = 4;
int current_beat = 0;


// the loop function runs over and over again forever
void loop() {
  unsigned long current_millis = millis();

  // catch signal
  if (Serial.available() >= 2) {
    // read serial input
    byte x = Serial.read();
    byte y = Serial.read();

    // stop working if the first byte is zero
    if (x == 0) {
      interval_millis = 0;
      stop_beat();
      return;
    }

    // update variables
    previous_millis = current_millis;
    interval_millis = (60L * 1000) / (unsigned long)x;
    num_beats = (int)y;
    current_beat = 0;

    flash_beat(true);
  } else if (interval_millis != 0 && current_millis - previous_millis >= interval_millis) {
    previous_millis += interval_millis;
    current_beat = (current_beat + 1) % num_beats;
    flash_beat(current_beat == 0);
  }
}

void flash_beat(bool is_downbeat) {
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(is_downbeat ? RED : BLUE, HIGH);
  delay(is_downbeat ? 200 : 150);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(is_downbeat ? RED : BLUE, LOW);
}

void stop_beat() {
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
}
