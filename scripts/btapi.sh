#!/bin/bash
# e.g. 00:AA:AA:AA:AA:AA is replaced with 00_AA_AA_AA_AA_AA
btapi_device_raw=$(sudo head -n1 bluez-autoconnect-device-history)
export btapi_device=$(sed 's/:/_/g' <<< $btapi_device_raw)
export btapi_functions=("connect" "play" "pause" "previous" "next" "volumeUp" "volumeDown" "rewind" "fastForward" "stepBack" "stepForward")

fn_name="$1"
btapi_fn_name="btapi_$fn_name"


dbus_bluez_call() {
	echo "dbus_bluez_call $btapi_device $1 $2"
	if [ "$2" == "" ]; then
		sudo dbus-send --system --type=method_call --dest=org.bluez "/org/bluez/hci0/dev_${btapi_device}" "org.bluez.${1}" 
	else 
		sudo dbus-send --system --type=method_call --dest=org.bluez "/org/bluez/hci0/dev_${btapi_device}/$2" "org.bluez.${1}" 
	fi
}

usage() {
	echo "btapi.sh [device] [${btapi_functions[@]}]"
}

btapi_connect() { dbus_bluez_call Device1.Connect; }
btapi_play() { dbus_bluez_call MediaPlayer1.Play player0; }
btapi_pause() { dbus_bluez_call MediaPlayer1.Pause player0; }
btapi_next() { dbus_bluez_call MediaPlayer1.Next player0; }
btapi_previous() { dbus_bluez_call MediaPlayer1.Previous player0; }
btapi_fastForward() { dbus_bluez_call MediaPlayer1.FastForward player0; }
btapi_rewind() { dbus_bluez_call MediaPlayer1.Rewind player0; }

btapi_volumeUp() { dbus_bluez_call MediaControl1.VolumeUp; }
btapi_volumeDown() { dbus_bluez_call MediaControl1.VolumeDown; }

if [ "$fn_name" == "" ]; then
	usage
else
	echo $fn_name
	$btapi_fn_name
fi
