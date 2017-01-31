from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.UART as UART
import Adafruit_ADS1x15
import Adafruit_GPIO.I2C as I2C
from brake_communication import Brakes
from imu import Imu

class Sensors:

	def __init__(self, brakes):
		UART.setup("UART1")
		self.adc1 = Adafruit_ADS1x15.ADS1115(address = 0x4A, busnum = 2)
		self.adc2 = Adafruit_ADS1x15.ADS1115(address = 0x4B, busnum = 2)
		self.temp1 = I2C.get_i2c_device(address = 0x4C, busnum = 2)
		self.brakes = brakes
		self.PodIMU = Imu("/dev/ttyO1", 115200)

		#self.temp1.write8(1,96)	#setup device in 12bit resolution - 0.0625degC

		self.current_data = {
				#Name		: [source,channel,value]
				'BBB_Temp'	: ['temp1',0,-1],
				#'LaserPortFwd'	: ['adc2' ,0,-1], # Laser. Not in use.
				#'LaserPortAft'	: ['adc2' ,1,-1], # Laser. Not in use.
				#'LaserStbdFwd'	: ['adc1' ,2,-1], # Laser. Not in use.
				#'LaserStbdAft'	: ['adc1' ,3,-1], # Laser. Not in use.
				#'AccumPress'	: ['adc1' ,0,-1],
				#'CylinderPress'	: ['adc1' ,1,-1],
				#'Ain7' 	: ['adc2' ,2,-1],
				#'Ain8' 	: ['adc2' ,3,-1],
				'HighPressure'  : ['adc2' ,0,-1], # 0 to 5000 psi
				'LowPressure'   : ['adc2' ,1,-1], # 0 to 100 psi
				'Accumulator'   : ['adc2' ,2,-1], # 0 to 5000 psi
				'Cylinder'      : ['adc2' ,3,-1], # 0 t0 1000 psi
				'TapeCount'     : ['due'  ,0,-1],
				'TapeMax'       : ['due'  ,0,-1],
				'Cell0'         : ['due'  ,0,-1],
				'Cell1'         : ['due'  ,0,-1],
				'Cell2'         : ['due'  ,0,-1],
				'Cell3'         : ['due'  ,0,-1],
				'BrakeStatus'   : ['due'  ,0,-1],
				'TimeElapsed'   : ['due'  ,0,-1],
				'TimeMax'       : ['due'  ,0,-1],
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
				'MagnetoZ'      : ['imu'  ,0,-1],
				'Position'      : ['imu'  ,0,-1],
				'Velocity'      : ['imu'  ,0,-1],
				'Acceleration'  : ['imu'  ,0,-1]}

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
			if('due' in self.current_data[item][0]): # Jank AF
			 	if item == 'TapeCount':
					self.current_data[item][2] = self.brakes.gettape()
				elif item == 'Cell0':
					self.current_data[item][2] = self.brakes.getvoltages()[0] / 1023 * 5
				elif item == 'Cell1':
					self.current_data[item][2] = (self.brakes.battery[1] * 2 - self.brakes.battery[0]) / 1023 * 5
				elif item == 'Cell2':
					self.current_data[item][2] = (self.brakes.battery[2] * 3 - self.brakes.battery[1] - self.brakes.battery[0]) / 1023 * 5 
				elif item == 'Cell3':
					self.current_data[item][2] = (self.brakes.battery[3] * 4 - self.brakes.battery[2] - self.brakes.battery[1] - self.brakes.battery[0]) / 1023 * 5
				elif item == 'BrakeStatus':
					self.current_data[item][2] = self.brakes.getbrakes() #
				elif item == 'TimeElapsed':
					self.current_data[item][2] = self.brakes.gettime()
				elif item == 'TimeMax':
					self.current_data[item][2] = self.brakes.maxtime
				elif item == 'TapeMax':
					self.current_data[item][2] = self.brakes.tapemax
				else:
				    	print('DATA: Unknown variable {}'.format(item))
			if('imu' in self.current_data[item][0]):
				self.PodIMU.update()
				self.current_data[item][2] = self.PodIMU.getdata(item)
		finally:
			return self.current_data[item][2]
