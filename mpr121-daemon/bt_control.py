#!/usr/bin/env python
import sys
import dbus
import time

class BtControl:
	SERVICE_NAME = "org.bluez"
	MEDIA_IFACE = SERVICE_NAME + '.Media1'
	AGENT_IFACE = SERVICE_NAME + '.Agent1'
	ADAPTER_IFACE = SERVICE_NAME + ".Adapter1"
	DEVICE_IFACE = SERVICE_NAME + ".Device1"
	PLAYER_IFACE = SERVICE_NAME + '.MediaPlayer1'
	TRANSPORT_IFACE = SERVICE_NAME + '.MediaTransport1'
	CONTROL_IFACE = SERVICE_NAME + '.MediaControl1'

	PLAYER_STATUS_PLAYING = "playing"
	PLAYER_STATUS_STOPPED = "stopped"
	PLAYER_STATUS_PAUSED = "paused"
	PLAYER_STATUS_FORWARD_SEEK = "forward-seek"
	PLAYER_STATUS_REVERSE_SEEK = "reverse-seek"
	PLAYER_STATUS_ERROR = "error"
	
	
	def __init__(self):
		self.paths = {}
		self.objects = {}
		self.props = {}
		self.connect()
		
	def connect(self):
		bus = dbus.SystemBus()
		manager = dbus.Interface(bus.get_object(self.SERVICE_NAME, "/"), "org.freedesktop.DBus.ObjectManager")
		objects = manager.GetManagedObjects()
		for path, interfaces in objects.iteritems():
			if self.MEDIA_IFACE in interfaces:
				self.paths[self.MEDIA_IFACE] = path

			if self.AGENT_IFACE in interfaces:
				self.paths[self.AGENT_IFACE] = path

			if self.ADAPTER_IFACE in interfaces:
				self.paths[self.ADAPTER_IFACE] = path
			
			if self.DEVICE_IFACE in interfaces:
				self.paths[self.DEVICE_IFACE] = path
				
			if self.PLAYER_IFACE in interfaces:
				self.paths[self.PLAYER_IFACE] = path
				
			if self.TRANSPORT_IFACE in interfaces:
				self.paths[self.TRANSPORT_IFACE] = path
				
			if self.CONTROL_IFACE in interfaces:
				self.paths[self.CONTROL_IFACE] = path
				
		for iface, path in self.paths.iteritems():
			self.objects[iface] = bus.get_object("org.bluez", path)
			self.props[iface] = dbus.Interface(self.objects[iface], "org.freedesktop.DBus.Properties")

	def runMethod(self, iface, methodName):
		if iface in self.objects: 
			obj = self.objects[iface]
			return getattr(obj, methodName)(dbus_interface=iface)
	
	def getProperty(self, iface, propertyName):
		if iface in self.props: 
			return self.props[iface].Get(iface, propertyName)			
		return None
	
	def setProperty(self, iface, propertyName, propertyValue):
		if iface in self.props: 
			return self.props[iface].Set(iface, propertyName, propertyValue)			
		return None	
	
	def getPlayingStatus(self):
		return self.getProperty(self.PLAYER_IFACE, "Status")
	
	def getPlayingPosition(self):
		return self.getProperty(self.PLAYER_IFACE, "Position")
	
	def getVolume(self):
		return self.getProperty(self.TRANSPORT_IFACE, "Volume")
	
#	def setVolume(self, value):
#		return self.setProperty(self.TRANSPORT_IFACE, "Volume", value)
		
	
	# PLAYER_IFACE METHODS
	def playPauseToggle(self):
		if self.getPlayingStatus() == "playing":
			self.pause()
		else:
			self.play()		
	
	def play(self):
		self.runMethod(self.PLAYER_IFACE, "Play")
	
	def pause(self):
		self.runMethod(self.PLAYER_IFACE, "Pause")
	
	def stop(self):
		self.runMethod(self.PLAYER_IFACE, "Stop")				
	
	def next(self):
		self.runMethod(self.PLAYER_IFACE, "Next")
		
	def previous(self):
		self.runMethod(self.PLAYER_IFACE, "Previous")		
		
	def fastForward(self):
		self.runMethod(self.PLAYER_IFACE, "FastForward")
		
	def rewind(self):
		self.runMethod(self.PLAYER_IFACE, "Rewind")
	
	def rewindFor30s(self):
		self.rewindForMs(30000)
	
	def fastForwardFor30s(self):
		self.fastForwardForMs(30000)
	
	def rewindForMs(self, msToRewind):
		# todo
		pass
	
	def fastForwardForMs(self, msToForward):
		'''
		status_before_action = self.getPlayingStatus()
		current_position = self.getPlayingPosition()
		target_position = current_position + msToForward
		self.fastForward()
	
		while self.getPlayingPosition() < target_position:
			time.sleep(0.1)
		
		if status_before_action == "playing":
			self.play()
		else:
			self.pause()
		'''
		# todo
		pass
		
	# CONTROL_IFACE METHODS (deprecated, but the only way to volume control)
	def volumeUp(self):
		self.runMethod(self.CONTROL_IFACE, "VolumeUp")
		
	def volumeDown(self):
		self.runMethod(self.CONTROL_IFACE, "VolumeDown")
	
	
		
