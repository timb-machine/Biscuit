from modules.base import Device
from modules.base import Module
import readline
import shlex

class Shell:
	STATUS_BAD = 0
	STATUS_OK = 1

	def __init__(self):
		self.devicemanager = Device.Manager()
		self.modulemanager = Module.Manager()

	def loop(self, promptstring):
		statusflag = self.STATUS_OK
		while statusflag != self.STATUS_BAD:
			try:
				device = self.devicemanager.get()
				if device in self.devicemanager.opendevices:
					openflag = " *"
				else:
					openflag = ""
				commandstring = raw_input("[" + self.modulemanager.modulename + "@" + self.devicemanager.filename + openflag + "] " + promptstring)
				if commandstring:
					commandtokens = shlex.split(commandstring)
					statusflag = self.execute(commandtokens)
			except EOFError:
				statusflag = self.STATUS_BAD

	def execute(self, commandtokens):
		if commandtokens[0] == "exit":
			return self.STATUS_BAD
		elif commandtokens[0] == "scan":
			self.devicemanager.scan()
			print self.devicemanager.devices
			return self.STATUS_OK
		elif commandtokens[0] == "select":
			if len(commandtokens) == 1:
				self.devicemanager.select("")
			elif len(commandtokens) == 2:
				if not self.devicemanager.devices:
					self.devicemanager.scan()
				self.devicemanager.select(commandtokens[1])
			return self.STATUS_OK
		elif commandtokens[0] == "open":
			self.devicemanager.open()
			return self.STATUS_OK
		elif commandtokens[0] == "ready":
			for device in self.devicemanager.opendevices:
				print device.filename
			return self.STATUS_OK
		elif commandtokens[0] ==  "show":
			device = self.devicemanager.get()
			if device:
				print device.filename
				print device.deviceoptions
			module = self.modulemanager.get()
			if module:
				print module.modulename
				print module.moduleoptions
			return self.STATUS_OK
		elif commandtokens[0] ==  "set":
			if commandtokens[1] == "device":
				device = self.devicemanager.get()
				if device:
					if len(commandtokens) == 2:
						print device.filename
						print device.deviceoptions
					elif len(commandtokens) == 4:
						device.set(commandtokens[2], commandtokens[3])
			elif commandtokens[1] == "module":
				module = self.modulemanager.get()
				if module:
					if len(commandtokens) == 2:
						print module.modulename
						print module.moduleoptions
					elif len(commandtokens) == 4:
						module.set(commandtokens[2], commandtokens[3])
			else:
				device = self.devicemanager.get()
				if device:
					print device.filename
					print device.deviceoptions
				module = self.modulemanager.get()
				if module:
					print module.modulename
					print module.moduleoptions
			return self.STATUS_OK
		elif commandtokens[0] == "available":
			device = self.devicemanager.get()
			if device:
				self.modulemanager.available(device.deviceoptions["local"])
				print self.modulemanager.modules
			return self.STATUS_OK
		elif commandtokens[0] == "use":
			device = self.devicemanager.get()
			if device:
				if len(commandtokens) == 1:
					self.modulemanager.use("")
				elif len(commandtokens) == 2:
					if not self.modulemanager.modules:
						self.modulemanager.available(device.deviceoptions["local"])
					self.modulemanager.use(commandtokens[1])
			return self.STATUS_OK
		elif commandtokens[0] == "active":
			for modulename in self.modulemanager.activemodules.keys():
				print modulename
		elif commandtokens[0] == "close":
			self.devicemanager.close()
			return self.STATUS_OK
		else:
			device = self.devicemanager.get()
			if device:
				module = self.modulemanager.get()
				if module:
					module.execute(commandtokens, device)
