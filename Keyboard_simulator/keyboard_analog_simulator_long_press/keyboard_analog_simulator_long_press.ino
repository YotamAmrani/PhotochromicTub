
#include "Keyboard.h"
#define X_RIGHT 2
#define X_LEFT 3
#define Y_FRONT 4
#define Y_BACK 5
#define FIRST_PRESS_DELAY 3

#define RED_BUTTON A0
#define BLUE_BUTTON A1
#define GREEN_BUTTON A2

#define X_AXIS_PIN A0
#define Y_AXIS_PIN A1
#define LED_CONTROL_PIN A2

#define IDLE_VALUE 445
#define LEFT_VALUE 855
#define RIGHT_VALUE 0
#define FORWARD_VALUE 855
#define BACK_VALUE 0
#define LED_ON_VALUE 0
#define NOISE 10


/** DIRECTIONS KEYS*/
const char FORWARD_KEY = 'w';
const char BACK_KEY = 's';
const char LEFT_KEY = 'a';
const char RIGHT_KEY = 'd';
const char UP_KEY = 'z';
const char DOWN_KEY = 'x';
const char LED_KEY = '1';

const char RED_KEY = 'i';
const char BLUE_KEY = 'o';
const char GREEN_KEY = 'p';

void setup() {
  Serial.begin(115200); 
  Keyboard.begin();
  pinMode(X_RIGHT, INPUT_PULLUP);
  pinMode(X_LEFT, INPUT_PULLUP);
  pinMode(Y_FRONT, INPUT_PULLUP);
  pinMode(Y_BACK, INPUT_PULLUP);
//
//  pinMode(RED_BUTTON, INPUT_PULLUP);
//  pinMode(BLUE_BUTTON, INPUT_PULLUP);
//  pinMode(GREEN_BUTTON, INPUT_PULLUP);


}
bool is_right_pressed = false;
bool is_left_pressed = false;
bool is_fornt_pressed = false;
bool is_back_pressed = false;
bool is_up_pressed = false;
bool is_down_pressed = false;
bool is_led_pressed = false;

void loop() {
    /* Move right */
     if(analogRead(X_AXIS_PIN) > (RIGHT_VALUE - NOISE) and analogRead(X_AXIS_PIN) < (RIGHT_VALUE + NOISE) and  !is_right_pressed){
        is_right_pressed = !is_right_pressed;
        Keyboard.press(RIGHT_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(analogRead(X_AXIS_PIN) > (IDLE_VALUE - NOISE) and analogRead(X_AXIS_PIN) < (IDLE_VALUE + NOISE) and is_right_pressed){
        is_right_pressed = !is_right_pressed;
        Keyboard.release(RIGHT_KEY);
      }
      
     /* move left */
     if(analogRead(X_AXIS_PIN) > (LEFT_VALUE - NOISE) and analogRead(X_AXIS_PIN) < (LEFT_VALUE + NOISE) and  !is_left_pressed){
        is_left_pressed = !is_left_pressed;
        Keyboard.press(LEFT_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(analogRead(X_AXIS_PIN) > (IDLE_VALUE - NOISE) and analogRead(X_AXIS_PIN) < (IDLE_VALUE + NOISE) and is_left_pressed){
        is_left_pressed = !is_left_pressed;
        Keyboard.release(LEFT_KEY);
      }

      /* move front */
     if(analogRead(Y_AXIS_PIN) > (FORWARD_VALUE - NOISE) and analogRead(Y_AXIS_PIN) < (FORWARD_VALUE + NOISE) and  !is_fornt_pressed){
        is_fornt_pressed = !is_fornt_pressed;
        Keyboard.press(FORWARD_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(analogRead(Y_AXIS_PIN) > (IDLE_VALUE - NOISE) and analogRead(Y_AXIS_PIN) < (IDLE_VALUE + NOISE) and is_fornt_pressed){
        is_fornt_pressed = !is_fornt_pressed;
        Keyboard.release(FORWARD_KEY);
      }

       /* move back */
     if(analogRead(Y_AXIS_PIN) > (BACK_VALUE - NOISE) and analogRead(Y_AXIS_PIN) < (BACK_VALUE + NOISE) and  !is_back_pressed){
        is_back_pressed = !is_back_pressed;
        Keyboard.press(BACK_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(analogRead(Y_AXIS_PIN) > (IDLE_VALUE - NOISE) and analogRead(Y_AXIS_PIN) < (IDLE_VALUE + NOISE) and is_back_pressed){
        is_back_pressed = !is_back_pressed;
        Keyboard.release(BACK_KEY);
      }

      /* control LED */
     if(analogRead(LED_CONTROL_PIN) > (LED_ON_VALUE - NOISE) and analogRead(LED_CONTROL_PIN) < (LED_ON_VALUE + NOISE) and  !is_led_pressed){
        is_led_pressed = !is_led_pressed;
        Keyboard.press(LED_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(analogRead(LED_CONTROL_PIN) > (IDLE_VALUE - NOISE) and analogRead(LED_CONTROL_PIN) < (IDLE_VALUE + NOISE) and is_led_pressed){
        is_led_pressed = !is_led_pressed;
        Keyboard.release(LED_KEY);
      }

       /* buttons */
//      if(digitalRead(RED_BUTTON) == LOW and !is_back_pressed){
////        Serial.println("red");
//        Keyboard.write(RED_KEY);
//        delay(300);
//      }
//      if(digitalRead(BLUE_BUTTON) == LOW and !is_back_pressed){
////        Serial.println("blue");
//        Keyboard.write(BLUE_KEY);
//        delay(300);
//      }
//      if(digitalRead(GREEN_BUTTON) == LOW and !is_back_pressed){
////        Serial.println("green");
//        Keyboard.write(GREEN_KEY);
//        delay(300);
//      }
}
