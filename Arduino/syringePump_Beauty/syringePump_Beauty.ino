#include <avr/pgmspace.h>
// Controls a stepper motor in a syringe pump

// Serial commands:
// Set serial baud rate to 19200 and terminate commands with newlines.
// Send a number, e.g. "100", to set bolus size.
// Send a "+" to push that size bolus.
// Send a "-" to pull that size bolus.

/* -- Constants -- */
#define SYRINGE_VOLUME_ML 1.0
#define SYRINGE_BARREL_LENGTH_MM 80.0 // mm

#define THREADED_ROD_PITCH 2 // mm
#define STEPS_PER_REVOLUTION 200.0
#define MICROSTEPS_PER_STEP 16.0

#define SPEED_MICROSECONDS_DELAY 500 //longer delay = lower speed

static const long ustepsPerMM = MICROSTEPS_PER_STEP * STEPS_PER_REVOLUTION / THREADED_ROD_PITCH;
static const long ustepsPerML = (MICROSTEPS_PER_STEP * STEPS_PER_REVOLUTION * SYRINGE_BARREL_LENGTH_MM) / (SYRINGE_VOLUME_ML * THREADED_ROD_PITCH );

/* -- Pin definitions -- */
static const uint8_t motorDirPin = 2;
static const uint8_t motorStepPin = 3;

/* -- Enums and constants -- */
enum{PUSH,PULL}; // syringe movement direction

//static const int mLBolusStepsLength = 9;
static const float mLBolusSteps[9] = {0.001, 0.002, 0.0025, 0.003, 0.0035, 0.004, 0.045, 0.005, 0.010};
//static const float mLBolusSteps[9] = {0.010, 0.025, 0.050, 0.100, 0.250, 0.500, 1.000, 5.000, 10.000};

/* -- Default Parameters -- */
float mLBolus = 0.002; // default bolus size (in mL)
float mLBigBolus = 0.010; // default large bolus size (in mL)
float mLUsed = 0.0;
uint8_t mLBolusStepIdx = 0; // 0.001mL (1uL) increments at first
float mLBolusStep = mLBolusSteps[mLBolusStepIdx];

long stepperPos = 0; //in microsteps
char charBuf[16];

//serial
String serialStr = "";
boolean serialStrReady = false;

const char invalid[] = "Invalid command: [";
const char invalid1[] = "]\n";

void setup(){
  /* Motor Setup */ 
  pinMode(motorDirPin, OUTPUT);
  pinMode(motorStepPin, OUTPUT);
  
  /* Serial setup */
  // Note that serial commands must be terminated with a newline
  // to be processed. Check this setting in your serial monitor if 
  // serial commands aren't doing anything.
  Serial.begin(19200);

  Serial.println(F("Syringe pump is ready!"));
}

void loop() {
  //check serial port for new commands
  readSerial();
	if(serialStrReady) {
		processSerial();
	}
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
	if(serialStr.equals(F("+"))) {
		bolus(PUSH);
	} else if(serialStr.equals(F("-"))) {
		bolus(PULL);
	} else if(serialStr.toInt() != 0) { // it's a number
	  int uLbolus = serialStr.toInt();
	  mLBolus = uLbolus / 1000.0; // convert from micro to milli
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

/* -- MOVE STEPPER -- */
void bolus(int direction) {
  // Will not return until stepper is done moving.
  
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

String decToString(float decNumber){
	// not a general use converter! Just good for the numbers we're working with here.
	int wholePart = decNumber; // truncate
	int decPart = round(abs(decNumber*1000)-abs(wholePart*1000)); // 3 decimal places
	String strZeros = String("");
  if(decPart < 10) {
    strZeros = String("00");
  } else if(decPart < 100) {
    strZeros = String("0");
  }
	return String(wholePart) + String('.') + strZeros + String(decPart);
}
