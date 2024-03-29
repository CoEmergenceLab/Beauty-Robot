/***************************************************************************************************
 * This code is for the Beauty project
 * Phylum Collective
 * http://phylum.org
 * 
 * It does three things:
 * 1. Sends commands to a motor driver (Big Easy Driver) attached to a stepper motor that controls a
 * linear actuator serving as a syringe pump to extract and dispense attracts and repellents onto a
 * petri dish containing pattern-forming bacteria.
 * 2. Lights the plate using an Adafruit DotStar LED strip.
 * 3. Controls a servo motor attached to for jig for working with multiple plates at conce (used 
 * for data collection only, not live installation).
 * 
 * The Arduino microconoller that controls these three elements recieves commands from a Python
 * script that also: (1) interfaces with a uArm Swift Pro robotic arm that postions a pipette to
 * collect the attractants/repellents, (2) collects live images of the plates from camera an sends
 * them to a deep reinforcement learning model that (3) determines the actions that the arm will
 * take (i.e. which attractant/repellent to drop and where to drop it).
 * 
 * This code is intended for an Arduino Uno but can work with most other Arduino microcontrollers
 * 
 * created September 13, 2021
 * by Carlos Castellanos

****************************************************************************************************/

#include <SPI.h>
#include <Adafruit_DotStar.h>
#include <Servo.h>


/******************************
MOTOR DRIVERS FOR SYRINGE PUMPS
******************************/
// Serial commands:
// Set serial baud rate to 19200 and terminate commands with newlines.
// Send a number, e.g. "100", to set bolus size.
// Send a "+" to push that size bolus.
// Send a "-" to pull that size bolus.
// Two syringe pumps are being used: 
// one for dropping attractants/repellents in the bacterial cultures
// and one for dispensing a bioremediating solution into a contaminated soil sampole

/* -- Constants -- */
#define SYRINGE_VOLUME_ML 1.0
#define SYRINGE_BARREL_LENGTH_MM 80.0 // mm

#define THREADED_ROD_PITCH 2 // mm
#define THREADED_ROD_PITCH_SOIL 1.25
#define STEPS_PER_REVOLUTION 200.0
#define MICROSTEPS_PER_STEP 16.0

#define SPEED_MICROSECONDS_DELAY 500 // longer delay = lower speed

static const long ustepsPerMM = MICROSTEPS_PER_STEP * STEPS_PER_REVOLUTION / THREADED_ROD_PITCH;
static const long ustepsPerML = (MICROSTEPS_PER_STEP * STEPS_PER_REVOLUTION * SYRINGE_BARREL_LENGTH_MM) / (SYRINGE_VOLUME_ML * THREADED_ROD_PITCH);
static const long ustepsPerMM_SOIL = MICROSTEPS_PER_STEP * STEPS_PER_REVOLUTION / THREADED_ROD_PITCH_SOIL;
static const long ustepsPerML_SOIL = (MICROSTEPS_PER_STEP * STEPS_PER_REVOLUTION * SYRINGE_BARREL_LENGTH_MM) / (SYRINGE_VOLUME_ML * THREADED_ROD_PITCH_SOIL);

/* -- Pin definitions -- */
static const uint8_t motorDirPin = 2;
static const uint8_t motorStepPin = 3;
static const uint8_t driverSleepPin = 4;
static const uint8_t motorDirPinSoil = 5;
static const uint8_t motorStepPinSoil = 6;
static const uint8_t driverSleepPinSoil = 7;

/* -- Enums and constants -- */
enum{PUSH,PULL}; // syringe movement direction

//static const int mLBolusStepsLength = 9;
static const float mLBolusSteps[9] = {0.001, 0.002, 0.0025, 0.003, 0.0035, 0.004, 0.045, 0.005, 0.010};
//static const float mLBolusSteps[9] = {0.010, 0.025, 0.050, 0.100, 0.250, 0.500, 1.000, 5.000, 10.000};

/* -- Default Parameters -- */
float mLBolus = 0.005; // default bolus size (in mL)
float mLBigBolus = 0.010; // default large bolus size (in mL)
float mLUsed = 0.0;
uint8_t mLBolusStepIdx = 0; // 0.001mL (1uL) increments at first
float mLBolusStep = mLBolusSteps[mLBolusStepIdx];

long stepperPos = 0; // in microsteps
char charBuf[16];

bool SOIL_STEPPER = false; // flag for soil stepper use


/*******************
ADAFRUIT DOTSTAR LED
*******************/
#define NUMPIXELS 39

// Here's how to control the LEDs from any two pins:
// The below code is for software SPI on pins 8 & 9
//#define DATAPIN    8
//#define CLOCKPIN   9
/*Adafruit_DotStar strip = Adafruit_DotStar(
  NUMPIXELS, DATAPIN, CLOCKPIN, DOTSTAR_BRG);*/
// The last parameter is optional -- this is the color data order of the
// DotStar strip, which has changed over time in different production runs.
// Your code just uses R,G,B colors, the library then reassigns as needed.
// Default is DOTSTAR_BRG, which apprently doesn't work with the latest
// production runs. DOTSTAR_BGR worked for me.

// Hardware SPI is a little faster, but must be wired to specific pins
// (Arduino Uno & Pro/Pro Mini = pin 11 for data, 13 for clock, other boards are different).
// And that's what we're doing!
Adafruit_DotStar strip = Adafruit_DotStar(NUMPIXELS, DOTSTAR_BGR);
uint32_t color = 0xFFFFFF;


/***********
SERVO MOTOR
***********/
static const uint8_t servoPin = 9;
int servoPrevPos = 0;
Servo myServo;
bool TRAINING_MODE = false; // default to training mode off (no servo)
bool SERVO_CONTROL = false; // if training mode = true we need a flag to determine when to receive angles for the servo


/*******************
SERIAL COMMUNICATION
*******************/
// == serial == //
String serialStr = "";
boolean serialStrReady = false;

// == commands == //
/*
 * "+" = push syinge pump
 * "-" = pull syinge pump
 * "S" = put stepper driver in sleep mode
 * "s" = take stepper driver out of sleep mode
 * "T" = turn on training mode (use servo)
 * "t" = turn off training mode
 * "V" = servo control on
 * "v" = servo control off
 * "L" = soil stepper control on
 * "l" = soil stepper control off
 * "COM" = receive request to establish serial communication (optional)
 * "ACK" = send back acknowledgment (optional)
 */
const char COM[] = "COM";
const char ACK[] = "ACK\n";
const char invalid[] = "Invalid command: [";
const char invalid1[] = "]\n";

void setup() {
  // Stepper Motor Setup
  pinMode(motorDirPin, OUTPUT);
  pinMode(motorStepPin, OUTPUT);
  pinMode(driverSleepPin, OUTPUT);
  digitalWrite(driverSleepPin, HIGH);        // make sure stepper driver is awake to start

  // Stepper Motor Setup (soil)
  pinMode(motorDirPinSoil, OUTPUT);
  pinMode(motorStepPinSoil, OUTPUT);
  pinMode(driverSleepPinSoil, OUTPUT);
  digitalWrite(driverSleepPinSoil, HIGH);    // make sure stepper driver is awake to start

  // servo motor
  myServo.attach(servoPin);
  
  Serial.begin(19200);                      // enable the hardware serial port

  Serial.println(F("Syringe pump(s) ready!"));
  Serial.println(F("Servo ready!"));

  // initialize DotStar LEDs
  strip.begin();                            // Initialize LED pins for output
  strip.clear();                            // Set all pixel data to zero
  strip.show();                             // Turn all LEDs off ASAP

  delay(10);
  // set the color and turn on the LEDs
  for (int i=0; i < NUMPIXELS; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
  delay(10);
  Serial.println(F("DotStar LEDs ready!"));

}

void loop() {
  //check serial port for new commands
  readSerial();
  if(serialStrReady) {
    processSerial();
  }
  delay(1);
}

void readSerial() {
  // pulls in characters from serial port as they arrive
  // builds serialStr and sets ready flag when newline is found
  while (Serial.available()) {
    char inChar = (char)Serial.read(); 
    if (inChar == '\n') {
      serialStrReady = true;
    } else {
      serialStr += inChar;
    }
  }
}

void processSerial(){
  // process serial commands as they are read in
  int num = serialStr.toInt();
  
  if(serialStr.equals(F("+"))) {
    bolus(PUSH, SOIL_STEPPER);
  } else if(serialStr.equals(F("-"))) {
    bolus(PULL, SOIL_STEPPER);
  } else if(serialStr.equals(F("S"))) {
    digitalWrite(driverSleepPin, LOW); // put stepper driver to sleep
    digitalWrite(driverSleepPinSoil, LOW); // put stepper driver to sleep (soil)
  } else if(serialStr.equals(F("s"))) {
    digitalWrite(driverSleepPin, HIGH); // take stepper driver out of sleep mode
    digitalWrite(driverSleepPinSoil, HIGH); // take stepper driver out of sleep mode (soil)
    delay(1);
  } else if(serialStr.equals(F("V")) && TRAINING_MODE == true) {
    SERVO_CONTROL = true;
  } else if(serialStr.equals(F("v"))) {
    SERVO_CONTROL = false;
  } else if(serialStr.equals(F("T"))) {
    TRAINING_MODE = true;
    SOIL_STEPPER = false; // not using soil stepper during training
  } else if(serialStr.equals(F("t"))) {
    TRAINING_MODE = false;
    SERVO_CONTROL = false;
  } else if(serialStr.equals(F("L"))) {
    SOIL_STEPPER = true; // soil stepper control on
  } else if(serialStr.equals(F("l"))) {
    SOIL_STEPPER = false; // soil stepper control off
  } else if(serialStr == (String(num))) { // it's a number
    if(SERVO_CONTROL) {
      setServo(servoPrevPos, num);
      servoPrevPos = num;
    } else {
      mLBolus = num / 1000.0; // convert from micro to milli
    }
  } else if(serialStr.equals(F("COM"))) { // establish communication (optional)
    Serial.write(ACK); 
  } else {
    Serial.write(invalid); 
    char buf[40];
    serialStr.toCharArray(buf, 40);
    Serial.write(buf);
    Serial.write(invalid1); 
  }
  
  serialStrReady = false;
  serialStr = "";
}

/* -- MOVE STEPPER(S) -- */
void bolus(int direction, bool soilStepper) {
  // Will not return until stepper is done moving.

  if(soilStepper) {
    // -- soil stepper -- //
    // change units to steps
    long steps = mLBolus * ustepsPerML_SOIL;
    if(direction == PUSH) {
      digitalWrite(motorDirPinSoil, HIGH);
      steps = mLBolus * ustepsPerML_SOIL;
      mLUsed += mLBolus; // increment how much we've used
    } else if(direction == PULL) {
      digitalWrite(motorDirPinSoil, LOW);
      if((mLUsed-mLBolus) > 0) {
        mLUsed -= mLBolus;
      } else {
        mLUsed = 0;
      }
    }
    
    // extract or dispense solution
    for(unsigned long i=0; i < steps; i++){ 
      digitalWrite(motorStepPinSoil, HIGH); 
      delayMicroseconds(SPEED_MICROSECONDS_DELAY); 
  
      digitalWrite(motorStepPinSoil, LOW); 
      delayMicroseconds(SPEED_MICROSECONDS_DELAY); 
    }
  } else {
    // -- main (attractants/repellents) stepper -- //
    // change units to steps
    long steps = mLBolus * ustepsPerML;
    if(direction == PUSH) {
      digitalWrite(motorDirPin, HIGH);
      steps = mLBolus * ustepsPerML;
      mLUsed += mLBolus; // increment how much we've used
    } else if(direction == PULL) {
      digitalWrite(motorDirPin, LOW);
      if((mLUsed-mLBolus) > 0) {
        mLUsed -= mLBolus;
      } else {
        mLUsed = 0;
      }
    }
   
    // extract or dispense solution
    for(unsigned long i=0; i < steps; i++){ 
      digitalWrite(motorStepPin, HIGH); 
      delayMicroseconds(SPEED_MICROSECONDS_DELAY); 
  
      digitalWrite(motorStepPin, LOW); 
      delayMicroseconds(SPEED_MICROSECONDS_DELAY); 
    }
  }
}

/* -- MOVE SERVO -- */
void setServo(int prevPos, int newPos) {
//  int pos;
//  if (prevPos > newPos){
//    for(pos=prevPos; pos>=newPos; pos-=1) {      // goes from 180 degrees to 0 degrees                              
//      myServo.write(pos);                       // tell servo to go to position in variable 'pos' 
//      delay(15);                                // waits 15ms for the servo to reach the position 
//    }
//  } else if(prevPos < newPos){
//    for(pos=prevPos; pos<=newPos; pos+=1) {     // goes from 180 degrees to 0 degrees                                
//      myServo.write(pos);                      // tell servo to go to position in variable 'pos' 
//      delay(15);                               // waits 15ms for the servo to reach the position 
//    }
//  } else {
//    myServo.write(newPos);
//  }


  myServo.write(120);
  delay(1000);
  myServo.write(90);
  delay(1000);
  myServo.write(60);
  delay(1000);
  myServo.write(90);
    

}
