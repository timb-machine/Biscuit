from modules.base import Dummy
import sys
import re
import time

class RunScriptModule(Dummy.DummyModule):
	def __init__(self):
		super(RunScriptModule, self).__init__("RunScript")
		self.set("scriptfilename", "resources/DeviceID.txt")

	def activate(self, device):
		filehandle = open(self.moduleoptions["scriptfilename"], "r")
		for scriptdata in filehandle:
			if not re.match("^#", scriptdata):
				scriptdata = re.sub("[\x0a]$", "", scriptdata)
				print ">" + scriptdata + "\n"
				device.write(scriptdata + "\n\r")
				sys.stdout.write(device.read())
		filehandle.close()

	def execute(self, commandtokens, device):
		if commandtokens[0] == "activate":
			self.activate(device)
			return self.STATUS_OK
