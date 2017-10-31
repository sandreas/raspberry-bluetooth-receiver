#!/usr/bin/env python 
import dbus

import dbus
bus = dbus.SystemBus()
#hci0 = bus.get_object('org.bluez', '/org/bluez/hci0')
#props = dbus.Interface(hci0, 'org.freedesktop.DBus.Properties')
#props.Set('org.bluez.Adapter1', 'Discoverable', True)


# works
#path = "/org/bluez/hci0/dev_04_DB_56_83_DA_3F/player0"
#obj = bus.get_object("org.bluez", path)
#props = dbus.Interface(obj, 'org.freedesktop.DBus.Properties')
#print props.Get('org.bluez.MediaPlayer1', 'Position')

SERVICE_NAME = "org.bluez"
MEDIA_IFACE = SERVICE_NAME + '.Media1'
AGENT_IFACE = SERVICE_NAME + '.Agent1'
ADAPTER_IFACE = SERVICE_NAME + ".Adapter1"
DEVICE_IFACE = SERVICE_NAME + ".Device1"
PLAYER_IFACE = SERVICE_NAME + '.MediaPlayer1'
TRANSPORT_IFACE = SERVICE_NAME + '.MediaTransport1'
CONTROL_IFACE = SERVICE_NAME + '.MediaControl1'

manager = dbus.Interface(bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")
objects = manager.GetManagedObjects()

player_path = None
transport_path = None
control_path = None
for path, interfaces in objects.iteritems():
  if PLAYER_IFACE in interfaces:
    player_path = path
  if TRANSPORT_IFACE in interfaces:
    transport_path = path
  if CONTROL_IFACE in interfaces:
    control_path = path

print player_path
print transport_path
print control_path

player = bus.get_object("org.bluez", player_path)
control = bus.get_object("org.bluez", control_path)

# works
#player.Play(dbus_interface=PLAYER_IFACE)

# control.VolumeUp(dbus_interface=CONTROL_IFACE)
# playerProps = dbus.Interface(player, "org.freedesktop.DBus.Properties")
#playerStatus = playerProps.Get(PLAYER_IFACE, "Status")
#playerAll = playerProps.GetAll(PLAYER_IFACE)

#controlProps = dbus.Interface(control, "org.freedesktop.DBus.Properties")

#print controlProps.GetAll(CONTROL_IFACE)

#for service in dbus.SystemBus().list_names():
#    print(service)

#bus = dbus.SystemBus()
#path = "/org/bluez/hci0/dev_04_DB_56_83_DA_3F/player0"
#obj = bus.get_object("org.bluez", path)
#mp = dbus.Interface(obj, "org.bluez.MediaPlayer1")
#
#prop = dbus.Interface(bus.get_object("org.bluez", obj),
#						"org.freedesktop.DBus.Properties")
#
#properties = prop.GetAll("org.bluez.MediaPlayer1")
##mp.Play()
#print properties
#

#mp = dbus.Interface(bus.get_object("org.bluez", obj),
#						"org.bluez.MediaPlayer1")
#mp.Play()
