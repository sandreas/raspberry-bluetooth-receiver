#!/usr/bin/env python
import sys
import alsaaudio

'''
# list controls (search for Master Playback Volume)
amixer controls
numid=4,iface=MIXER,name='Master Playback Switch'
numid=3,iface=MIXER,name='Master Playback Volume'
numid=2,iface=MIXER,name='Capture Switch'
numid=1,iface=MIXER,name='Capture Volume'

amixer cget numid=3
numid=3,iface=MIXER,name='Master Playback Volume'
  ; type=INTEGER,access=rw------,values=2,min=0,max=65536,step=1
  : values=58983,58983

  
  
# set volume
amixer cset numid=3 80%

# increase by 3%
amixer -q sset Master 3%+

# decrease by 3%
amixer -q sset Master 3%-

# mute/unmute
amixer -q sset Master toggle

'''
class AlsaVolumeControl:
	def __init__(self, process_builder):
		self.cmd = process_builder
	'''
			self.master_num = "3"
			self.detectMaster()
		
		def detectMaster(self):
			code = self.cmd.run(["amixer", "controls"])
			if code != 0: 
				return
			lines = self.cmd.getOutput().splitlines()
			for line in lines:
				values = self.parseLine(line)
				if "numid" not in values:
					continue
				if "name" not in values:
					continue
				if "Master" in values["name"] and "Volume" in values["name"]:
					self.master_num = values["numid"]
					print self.master_num
		
		def parseLine(self, line):
			values = {}
			cols = line.split(",")
			for col in cols:
				parts = col.strip().split("=")
				if len(parts) == 2:
					key = parts[0]
					value = parts[1].strip("'")
					values[key] = value
			return values
		
		def setVolume(self, volume):
			self.cmd.run(["amixer", "cset", "numid={}".format(self.master_num)])
		
		def getVolume(self, volume):
			self.mixer.getvolume()	
		
		def mute(self):
			self.volume_before_mute = self.getVolume()
			self.setVolume(0)
		
		def unmute(self):
			return self.setVolume(self.volume_before_mute)
	'''	
	def muteToggle(self):
		self.cmd.run(["amixer", "sset", "Master", "toggle"])
	'''			
		def isMute(self):
			return self.getVolume() == 0L
	'''			
	def increase(self):
		self.changeVolume(3)
		
	def decrease(self):
		self.changeVolume(-3)
		
	def changeVolume(self, offset):
		operator = "+"
		if offset < 0:
			operator = "-"
				
		self.cmd.run(["amixer", "sset", "Master", "{}%{}".format(abs(offset), operator)])
		if "[off]" in self.cmd.getOutput():
			self.muteToggle()
		
	