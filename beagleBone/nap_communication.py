import socket

class NAP:

	def __init__(self, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '192.168.1.2'
		self.port = port
		self.s.bind((self.host,self.port))
	
	def connect(self):
		self.s.listen(1)
		self.c, self.addr = self.s.accept()
		print 'Connected to Address:', self.addr
	
	def send(self, data):
		if type(data) is str:
			self.c.send(data)
		else:
			self.c.send(str(data))

	def sendln(self, data):
		if type(data) is str:
			self.send(data + "\r\n")
		else:
			self.send(str(data) + "\r\n")

	def recieve(self):
		data = self.c.recv(1024)
		print 'Acknowledge Data: ' + data[:len(data)-1]
		#self.c.send('Acknowledge')
		return data

	def close(self):
		self.c.close()
		self.s.shutdown(1)
		self.s.close()
