import thread
import time
import sched
import threading
import math
from nap_communication import NAP
from telemetry import Telemetry


class SensorLogging(threading.Thread):

	daemon = True

	oldtime = 0

	def __init__(self, filename, sensors):
		try:
			self.nap = NAP(7003)
			self.nap.connect()
		except:
			print 'data logging failed to connect'
		threading.Thread.__init__(self)
		# Setup the telemetry sending class.
		SpaceXTelemetry = Telemetry(192.168.0.1, 3000)
		# For debugging purposes, in the lab.
		MyTelemetry = Telemetry(192.168.1.3, 3000)
		PodStats = PodDataStruct()

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
			if now - oldtime > 0.1:
				SpaceXTelemetry.podstats['id'] = 29
				SpaceXTelemetry.podstats['status'] = 0
				SpaceXTelemetry.podstats['accel'] = self.sensors.PodIMU.accel
				SpaceXTelemetry.podstats['pos'] = self.sensors.PodIMU.position
				SpaceXTelemetry.podstats['vel'] = self.sensors.PodIMU.velocity
				SpaceXTelemetry.podstats['volt'] = 0
				SpaceXTelemetry.podstats['current'] = 0
				SpaceXTelemetry.podstats['battemp'] = 0
				SpaceXTelemetry.podstats['podtemp'] = 0
				SpaceXTelemetry.podstats['stripe'] = self.data['TapeCount'][2]
				MyTelemetry.podstats = SpaceXTelemetry.podstats
				SpaceXTelemetry.beacon()
				MyTelemetry.beacon()
				oldtime = now

			for key, list in self.data.items():
				self.nap.sendln(str(self.index) + ',' + str(time.time()) + ',' + key + ',' + str(list[2]))
				self.log.write(str(self.index) + ',' + str(time.time()) + ',' + key + ',' + str(list[2]) + '\n')
				self.index = self.index+1

	def close_log(self):
		self.logRun = False
		time.sleep(1)
		self.nap.close()
		self.log.close()
		return self.log.closed
