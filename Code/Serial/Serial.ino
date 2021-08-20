String COM_X = "COM_X";
String COM_Y = "COM_Y";
String COM_Z = "COM_Z";
String ACK_X = "ACK_X";
String ACK_Y = "ACK_Y";
String ACK_Z = "ACK_Z";

void setup(){
  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0){  // Check if there is data available to read from the Serial port.
    String s_com = (Serial.readStringUntil("/r"));
    if(s_com == COM_X){
      Serial.println(ACK_X);
      while(1){
        if (Serial.available() > 0){  // Check if there is data available to read from the Serial port.
          String s_xval = (Serial.readStringUntil("/r"));
          int xval = s_xval.toInt();
          Serial.print("X: ");
          Serial.println(xval);
          delay(100);
          Serial.println(ACK_X);
          break; 
        }
      }
    }
    if (s_com == COM_Y){
      Serial.println(ACK_Y);
      while(1){
        if (Serial.available() > 0){  // Check if there is data available to read from the Serial port.
          String s_yval = (Serial.readStringUntil("/r"));
          int yval = s_yval.toInt();
          Serial.print("Y: ");
          Serial.println(yval);
          delay(100);
          Serial.println(ACK_Y);
          break; 
        }
      }
    }
    if (s_com == COM_Z){
      Serial.println(ACK_Z);
      while(1){
        if (Serial.available() > 0){  // Check if there is data available to read from the Serial port.
          String s_zval = (Serial.readStringUntil("/r"));
          int zval = s_zval.toInt();
          Serial.print("Z: ");
          Serial.println(zval);
          delay(100);
          Serial.println(ACK_Z);
          break; 
        }
      }
    }
  }
}
