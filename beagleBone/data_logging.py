import thread
import time
import sched
import threading
import math
from nap_communication import NAP
from telemetry import Telemetry
from ctypes import *

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
		    
class SensorLogging(threading.Thread):

	daemon = True

	oldbeacontime = 0
	olddatatime   = 0

	def __init__(self, filename, sensors):
		try:
			self.nap = NAP(7003)
			self.nap.connect()
		except:
			print 'data logging failed to connect'
		threading.Thread.__init__(self)
		# Setup the telemetry sending class.
		self.SpaceXTelemetry = Telemetry("192.168.0.1", 3000)
		# For debugging purposes, in the lab.
		self.MyTelemetry = Telemetry("192.168.1.3", 3000)
		self.PodStats = PodDataStruct()

		self.PodStats.id = 29
		self.PodStats.status = 1
		self.PodStats.accel = 0
		self.PodStats.pos = 0
		self.PodStats.vel = 0
		self.PodStats.volt = 0
		self.PodStats.current = 0
		self.PodStats.battemp = 0
		self.PodStats.podtemp = 0
		self.PodStats.stripe = 0

		self.log = open(filename, 'w+', 0)
		self.log.write('index,timestamp,sensor_name,value\n')
		self.index = 0
		self.logRun = True
		self.sched = sched.scheduler(time.time, time.sleep)
		self.data = sensors.current_data
		self.sensors = sensors
		self.oldtime = time.time()

	def run(self):
		while self.logRun:
			self.sensors.read_all()
			now = time.time()
			if now - self.oldbeacontime > 0.1:
				self.PodStats.accel = self.sensors.PodIMU.accel
				self.PodStats.pos = self.sensors.PodIMU.position
				self.PodStats.vel = self.sensors.PodIMU.velocity
				self.Podstats['stripe'] = self.data['TapeCount'][2]
				self.SpaceXTelemetry.beacon(self.PodStats)
				self.MyTelemetry.beacon(self.PodStats)
				self.oldbeacontime = now

			if now - self.olddatatime > 0.05:
				for key, list in self.data.items():
					self.nap.sendln(str(self.index) + ',' + str(time.time()) + ',' + key + ',' + str(list[2]))
					self.log.write(str(self.index) + ',' + str(time.time()) + ',' + key + ',' + str(list[2]) + '\n')
					self.index = self.index+1
				self.olddatatime = now

	def close_log(self):
		self.logRun = False
		time.sleep(1)
		self.nap.close()
		self.log.close()
		return self.log.closed
