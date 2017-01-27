int race_time = 0;
int program_start_time = 0;
int brake_time = 25000;  //millis
int counts_to_stop = 35;
int tapecount = 0;

// Values range from 0 to 1023, corresponding to 0 to 5 V respectively.
int cell1
int cell2
int cell3
int cell4

String input = "";

void setBrakeTime(){
  String brakeString = "";
  int inChar = Serial.read();
  if (isDigit(inChar)) {
    // convert the incoming byte to a char
    // and add it to the string:
    brakeString += (char)inChar;
  }
  if (inChar == '\n') {
    brake_time = brakeString.toInt();
  }
}

void setStopCount(){
  String tapeString = "";
  int inCharT = Serial.read();
  if (isDigit(inCharT)) {
    // convert the incoming byte to a char
    // and add it to the string:
    tapeString += (char)inCharT;
  }
  if (inCharT == '\n') {
    counts_to_stop = tapeString.toInt();
  } 
}

void handleSerial() {

  if(Serial.available()){
    input = Serial.readStringUntil(';');
    //Serial.println(input);
  }
    if(String("tape_count").equals(input)) {
      Serial.println("Tapes: "  + String(tapecount) + " units");
    }
    if(String("reset_count").equals(input)) {
      resetCount();
    }
    if(String("brake_set").equals(input)) {
      brakeSet();
    }
    if(String("start_test").equals(input)) {
      startTest();
    }
    if(String("brake_release").equals(input)) {
      brakeRelease();
    }
    if(String("brake_state").equals(input)) {
      brakeState();
    }
    if (String("set_time").equals(input)) {
      setBrakeTime();
    }
    if (String("set_count").equals(input)) {
      setStopCount();
    }
    if(String("current").equals(input)) {
      Serial.println("Current Is: " + String(analogRead(A0)) + "counts");
    }
    if (String("read_voltages").equals(input) {
      Serial.println("voltage," + String(analogRead(A2)) + "," + String(analogRead(A3)) + "," + String(analogRead(A4)) + "," + String(analogRead(A5)));
    }
}

void resetCount(){
  tapecount = 0;
  Serial.println("Tapecount Reset: "  + String(tapecount) + " units");
  }
void startTest(){
  race_time = millis -  program_start_time;
  Serial.println("Test time started");
}
void brakeState() {
  if(digitalRead(4) && digitalRead(5)){
    Serial.println("brakes released");
  }
  else if(!digitalRead(4) && !digitalRead(5)){
    Serial.println("brakes set");
  }
  else{
    Serial.println("indeterminate: abort");
  }
}
void brakeRelease() {
  digitalWrite(4, HIGH);
  delay(100);
  digitalWrite(4, LOW);
  Serial.println("brakes released");
}
void brakeSet() {
  digitalWrite(5, HIGH);
  delay(100);
  digitalWrite(5, LOW);
  Serial.println("brakes released");
}

void setup() {
  //Setup Pins, 2 are reflection sense, 4 Solenoid On, 5 Solenoid Off
  pinMode(2,INPUT);
  pinMode(3,INPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  Serial.begin(115200);
  
  //Setup ISR for counting
  attachInterrupt(digitalPinToInterrupt(2), tapeCounter ,RISING);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  
  //Set brakes on startup
  brakeSet();

  program_start_time = millis;

if(Serial.available()){
  askForBrakeTime();
  askForStopCount();
  }
}

// ISR
void tapeCounter() {
    tapecount++;  //count total tape
}

// LOOP
void loop() {

   handleSerial();
   
  if (tapecount > 1){
    startTest();
  }

  if (tapecount > counts_to_stop ){
    brakeSet();
  }
  if (race_time > brake_time){
    brakeSet();
  }
 
}
