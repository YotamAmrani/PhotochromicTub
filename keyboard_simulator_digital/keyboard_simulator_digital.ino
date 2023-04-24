
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

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); 
  Keyboard.begin();
  Serial.println("Initializing Setup..."); 
  pinMode(X_RIGHT, INPUT_PULLUP);
  pinMode(X_LEFT, INPUT_PULLUP);
  pinMode(Y_FRONT, INPUT_PULLUP);
  pinMode(Y_BACK, INPUT_PULLUP);

}


void loop() {
     if(digitalRead(X_RIGHT) == LOW){
        Keyboard.press(RIGHT_KEY);
        Keyboard.releaseAll();
      }
    else if(digitalRead(X_LEFT) == LOW){
      Keyboard.press(LEFT_KEY);
      Keyboard.releaseAll();
      }
    if(digitalRead(Y_FRONT) == LOW){
        Keyboard.press(FORWARD_KEY);
        Keyboard.releaseAll();
      }
    else if(digitalRead(Y_BACK) == LOW){
      Keyboard.press(BACK_KEY);
      Keyboard.releaseAll();
      }
    else{
     Keyboard.releaseAll();
     Serial.flush();
    }
    delay(2);
}
