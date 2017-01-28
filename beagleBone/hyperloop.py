from servo_valve import ServoValve
from nap_communication import NAP
from brake_communication import Brakes
from data_collection import Sensors
from switchctl import Switch
from duointerface import Arduino
from data_logging import SensorLogging
import Adafruit_BBIO.UART as UART
import time
import array
import thread

try:
	helpfile = 	"""\n '>' indicates the system is ready for a command
			commands are as follows:
			valve_open \t\t 	Opens the air bearing valve
			valve_close \t\t 	Close the air bearing valve 
			valve_set_open  $$$ \t 	sets the open position to $$$ (PWM counts)
			valve_set_close $$$ \t 	sets the close position to $$$ (PWM counts)
			tape_pulse_period \t 	returns the length of time the pod sensed the relflective tape (microseconds)
			position \t		returns the position of the pod from the start (feet)
			speed \t\t		returns the speed of the pod (mph)
			brake_set \t		Sets (engages) the brakes
			brake_release \t\t	Releases brake pressure (Brakes do not retract automatically!)
			read_data % \t\t	Returns the raw value of the sensor % (to see a list, 'sensor_list')
			abort       \t\t        Sets the pod status flag to signal an abort.
			ready       \t\t        Indicate the pod is ready to be pushed.
			reset_imu   \t\t        Reset IMU acceleration, velocity, position variables."""

	sensor_list = 	"""\n\t\t\tBBB_Temp \t	Temperature Sensor on the Beaglebone Black Cape
			LaserPortFwd \t	Laser Distance Sensor on the Port Forward Air Bearing
			LaserPortAft \t	Laser Distance Sensor on the Port Aft Air Bearing
			LaserStbdFwd \t	Laser Distance Sensor on the Starbord Forward Air Bearing
			LaserStbdAft \t	Laser Distance Sensor on the Starboard Aft Air Bearing
			AccumPress \t Hydraulic Pressure Transducer on the Accumulator
			CylinderPress \t Hydraulic Pressure Transducer on the Brake Cylinders
			SolenoidCurr \t Current in the Brake Solenoid Valves"""			

	nap = NAP(7002)
	nap.connect()
	air = ServoValve(0,328,525)
	UART.setup("UART2")
	# brakes = Brakes("/dev/ttyO3", 115200)
	Expansion = Arduino("/dev/ttyO2", 115200)
	AirValve = Switch("GPIO3_19", "GPIO1_17")
	sensors = Sensors(Expansion)
	log = SensorLogging('DataLoggingTest.csv', sensors)
	log.start()

	nap.sendln("Hello World!")

	data = ""
	command = ""
	args = ""
	
	while not ("quit" in command):
		nap.send(">")
		data = nap.recieve()
		command = data[0:data.find(" ")]
		args = data[data.find(" ")+1:len(data)-1]
		if command == "valve_open":
			nap.sendln(" CMD: Opening valve.")
			AirValve.open()
		if command == "valve_close":
			nap.sendln(" CMD: Closing valve.")
			AirValve.close()
		if command == "valve_status":
			nap.sendln(" CMD: Is open: {}".format(AirValve.isopen))
		if command == "tape_pulse_period":
			nap.sendln(str(brakes.pulseperiod()))
		if command == "set_brakes":
			Expansion.setbrakes(True)
		if command == "release_brakes":
			Expansion.setbrakes(False)
		if command == "start_test":
			Expansion.settest(True)
		if command == "stop_test":
			Expansion.settest(False)
		if command == "read_data":
			nap.sendln(sensors.read(args))
		if command == "help":
			nap.sendln(helpfile)
		if command == "sensor_list":
			nap.sendln(sensor_list)
		if command == "ready":
			nap.sendln(" CMD: Signaling ready to be pushed.")
			log.SpaceXTelemetry.podstats['status'] = 2
		if command == "abort":
			nap.sendln(" CMD: Signaling abort.")
			log.SpaceXTelemetry.podstats['status'] = 0
		if command == "reset_imu":
			nap.sendln(" CMD: Taring IMU values.")
			log.sensors.Imu.firstrun = True
			log.sensors.Imu.velocity = 0
			log.sensors.Imu.position = 0

finally:
	try:
		log.close_log()
	except:
		print 'cant close log'
	try:
		air.close()
	except:
		print 'cant close air'
	try:
		brakes.close()
	except:
		print 'cant close brakes'
	try:
		nap.close()
	except:
		print 'cant close nap'
	
