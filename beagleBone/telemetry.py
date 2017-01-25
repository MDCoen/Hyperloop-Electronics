import socket

class Telemetry:
	def __init__(self, dest, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.target = dest
		self.port = port

	def beacon(self, data):
		self.s.sendto(data, (self.target, self.port))

	def close(self):
		self.s.close()
