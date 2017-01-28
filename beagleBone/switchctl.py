import Adafruit_BBIO.GPIO as GPIO
import time

class Switch:

	isopen = False

	def __init__(self, newpinopen, newpinclose):
		self.pinopen = newpinopen
		self.pinclose = newpinclose

		GPIO.setup(self.pinopen, GPIO.OUT)
		GPIO.setup(self.pinclose, GPIO.OUT)

		GPIO.output(self.pinopen, GPIO.LOW)
		GPIO.output(self.pinclose, GPIO.LOW)

		self.close()

	def open(self):
		GPIO.output(self.pinopen, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(self.pinopen, GPIO.LOW)
		self.isopen = True

	def close(self):
		GPIO.output(self.pinclose, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(self.pinclose, GPIO.LOW)
		self.isopen= False

	def status(self):
		return self.isopen
