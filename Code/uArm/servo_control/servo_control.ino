#include <Servo.h> 

Servo myservo;
#define SERVO_PIN (4)
String COM_ANGLE = "COM_ANGLE";
String ACK_ANGLE = "ACK_ANGLE";
int prev_pos = 0;

void setup(){
  Serial.begin(9600);
  myservo.attach(SERVO_PIN);
}

void loop(){
  if (Serial.available() > 0){  // Check if there is data available to read from the Serial port.
    String s_com = (Serial.readStringUntil("/r"));
    if(s_com == COM_ANGLE){
      Serial.println(ACK_ANGLE);
      while(1){
        if (Serial.available() > 0){  // Check if there is data available to read from the Serial port.
          String s_xval = (Serial.readStringUntil("/r"));
          int xval = s_xval.toInt();
          Serial.print("X: ");
          Serial.println(xval);

          set_servo(prev_pos, xval);
          
          delay(100);
          Serial.println(ACK_ANGLE);
          prev_pos = xval;
          break; 
        }
      }
    }
  }
}

void set_servo(int prev_pos, int new_pos){
  int pos;
  if (prev_pos > new_pos){
    for(pos = prev_pos; pos>=new_pos; pos-=1)     // goes from 180 degrees to 0 degrees 
    {                                
      myservo.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(15);                       // waits 15ms for the servo to reach the position 
    }
  }
  else if (prev_pos < new_pos){
    for(pos = prev_pos; pos<=new_pos; pos+=1)     // goes from 180 degrees to 0 degrees 
    {                                
      myservo.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(15);                       // waits 15ms for the servo to reach the position 
    }
  }
  else{
    myservo.write(new_pos);
  }
}
