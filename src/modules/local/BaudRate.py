from modules.base import Dummy
import sys

class BaudRateModule(Dummy.DummyModule):
	def __init__(self):
		super(BaudRateModule, self).__init__("BaudRate")

	def activate(self, device):
		for baudrate in [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 56000, 57600, 115200, 128000, 153600, 230400, 256000, 460800, 921600]:
			device.close()
			print baudrate
			device.options["baudrate"] = baudrate
			device.open()
			device.write("AT\r")
			print device.read()
	
	def execute(self, tokens, device):
		if tokens[0] == "activate":
			self.activate(device)
			return self.STATUS_OK
