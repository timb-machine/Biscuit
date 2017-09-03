#!/usr/bin/python

from modules.base import UI

if __name__ == "__main__":
	shell = UI.Shell()
	shell.loop("biscuit> ")
