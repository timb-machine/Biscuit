from modules.base import Dummy
from modules.base import Device
import threading
import sys

def tracer(device, filehandle):
	STATUS_BAD = 0
	STATUS_OK = 1
	status = STATUS_OK
	while statusflag != STATUS_BAD:
		try:
			filehandle.write(device.serial.read(1))
		except device.serial.SerialException:
			statusflag = STATUS_BAD
	
class ATTRACEModule(Dummy.DummyModule):
	def __init__(self):
		super(ATTRACEModule, self).__init__("ATTRACE")
		self.set("devicefilename", "/dev/ttyACM1")
		self.set("outputfilename", "trace")

	def activate(self, device):
		self.tracedevice = Device.Device(self.moduleoptions["devicefilename"])
		self.filehandle = open(self.moduleoptions["outputfilename"], "w")
		self.thread = threading.Thread(target=tracer, args=(self.tracedevice, self.filehandle))
		self.thread.start()
		device.write("AT+TRACE=1\r")
		print device.read()

	def deactivate(self, device):
		self.thread.stop()
		self.filehandle.close()
		self.tracedevice.close()
		device.write("AT+TRACE=0\r")
		print device.read()

	def execute(self, commandtokens, device):
		if commandtokens[0] == "activate":
			self.activate(device)
			return self.STATUS_OK
		if commandtokens[0] == "deactivate":
			self.deactivate(device)
			return self.STATUS_OK
