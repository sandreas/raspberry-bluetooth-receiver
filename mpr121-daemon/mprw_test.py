#!/usr/bin/env python
 
import sys, time, alsaaudio
from mpr_watcher import MprWatcher
from bt_control import BtControl
from net_device_control import NetDeviceControl
from process_builder import ProcessBuilder
from alsa_control import AlsaVolumeControl

from alsa_control import AlsaVolumeControl

cmd = ProcessBuilder()

wifi = NetDeviceControl("wlan0")
btplayer = BtControl()
volume = AlsaVolumeControl(cmd)


# volume.muteToggle()
# volume.decrease()


buttonFunctionMapping = {
	0: btplayer.rewindFor30s,
	1: volume.decrease,
	2: volume.muteToggle,
	3: volume.increase,
	4: btplayer.fastForwardFor30s,
	5: wifi.toggle,

	6: btplayer.previous,
	7: btplayer.rewind,
	8: btplayer.playPauseToggle,
	9: btplayer.stop,
	10: btplayer.fastForward,
	11: btplayer.next
}

#print btplayer.getPlayingStatus()
#btplayer.play()
	
watcher = MprWatcher(buttonFunctionMapping)
#print "running watcher"
watcher.run() 


'''
print output
print err
print rc
'''
#print controls_output


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




#volume = AlsaVolumeControl()

#alsaaudio.cards()
#alsaaudio.mixers()

#alsaaudio.Mixer("Master", 0)




#wifi.down()
#time.sleep(3);
#wifi.up()
#time.sleep(3);
# wifi.toggle()
# time.sleep(10)
# wifi.toggle()
# time.sleep(50)
# wifi.up()
# btplayer.connect()
'''
btplayer.play()
time.sleep(3)	
btplayer.pause()
'''
# print btplayer.getVolume()
# btplayer.setVolume(50)
# self.setProperty(self.TRANSPORT_IFACE, "Volume", )
# print btplayer.getVolume()


# btplayer.playPauseToggle()
# time.sleep(3)
# btplayer.playPauseToggle()
# time.sleep(3)
# btplayer.playPauseToggle()
# time.sleep(3)
# btplayer.playPauseToggle()
# time.sleep(3)


# /sys/class/net/eth0/operstate
'''
def firstButtonFunction(): #program does nothing as written
    print("First button released")

	
buttonFunctionMapping = {
	0:firstButtonFunction
}	
	
watcher = MprWatcher(buttonFunctionMapping)
watcher.run() 

'''