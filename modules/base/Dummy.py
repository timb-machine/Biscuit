class DummyModule(object):
	STATUS_BAD = 0
	STATUS_OK = 1

	def __init__(self, modulename):
		self.modulename = modulename
		self.statusflag = self.STATUS_BAD
		self.moduleoptions = {}
		print self.modulename

	def set(self, optionname, optionvalue):
		self.moduleoptions[optionname] = optionvalue
