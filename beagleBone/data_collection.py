from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.UART as UART
import Adafruit_ADS1x15
import Adafruit_GPIO.I2C as I2C
from brake_communication import Brakes
from imu import Imu

class Sensors:

	def __init__(self, brakes):
		self.adc1 = Adafruit_ADS1x15.ADS1115(address = 0x4A)
		self.adc2 = Adafruit_ADS1x15.ADS1115(address = 0x4B)
		self.temp1 = I2C.get_i2c_device(address = 0x4C)
		self.brakes = brakes
		UART.setup("UART2")
		self.PodIMU = Imu("/dev/ttyO2", 115200)
		self.brake_read = 0

		self.temp1.write8(1,96)	#setup device in 12bit resolution - 0.0625degC

		self.current_data = {
				#Name		: [source,channel,value]
				'BBB_Temp'	: ['temp1',0,-1],
				'LaserPortFwd'	: ['adc2' ,0,-1],
				'LaserPortAft'	: ['adc2' ,1,-1],
				'LaserStbdFwd'	: ['adc1' ,2,-1],
				'LaserStbdAft'	: ['adc1' ,3,-1],
				'AccumPress'	: ['adc1' ,0,-1],
				'CylinderPress'	: ['adc1' ,1,-1],
				'Ain7'		: ['adc2' ,2,-1],
				'Ain8'		: ['adc2' ,3,-1],
				#%'SolenoidCurr'	: ['due'  ,0,-1],
				'TapeCount'     : ['due'  ,0,-1],
				'Roll'          : ['imu'  ,0,-1],
				'Pitch'         : ['imu'  ,0,-1],
				'Yaw'           : ['imu'  ,0,-1],
				'Heading'       : ['imu'  ,0,-1],
				'GyroX'         : ['imu'  ,0,-1],
				'GyroY'         : ['imu'  ,0,-1],
				'GyroZ'         : ['imu'  ,0,-1],
				'AccelX'        : ['imu'  ,0,-1],
				'AccelY'        : ['imu'  ,0,-1],
				'AccelZ'        : ['imu'  ,0,-1],
				'MagnetoX'      : ['imu'  ,0,-1],
				'MagnetoY'      : ['imu'  ,0,-1],
				'MagnetoZ'      : ['imu'  ,0,-1]}

	def read_all(self):
		for self.name in self.current_data:
			self.read(self.name)
		return 0

	def read(self,item):
		try:
			if item not in self.current_data:
				return 'Invalid Sensor Name'
			if('temp' in self.current_data[item][0]):
				self.current_data[item][2] = eval('self.' + self.current_data[item][0] + '.readU16(0,False)')
			if('adc' in self.current_data[item][0]):
				self.current_data[item][2] = eval('self.' + self.current_data[item][0] + '.read_adc(' + str(self.current_data[item][1]) + ')')
			# if('due' in self.current_data[item][0]):
			# 	if item == 'SolenoidCurr':
			# 		if(self.brake_read%4 == 0):
			# 			self.current_data[item][2] = self.brakes.solenoid_current()
				if item == 'TapeCount':
					if self.brake_read % 4 == 0:
						self.current_data[item][2] = self.brakes.tapecount()
				self.brake_read = self.brake_read+1
			if('imu' in self.current_data[item][0]):
				self.PodIMU.update()
				self.current_data[item][2] = self.PodIMU.getdata(item)
		finally:
			return self.current_data[item][2]
