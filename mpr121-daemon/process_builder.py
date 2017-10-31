#!/usr/bin/env python

from subprocess import Popen, PIPE
class ProcessBuilder:
	def run(self, cmd):
		self.output = ""
		self.err = ""
		self.p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		self.output, self.err = self.p.communicate()
		return self.p.returncode
	
	def getOutput(self):
		return self.output
		
	def getError(self):
		return self.err