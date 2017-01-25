import serial
import time
import math

# Calculate the checksum of some arbitrary string.
def calcsum(data):
	checksum = 0
	for i in data:
		checksum ^= ord(i)
	return checksum

class Imu:
	# The most recent attitude packet received.
	attitude = { 'time'   : 0 , # UTC time of day (if GPS is connected), otherwise time since the last attitude packet was sent.
		     'roll'   : 0 , # degrees
		     'pitch'  : 0 ,
		     'yaw'    : 0 ,
		     'heading': 0 } # degrees, as reported by GPS (if connected)

	# The most recent sensor packet received.
	sensor = { 'count'     : 0 , # Most recent sensor packet type. 0 = gyro, 1 = accel, 2 = magneto
		   'time'      : 0 , # UTC time of day (if GPS is connected), otherwise time since the sensor was turned on.
		   'gyro_x'    : 0 , # degrees per second
		   'gyro_y'    : 0 ,
		   'gyro_z'    : 0 ,
		   'accel_x'   : 0 , # in units of gravities
		   'accel_y'   : 0 ,
		   'accel_z'   : 0 ,
		   'magneto_x' : 0 , # unitless (normalized)
		   'magneto_y' : 0 ,
		   'magneto_z' : 0 }

	accel = 0
	velocity = 0
	position = 0

	def __init__(self, port, baud):
		# Initialize serial port. Constructor opens port for us.
		self.device = serial.Serial(port, baud, timeout=0)
		# Error checking ?

	def update(self):
		pkt = self.device.readline()
		if pkt == "":
			return

		fields = pkt.split(",")
		# Get the last element in the array (checksum) and compare it to the actual value.
		chksum = int(fields.pop()[1:], 16) # The second argument is to interpret string as base 16.
		# pkt[1:-5] Everything except the first 1 character and the last 5 characters.
		expected = calcsum(pkt[1:-5])

		if chksum != expected:
			print(' IMU: Bad checksum! Expected "{}", got "{}"'.format(expected, chksum))
			return

		if fields[0] == "$PCHRA": # Attitude packet received.
			print(' IMU: Received an attitude packet.')
			self.attitude['time']    = float(fields[1])
			self.attitude['roll']    = float(fields[2])
			self.attitude['pitch']   = float(fields[3])
			self.attitude['yaw']     = float(fields[4])
			self.attitude['heading'] = float(fields[5])
		elif fields[0] == "$PCHRS": # Sensor packet received.
			print(' IMU: Received a sensor packet.')
			self.sensor['count']     = int(fields[1])

			if self.sensor['count'] == 0: # Gyroscope data.
				self.sensor['gyro_x']  = float(fields[3])
				self.sensor['gyro_y']  = float(fields[4])
				self.sensor['gyro_z']  = float(fields[5])
			elif self.sensor['count'] == 1: # Accelerometer data.
				self.sensor['accel_x'] = float(fields[3])
				self.sensor['accel_y'] = float(fields[4])
				self.sensor['accel_z'] = float(fields[5])

				# Assumes this packets are received more or less in realtime.
				now = float(fields[2])
				delt = now - self.sensor['time'] # Seconds since last timestamp, in decimal form.
				self.accel = math.sqrt(self.sensor['accel_x'] ** 2 + self.sensor['accel_y'] ** 2 + self.sensor['accel_z'] ** 2)
				self.velocity += self.accelmag / delt
				self.position += self.velocity / delt

				self.sensor['time'] = now
			elif self.sensor['count'] == 2: # Magnetometer data.
				self.sensor['magneto_x'] = float(fields[3])
				self.sensor['magneto_y'] = float(fields[4])
				self.sensor['magneto_z'] = float(fields[5])
		else:
			print(' IMU: Received undefined packet type "{}".'.format(fields[0]))

	# Weird interface function needed for the Sensors class in the data_collection.py file.
	def getdata(self, query):
		if query == 'Roll':
			return self.attitude['roll']
		elif query == 'Pitch':
			return self.attitude['pitch']
		elif query == 'Yaw':
			return self.attitude['yaw']
		elif query == 'Heading':
			return self.attitude['heading']
		elif query == 'GyroX':
			return self.sensor['gyro_x']
		elif query == 'GyroY':
			return self.sensor['gyro_y']
		elif query == 'GyroZ':
			return self.sensor['gyro_z']
		elif query == 'AccelX':
			return self.sensor['accel_x']
		elif query == 'AccelY':
			return self.sensor['accel_y']
		elif query == 'AccelZ':
			return self.sensor['accel_z']
		elif query == 'MagnetoX':
			return self.sensor['magneto_x']
		elif query == 'MagnetoY':
			return self.sensor['magneto_y']
		elif query == 'MagnetoZ':
			return self.sensor['magneto_z']
		elif query == 'Position':
			return self.position
		elif query == 'Velocity':
			return self.velocity
		elif query == 'Acceleration'
			return self.accel:
		else:
			return -999
