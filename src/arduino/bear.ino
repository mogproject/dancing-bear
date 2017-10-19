#include <Servo.h>
#include "IRremote.h"

// define pins

const int IR_RECEIVER = 11;

const int SERVO = 2;

const int BLUE = 3;
const int GREEN = 5;
const int RED = 6;

const int LED_1 = 9;
const int LED_2 = 8;

const int SERVO_MAX_ANGLE = 30;

const int BLINK_INTERVAL = 150; // in milliseconds

Servo myservo; // create servo object to control a servo

int current_bpm = 120;
unsigned long previous_blink_downbeat = 0;
unsigned long previous_blink_upbeat = 0;

IRrecv irrecv(IR_RECEIVER);     // create instance of 'irrecv'
decode_results results;      // create instance of 'decode_results'

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);

  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
  digitalWrite(LED_1, LOW);
  digitalWrite(LED_2, LOW);

  // attaches the servo on pin 9 to the servo object
  myservo.attach(SERVO);

  // IR receiver
  irrecv.enableIRIn(); 
}

// the loop function runs over and over again forever
void loop() {
  unsigned long current_millis = millis();

  // catch signal
  if (Serial.available()) {
    // read serial input
    char x = Serial.read();
    switch (x) {
      case 0: flash_beat(true, current_millis); break;
      case 1: flash_beat(false, current_millis); break;
      default: if (x > 1) current_bpm = x; break;
    }
  } else if (irrecv.decode(&results)) {
    switch (translate_ir()) {
      case 1: flash_beat(true, current_millis); break;
      case 2: flash_beat(false, current_millis); break;
//      case 7: test_speed(75); break;
      default: break;
    } 
    irrecv.resume();
  } else {
    if (previous_blink_downbeat && current_millis - previous_blink_downbeat >= BLINK_INTERVAL) stop_blink(true, current_millis);
    if (previous_blink_upbeat && current_millis - previous_blink_upbeat >= BLINK_INTERVAL) stop_blink(false, current_millis);
  }
}

void flash_beat(bool is_downbeat, unsigned long current_millis) {
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(is_downbeat ? RED : BLUE, HIGH);
  digitalWrite(is_downbeat ? LED_1 : LED_2, HIGH);
  switch_servo();
  (is_downbeat ? previous_blink_downbeat : previous_blink_upbeat) = current_millis;
}

void stop_beat() {
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
  digitalWrite(LED_1, LOW);
  digitalWrite(LED_2, LOW);
}

void stop_blink(bool is_downbeat, unsigned long current_millis) {
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(is_downbeat ? RED : BLUE, LOW);
  digitalWrite(is_downbeat ? LED_1 : LED_2, LOW);
  (is_downbeat ? previous_blink_downbeat : previous_blink_upbeat) = current_millis;
}

void switch_servo() {
  int num_steps = 4;
  int step = SERVO_MAX_ANGLE / num_steps;

  int interval = 60000 / current_bpm;
  int delay_ms = interval * 4 / 5 / (num_steps * 2);

  for (int i = 0; i < num_steps; ++i) {
    myservo.write(90 + i * step);
    delay(delay_ms);
  }
  for (int i = num_steps; i > 0; --i) {
    myservo.write(90 + i * step);
    delay(delay_ms);
  }
  myservo.write(90);
}

int translate_ir() {
  // todo control repetition
  switch(results.value) {
    case 0xFFA25D: return 64; // POWER
    case 0xFFE21D: return 65; // FUNC/STOP
    case 0xFF629D: return 66; // VOL+
    case 0xFF22DD: return 67; // FAST BACK
    case 0xFF02FD: return 68; // PAUSE
    case 0xFFC23D: return 69; // FAST FORWAR
    case 0xFFE01F: return 70; // DOWN
    case 0xFFA857: return 71; // VOL-
    case 0xFF906F: return 72; // UP
    case 0xFF9867: return 73; // EQ
    case 0xFFB04F: return 74; // ST/REPT
    case 0xFF6897: return 0; // 0
    case 0xFF30CF: return 1; // 1
    case 0xFF18E7: return 2; // 2
    case 0xFF7A85: return 3; // 3
    case 0xFF10EF: return 4; // 4
    case 0xFF38C7: return 5; // 5
    case 0xFF5AA5: return 6; // 6
    case 0xFF42BD: return 7; // 7
    case 0xFF4AB5: return 8; // 8
    case 0xFF52AD: return 9; // 9
    case 0xFFFFFFFF: return 75; // REPEAT
    default: return -1; // other button
  }
}

void test_speed(int angle) {
  for (int i = 0; i < 20; ++i) {
    myservo.write(90 - angle);
    delay(300);
    myservo.write(90 + angle);
    delay(300);
  }
}
