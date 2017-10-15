// define pins
const int SERVO = 2;
const int BLUE = 3;
const int GREEN = 5;
const int RED = 6;

const int latch = 9;  // 74HC595  pin 9 STCP
const int clock = 10; // 74HC595  pin 10 SHCP
const int data = 8;   // 74HC595  pin 8 DS

const int SERVO_MAX_DEGREE = 30;

#include <Servo.h>

Servo myservo; // create servo object to control a servo
bool servo_count = false;
int current_bpm = 120;

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

  // attaches the servo on pin 9 to the servo object
  myservo.attach(SERVO);

  // 4-digit display
  pinMode(latch, OUTPUT);
  pinMode(clock, OUTPUT);
  pinMode(data, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  // catch signal
  if (Serial.available()) {
    // read serial input
    char x = Serial.read();
    switch (x) {
    case 0:
      flash_beat(true);
      break;
    case 1:
      flash_beat(false);
      break;
    default:
      current_bpm = (unsigned char)x;
      display_int();
      break;
    }
  }
}

void flash_beat(bool is_downbeat) {
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(is_downbeat ? RED : BLUE, HIGH);
  delay(is_downbeat ? 200 : 150);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(is_downbeat ? RED : BLUE, LOW);
  switch_servo();
}

void stop_beat() {
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
  switch_servo();
}

void switch_servo() {
  int step = 10;
  int sign = servo_count ? -1 : 1;

  delay(max(0, 60000 / current_bpm - 300));
  for (int i = -SERVO_MAX_DEGREE; i <= SERVO_MAX_DEGREE; i += step) {
    delay(20);
    myservo.write(90 + sign * i);
  }
  servo_count = !servo_count;
}

void display_int() {
  digitalWrite(latch, LOW);
  shiftOut(data, clock, MSBFIRST, 0xff);
  digitalWrite(latch, HIGH);
}
