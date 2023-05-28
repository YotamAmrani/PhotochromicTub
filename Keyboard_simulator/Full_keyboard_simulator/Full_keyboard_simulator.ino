
#include "Keyboard.h"
//#define X_RIGHT 2
//#define X_LEFT 3
//#define Y_FRONT 4
//#define Y_BACK 5
#define FIRST_PRESS_DELAY 3

#define RED_BUTTON 7
#define BLUE_BUTTON 6
#define GREEN_BUTTON 5

#define X_AXIS_PIN A0
#define Y_AXIS_PIN A1
#define Z_UP_PIN 3
#define Z_DOWN_PIN 4 

#define LED_CONTROL_PIN A2

#define IDLE_VALUE 445
#define LEFT_VALUE 855
#define RIGHT_VALUE 0
#define FORWARD_VALUE 855
#define BACK_VALUE 0
#define LED_ON_VALUE 0
#define NOISE 50


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
//  pinMode(X_RIGHT, INPUT_PULLUP);
  pinMode(LED_CONTROL_PIN, INPUT);
  pinMode(X_AXIS_PIN, INPUT);
  pinMode(Y_AXIS_PIN, INPUT);
  pinMode(Z_UP_PIN, INPUT_PULLUP);
  pinMode(Z_DOWN_PIN, INPUT_PULLUP);

  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(BLUE_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);

}
bool is_right_pressed = false;
bool is_left_pressed = false;
bool is_fornt_pressed = false;
bool is_back_pressed = false;
bool is_up_pressed = false;
bool is_down_pressed = false;
bool is_led_pressed = false;

void plottingControlInput(){
    Serial.print("X axis:");
    Serial.print(analogRead(X_AXIS_PIN));
    Serial.print(",");
    Serial.print("Y axis:");
    Serial.print(analogRead(Y_AXIS_PIN));
    Serial.print(",");
    Serial.print("Z up axis:");
    Serial.print(digitalRead(Z_UP_PIN));
    Serial.print(",");
    Serial.print("Z down axis:");
    Serial.print(digitalRead(Z_DOWN_PIN));
    Serial.print(",");
    Serial.print("red button:");
    Serial.print(digitalRead(RED_BUTTON));
    Serial.print(",");
    Serial.print("blue button:");
    Serial.print(digitalRead(BLUE_BUTTON));
    Serial.print(",");
    Serial.print("green button:");
    Serial.print(digitalRead(GREEN_BUTTON));
    Serial.print(",");
    Serial.print("led control:");
    Serial.println(analogRead(LED_CONTROL_PIN));
  }

void loop() {
//    plottingControlInput();
      /* control LED */
     if(analogRead(LED_CONTROL_PIN) > (LED_ON_VALUE - NOISE) and analogRead(LED_CONTROL_PIN) < (LED_ON_VALUE + NOISE) and  !is_led_pressed){
        Serial.println("led is on!");
        is_led_pressed = !is_led_pressed;
        Keyboard.press(LED_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(analogRead(LED_CONTROL_PIN) > (IDLE_VALUE - NOISE) and analogRead(LED_CONTROL_PIN) < (IDLE_VALUE + NOISE) and is_led_pressed){
        is_led_pressed = !is_led_pressed;
        Keyboard.release(LED_KEY);
      }


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
      /* move up */
      if(digitalRead(Z_UP_PIN) == LOW and !is_up_pressed){
        is_up_pressed = !is_up_pressed;
        Keyboard.press(UP_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(digitalRead(Z_UP_PIN) == HIGH and is_up_pressed){
        is_up_pressed = !is_up_pressed;
        Keyboard.release(UP_KEY);
      }
       /* move down */
      if(digitalRead(Z_DOWN_PIN) == LOW and !is_down_pressed){
        is_down_pressed = !is_down_pressed;
        Keyboard.press(DOWN_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(digitalRead(Z_DOWN_PIN) == HIGH and is_down_pressed){
        is_down_pressed = !is_down_pressed;
        Keyboard.release(DOWN_KEY);
      }



       /* buttons */
      if(digitalRead(RED_BUTTON) == LOW and !is_back_pressed){
        Keyboard.write(RED_KEY);
        delay(300);
      }
      if(digitalRead(BLUE_BUTTON) == LOW and !is_back_pressed){
        Keyboard.write(BLUE_KEY);
        delay(300);
      }
      if(digitalRead(GREEN_BUTTON) == LOW and !is_back_pressed){
        Keyboard.write(GREEN_KEY);
        delay(300);
      }
}
