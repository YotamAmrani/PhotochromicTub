
#include "Keyboard.h"
#define X_RIGHT 2
#define X_LEFT 3
#define Y_FRONT 4
#define Y_BACK 5

/** DIRECTIONS KEYS*/
const char FORWARD_KEY = 'w';
const char BACK_KEY = 's';
const char LEFT_KEY = 'a';
const char RIGHT_KEY = 'd';
const char UP_KEY = 'z';
const char DOWN_KEY = 'x';

bool right_key_state = false;
unsigned int right_key_pressed_time = 0;


void setup() {
//  Serial.begin(115200); 
  Keyboard.begin();
  pinMode(X_RIGHT, INPUT_PULLUP);
  pinMode(X_LEFT, INPUT_PULLUP);
  pinMode(Y_FRONT, INPUT_PULLUP);
  pinMode(Y_BACK, INPUT_PULLUP);

}


void loop() {
     if(digitalRead(X_RIGHT) == LOW){
      if (!right_key_state){
          right_key_state = !right_key_state;
          Keyboard.write(RIGHT_KEY);
//          delay(200);
        }
       else{
        Keyboard.write(RIGHT_KEY);
//        delay(1);
        }
      }
      else{
          right_key_state = !right_key_state;
        }

      
//    else if(digitalRead(X_LEFT) == LOW){
//      Keyboard.write(LEFT_KEY);
//      }
//    if(digitalRead(Y_FRONT) == LOW){
//        Keyboard.write(FORWARD_KEY);
//      }
//    else if(digitalRead(Y_BACK) == LOW){
//      Keyboard.write(BACK_KEY);
//      }
//    else{
//     Keyboard.releaseAll();
//    }
//    delay(1);
}
