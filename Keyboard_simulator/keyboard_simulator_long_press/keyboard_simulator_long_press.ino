
#include "Keyboard.h"
#define X_RIGHT 2
#define X_LEFT 3
#define Y_FRONT 4
#define Y_BACK 5
#define FIRST_PRESS_DELAY 3

#define RED_BUTTON A0
#define BLUE_BUTTON A1
#define GREEN_BUTTON A2


/** DIRECTIONS KEYS*/
const char FORWARD_KEY = 'w';
const char BACK_KEY = 's';
const char LEFT_KEY = 'a';
const char RIGHT_KEY = 'd';
const char UP_KEY = 'z';
const char DOWN_KEY = 'x';

const char RED_KEY = 'i';
const char BLUE_KEY = 'o';
const char GREEN_KEY = 'p';

void setup() {
//  Serial.begin(115200); 
  Keyboard.begin();
  pinMode(X_RIGHT, INPUT_PULLUP);
  pinMode(X_LEFT, INPUT_PULLUP);
  pinMode(Y_FRONT, INPUT_PULLUP);
  pinMode(Y_BACK, INPUT_PULLUP);

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

void loop() {
    /* Move right */
     if(digitalRead(X_RIGHT) == LOW and !is_right_pressed){
        is_right_pressed = !is_right_pressed;
        Keyboard.press(RIGHT_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(digitalRead(X_RIGHT) == HIGH and is_right_pressed){
        is_right_pressed = !is_right_pressed;
        Keyboard.release(RIGHT_KEY);
        Serial.println("right");
      }
      
      /* move left */
      if(digitalRead(X_LEFT) == LOW and !is_left_pressed){
        is_left_pressed = !is_left_pressed;
        Keyboard.press(LEFT_KEY);
        delay(FIRST_PRESS_DELAY);
      }
     else if(digitalRead(X_LEFT) == HIGH and is_left_pressed){
        is_left_pressed = !is_left_pressed;
        Keyboard.release(LEFT_KEY);
        Serial.println("left");
      }

      /* move front */
      if(digitalRead(Y_FRONT) == LOW and !is_fornt_pressed){
        is_fornt_pressed = !is_fornt_pressed;
        Keyboard.press(FORWARD_KEY);
        delay(FIRST_PRESS_DELAY);
        Serial.println("front");
      }
     else if(digitalRead(Y_FRONT) == HIGH and is_fornt_pressed){
        is_fornt_pressed = !is_fornt_pressed;
        Keyboard.release(FORWARD_KEY);
      }

       /* move back */
      if(digitalRead(Y_BACK) == LOW and !is_back_pressed){
        is_back_pressed = !is_back_pressed;
        Keyboard.press(BACK_KEY);
        delay(FIRST_PRESS_DELAY);
        Serial.println("back");
      }
     else if(digitalRead(Y_BACK) == HIGH and is_back_pressed){
        is_back_pressed = !is_back_pressed;
        Keyboard.release(BACK_KEY);
        
      }

       /* buttons */
      if(digitalRead(RED_BUTTON) == LOW and !is_back_pressed){
//        Serial.println("red");
        Keyboard.write(RED_KEY);
        delay(300);
      }
      if(digitalRead(BLUE_BUTTON) == LOW and !is_back_pressed){
//        Serial.println("blue");
        Keyboard.write(BLUE_KEY);
        delay(300);
      }
      if(digitalRead(GREEN_BUTTON) == LOW and !is_back_pressed){
//        Serial.println("green");
        Keyboard.write(GREEN_KEY);
        delay(300);
      }
}
