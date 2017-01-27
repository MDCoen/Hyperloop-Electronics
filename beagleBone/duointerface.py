import serial

class Arduino:

	tapec = 0
	isbraking = True
	istesting = False
	battery = [ 0, 0, 0, 0 ]

	def __init__(self, nport, baud):
		self.serline = serial.Serial(port = nport, baudrate=baud, timeout=2)

	def parseln(self):
		pkt = self.serline.readline()
		if pkt == "":
			return -1

		fields = pkt.split(",")
		return fields
	
	def gettapes(self):
		self.serline.write("tape_count;")
		values = self.parseln()
		if values != -1:
			if values[0] == "tape":
				tapec = int(values[1])
				return tapec
			else:
				print(' DUO: Incorrect packet. Expected tape, got {}'.format(values[0]))
				return -2

		print(' DUO: No response received!')
		return -1

	def setbrakes(self, on):
		if on:
			self.serline.write("brakes_on")
		else:
			self.serline.write("brakes_off")
		return self.getbrakes()

	def getbrakes(self):
		self.serline.write("get_brake_status")
		values = self.parseln()
		if values != -1:
			if values[0] == "brake":
				self.isbraking = int(values[1])
				return self.isbraking
			else:
				print(' DUO: Incorrect packet. Expected brake, got {}'.format(values[0]))
				return -2

		print(' DUO: No response received!')
		return -1

	def settest(self, start):
		if start:
			self.serline.write("start_test")
		else:
			self.serline.write("stop_test")
		return self.gettest()

	def gettest(self):
		self.serline.write("get_test_status")
		values = self.parseln()
		if values != -1:
			if values[0] == "test":
				self.istesting = int(values[1])
				return self.istesting
			else:
				print(' DUO: Incorrect packet. Expected test, got {}'.format(values[0]))
				return -2

		print(' DUO: No response received!')
		return -1

	def getvoltages(self):
		self.serline.write("get_voltages")
		values = self.parseln()
		if values != -1:
			if values[0] == "voltages":
				self.battery[0] = float(values[1])
				self.battery[1] = float(values[2])
				self.battery[3] = float(values[3])
				self.battery[4] = float(values[4])
				return self.battery
			else:
				print(' DUO: Incorrect packet. Expected voltages, got {}'.format(values[0]))
				return 02

		print(' DUO: No response received!')
		return -1
