unsigned long starttime = 0;     /* Timestamp, in ms, when the test started. */
unsigned long maxtime   = 25000; /* Maximum amount of time, in ms, that can elapse. */
int           maxtape   = 35;    /* Maximum number of tapes the pod is allowed to pass. */
int           numtape   = 0;     /* Number of tapes passed. */
bool          running   = false; /* Whether or not the test timer is active. */
bool          braking   = false; /* Whether or not the brakes have been activated. */

/* Read commands and data queries from the serial port. */
void handleserial() {
	String input;
	if (Serial.available()) {
		input = Serial.readStringUntil(';');
	}
	else 
		return;

	if (String("tape_count").equals(input)) {
		Serial.println("tape," + String(numtape));
	}
	else if (String("brakes_on").equals(input)) {
		setbrake();
	}
	else if (String("brakes_off").equals(input)) {
		releasebrake();
	}
	else if (String("get_brake_status").equals(input)) {
		Serial.println("brake," + String(braking));
	}
	else if (String("start_test").equals(input)) {
		starttime = millis();
		running = true;
	}
	else if (String("set_time").equals(input)) {
		maxtime = Serial.readStringUntil(';').toInt();
	}
	else if (String("set_tape").equals(input)) {
		maxtape = Serial.readStringUntil(';').toInt();
	}
	else if (String("get_time").equals(input)) {
		if (running)
			Serial.println("time," + String(millis() - starttime) + "," + String(maxtime));
		else
			Serial.println("time,0," + String(maxtime));
	}
	else if (String("stop_test").equals(input)) {
		running = false;
	}
	else if (String("get_test_status").equals(input)) {
		Serial.println("test," + String(running));
	}
	else if (String("get_voltages").equals(input)) {
		Serial.println("voltages," + String(analogRead(A2)) + "," + String(analogRead(A3)) + "," + String(analogRead(A4)) + "," + String(analogRead(A5)));
	}
}

/* Set the switch off, cutting off power from the solenoid. */
void setbrake() {
	digitalWrite(5, HIGH);
	delay(100);
	digitalWrite(5, LOW);
	braking = true;
}

/* Set the switch on, allowing power to flow through the solenoid. */
void releasebrake() {
	digitalWrite(4, HIGH);
	delay(100);
	digitalWrite(4, LOW);
	braking = false;
}

/* Increases the number of tapes passed by one. */
void tapeincrement() {
	numtape++;
}

/* Setup pin IO. Called by the board every startup. */
void setup() {

	pinMode(2, INPUT);
	pinMode(3, INPUT);
	pinMode(4, OUTPUT);
	pinMode(5, OUTPUT);

	/* Battery voltage analog pins. */
	pinMode(A2, INPUT);
	pinMode(A3, INPUT);
	pinMode(A4, INPUT);
	pinMode(A5, INPUT);
	
	Serial.begin(115200);

	/* Setup ISR for counting. */
	attachInterrupt(digitalPinToInterrupt(2), tapeincrement, RISING);
	digitalWrite(4, LOW);
	digitalWrite(5, LOW);

	starttime = millis();

}

/* Loop until power is cut off. Called continuously after setup() */
void loop() {

	handleserial();

	if (millis() - starttime > maxtime && running && !braking) {
		setbrake();
	}

	if (numtape > maxtape && !braking) {
		setbrake();
	}
}
