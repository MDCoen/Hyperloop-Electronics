import socket

class PodDataStruct(LittleEndianStructure):
	_pack_   = 1
	_fields_ = [("id"     , c_ubyte),
	            ("status" , c_ubyte),
                ("accel"  , c_int),
                ("pos"    , c_int),
                ("vel"    , c_int),
                ("volt"   , c_int),
                ("current", c_int),
                ("battemp", c_int),
                ("podtemp", c_int),
                ("stripe" , c_uint)]

class Telemetry:
	def __init__(self, dest, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.target = dest
		self.port = port
		self.podstats = PodDataStruct()

	def beacon(self):
		self.s.sendto(self.podstats, (self.target, self.port))

	def close(self):
		self.s.close()
