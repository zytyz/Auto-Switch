#include "Time.h"

//laser and sensor//
int Detector1 = 7;
int Detector2 = 13;

//value//
int counter = 0;
int value; 

//state//
int state;
const int nobody = 0;
const int ready_enter = 1;
const int ready_escape = 2;
const int enter = 3;
const int escape = 4;

bool has_print = 0;

void get_value();


void setup(){ 
  Serial.begin (9600);
  pinMode(Detector1, INPUT);
  pinMode(Detector2, INPUT);
  state = nobody;
}

void loop(){
  get_value();
  if (state == nobody ){
    has_print = 0;
    if (value == 01) state = ready_enter;
    else if (value == 10) state = ready_escape;
    else if (value == 11) state = nobody;
  }
  else if (state == ready_enter){
    if (value == 10) {
      state = enter;
    }
    else if (value == 01) state = ready_enter;
    else if (value == 11) state = nobody;
  }
  else if (state == ready_escape){
    if (value == 01) {
      state = escape;
    }
    else if (value == 10) state = ready_escape;
    else if (value == 11) state = nobody;
  }
  else if (state == enter){
    if (value == 11) state = nobody;
    else if (value == 01) state = ready_enter;
  }
  else if (state == escape){
    if (value == 11) state = nobody;
    else if (value == 10) state = ready_escape;
  }
  
  if (value == 0) state = state;
  
  if (state == 3) {
    if (has_print == 0) {
      Serial.println('i');
      has_print = 1;
    }
  }
  else if (state == 4) {
    if (has_print == 0) {
      Serial.println('o');
      has_print = 1;
    }
  }
  delay(1000);
}  

void get_value(){
  int val1 = digitalRead(Detector1);
  int val2 = digitalRead(Detector2);
  value = 10 * val1 + val2;
}
