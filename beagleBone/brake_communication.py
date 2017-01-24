import Adafruit_BBIO.UART as UART
import serial

UART.setup("UART2")

class Brakes:

	def __init__(self):
		UART.setup("UART2")
		self.brakes = serial.Serial(port = "/dev/ttyO2", baudrate=115200, timeout=2)
		self.brakes.close()
		self.brakes.open()
		if self.brakes.isOpen():
			return
		else:
			self.brakes.close()

	def tapecount(self):
		self.brakes.write("tapeCount;")
		response = self.brakes.readline()
		return int(response[response.find(':')+2:response.find('u')-1])

	def pulseperiod(self):
		self.brakes.write("pulseperiod;")
		response = self.brakes.readline()
		return int(response[response.find(':')+2:response.find('m')-1])

	def pulsetime(self):
		self.brakes.write("pulsetime;")
		response = self.brakes.readline()
		return float(response[response.find(':')+2:response.find('m')-1])

	def speed(self):
		self.brakes.write("speed;")
		response = self.brakes.readline()
		return float(response[response.find(':')+2:response.find('m')])

	def position(self):
		self.brakes.write("position;")
		response = self.brakes.readline()
		return int(response[response.find(':')+2:response.find('f')])

	def solenoid_current(self):
		self.brakes.write("current;")
		response = self.brakes.readline()
		return float(response[response.find(':')+2:response.find('c')])

	def set_brakes(self, position):
		if position == "open":
			self.brakes.write("brake_release;")
		else:
			if position == "close":
				self.brakes.write("brake_set;")
			else:
				return "Invalid Command"
		response = self.brakes.readline()
		return response[:len(response)-1]

	def close(self):
		self.brakes.close()
