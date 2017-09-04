import glob
import serial

class Manager:
	def __init__(self):
		self.devices = []
		self.filename = ""
		self.opendevices = []

	def scan(self):
		self.devices = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")

	def select(self, filename):
		if filename in self.devices:
			self.filename = filename
		else:
			self.filename = ""

	def open(self):
		if self.filename:
			for device in self.opendevices:
				if device.filename == self.filename:
					device.close()
					self.opendevices.remove(device)
					del(device)
			device = Device(self.filename)
			self.opendevices.append(device)

	def get(self):
		if self.filename:
			for device in self.opendevices:
				if device.filename == self.filename:
					return device

	def close(self):
		if self.filename:
			for device in self.opendevices:
				if device.filename == self.filename:
					device.close()
					self.opendevices.remove(device)
					del(device)

class Device:
	STATUS_BAD = 0
	STATUS_OK = 1

	def __init__(self, filename):
		self.filename = filename
		self.deviceoptions = {}
		self.deviceoptions["baudrate"] = 115200
		self.deviceoptions["local"] = 1
		self.statusflag = self.STATUS_BAD
		self.open()

	def set(self, optionname, optionvalue):
		self.deviceoptions[optionname] = optionvalue

	def open(self):
		# TODO we should really do this properly
		self.serial = serial.Serial(self.filename, self.deviceoptions["baudrate"])
		self.serial.timeout = 0 
		self.serial.inter_byte_timeout = 1
		self.statusflag = self.STATUS_OK

	def read(self):
		# TODO we should really do this properly
		return self.serial.read(512)
	
	def write(self, writedata):
		# TODO we should really do this properly
		self.serial.write(writedata)
	
	def close(self):
		self.statusflag = self.STATUS_BAD
		self.serial.close()
		del(self.serial)
