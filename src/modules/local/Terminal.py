from modules.base import Dummy
import threading
import sys
import termios
import tty

def reader(device):
	while device.statusflag != device.STATUS_BAD:
		try:
			character = device.serial.read(1)
		except device.serial.SerialException:
			device.statusflag = device.STATUS_BAD
		if character == "\n":
			character = "\r\n"
		sys.stdout.write(character)

def writer(device):
	# TODO handle ctrl-C sanely
	while device.statusflag != device.STATUS_BAD:
		filehandle = sys.stdin.fileno()
		oldtermattr = termios.tcgetattr(filehandle)
		tty.setraw(filehandle)
		character = sys.stdin.read(1)
		#sys.stdout.write(character)
		if character == "\x04":
			device.statusflag = device.STATUS_BAD
		elif character == "\n":
			character = "\r"
		termios.tcsetattr(filehandle, termios.TCSADRAIN, oldtermattr)
		device.serial.write(character)

class TerminalModule(Dummy.DummyModule):
	def __init__(self):
		super(TerminalModule, self).__init__("Terminal")

	def activate(self, device):
		if device.statusflag == device.STATUS_OK:
			self.readerthread = threading.Thread(target=reader, args=(device,))
			self.readerthread.start()
			self.writerthread = threading.Thread(target=writer, args=(device,))
			self.writerthread.start()
			self.writerthread.join()
			self.readerthread.join()

	def execute(self, commandtokens, device):
		if commandtokens[0] == "activate":
			self.activate(device)
			return self.STATUS_OK
