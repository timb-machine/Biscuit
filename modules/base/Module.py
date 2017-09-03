import glob
import os.path

import sys
import pprint

class Manager:
	MODULE_NOT_IMPORTED = 0
	MODULE_IMPORTED = 1

	def __init__(self):
		self.modules = []
		self.modulename = ""
		self.activemodules = {}

	def available(self, local):
		if local == 1 or local == "1":
			self.modules = glob.glob("modules/local/[A-Za-z]*.py")
		else:
			self.modules = glob.glob("modules/remote/[A-Za-z]*.py")

	def use(self, filename):
		if filename in self.modules:
			modulepath, filename = os.path.split(filename)
			modulepath = modulepath.replace("/", ".")
			modulename, modulexextension = os.path.splitext(filename)
			statusflag = self.MODULE_NOT_IMPORTED
			for activemodulename in self.activemodules.keys():
				if activemodulename == modulename:
					statusflag = self.MODULE_IMPORTED
			if statusflag == self.MODULE_NOT_IMPORTED:
				module = __import__(modulepath, fromlist=[modulename])
				moduleclass = getattr((getattr(module, modulename)), modulename + "Module")
				self.activemodules[modulename] = moduleclass()
				self.modulename = modulename
			else:
				# already imported, what should we do
				self.modulename = modulename
				pass
		else:
			self.modulename = ""

	def get(self):
		if self.modulename:
			for modulename in self.activemodules.keys():
				if modulename == self.modulename:
					return self.activemodules[modulename]
