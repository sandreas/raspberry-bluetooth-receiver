#!/usr/bin/env python
import sys
import time

import Adafruit_MPR121.MPR121 as MPR121
 
class MprWatcher:
	def __init__(self,keyMethodMapping):
		self.keyMethodMapping = keyMethodMapping
		
	def run(self):
		self.cap = MPR121.MPR121()
		if not self.cap.begin():
			raise IOError("Could not begin capturing")
		last_touched = self.cap.touched()
		#print "last_touched: "
		while True:
			current_touched = self.cap.touched()
			for i in range(12):
				pin_bit = 1 << i
				if current_touched & pin_bit and not last_touched & pin_bit:
					print('{0} touched!'.format(i))
				if not current_touched & pin_bit and last_touched & pin_bit:
					print('{0} released!'.format(i))
					if i in self.keyMethodMapping:#
						print('key found, method executing')
						self.keyMethodMapping[i]()
					else:
						print('key not found')
			last_touched = current_touched
			time.sleep(0.1)			
