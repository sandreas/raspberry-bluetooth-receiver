#!/usr/bin/env python
import sys
from subprocess import call


class NetDeviceControl:
	def __init__(self, deviceName):
		self.device = deviceName
		
	def up(self):
		call(["ifconfig", self.device, "up"])
	
	def down(self):
		call(["ifconfig", self.device, "down"])
	
	def getStatus(self):
		statusfile = "/sys/class/net/{}/operstate".format(self.device)
		file = open(statusfile, "r") 
		status = file.read() 
		file.close()
		return status.strip()
	
	def toggle(self):
		if self.getStatus() == "up":
			self.down()
		else:
			self.up();
	
		
		
