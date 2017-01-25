from Adafruit_I2C import Adafruit_I2C
import Adafruit_PCA9685
import time

class ServoValve:

	min_pos = 0
	max_pos = 0
	channel = 0

	def __init__(self, valve, open, close):
		self.i2c = Adafruit_I2C(0x40, busnum=2)
		self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=2)
		self.pwm.set_pwm_freq(60)
		self.channel = valve
		self.min_pos = open
		self.max_pos = close
	
	def open(self):
		self.pwm.set_pwm(self.channel,0,self.min_pos-50)
		time.sleep(2)
		self.pwm.set_pwm(self.channel,0,self.min_pos)
		return "Valve Open"
	
	def close(self):
		self.pwm.set_pwm(self.channel,0,self.max_pos+50)
		time.sleep(2)
		self.pwm.set_pwm(self.channel,0,self.max_pos)
		return "Valve Closed"
	
	def set_close(self, position):
		if type(position) is int or type(position) is float:
			self.max_pos = position
			return position
		else:
			return 0
	
	def set_open(self, position):
		if type(position) is int or type(position) is float:
			self.min_pos = position
			return position
		else:
			return 0

	def get_close(self):
		return self.max_pos
		
	def get_open(self):
		return self.min_pos
