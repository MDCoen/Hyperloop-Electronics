import serial

class BatMon

	voltage = 0
	current = 0
	temp = 0

	def __init__(self, nport)
		self.s = serial.Serial(port = nport, baudrate = 19200, timeout = 0)

	def update(self)
		pkt = self.s.readline()
		if pkt == "":
			return

		fields = pkt.split("\t")

		if fields[0] == "V":
			# Battery voltage, in mV
			self.voltage = float(fields[1])
		if fields[0] == "I":
			# Battery current, in mA
			self.current = float(fields[1])
		if fields[0] == "T"
			# Battery temperature, in deg. C
			self.temp = float(fields[1])
