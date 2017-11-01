# raspberry-bluetooth-receiver
This repository contains scripts, tools and documentation for creating a bluetooth receiver with raspberry pi zero w or raspberry pi 3.

# Hardware

The repository is designed for the following hardware (links to amazon):

## Raspberry PI Zero W

### Required Hardware
- <a href="https://www.amazon.de/exec/obidos/ASIN/B07231SHZB/wwwgeschenke-inspiration-21" target="_blank">Raspberry PI Zero W</a>
- [Pimoroni Phat DAC](https://www.amazon.de/exec/obidos/ASIN/B019U9VC9E/wwwgeschenke-inspiration-21)
- [PI Zero Case](https://www.amazon.de/exec/obidos/ASIN/B01FHDXNNU/wwwgeschenke-inspiration-21)

### Optional Hardware
- [Capacitive Touch Sensor](https://www.amazon.de/exec/obidos/ASIN/B00SK8PVNA/wwwgeschenke-inspiration-21)
- [Breadboard 70x30mm](https://www.amazon.de/exec/obidos/ASIN/B076N6M6RB/wwwgeschenke-inspiration-21)


## Raspberry PI 3 (alternative)

### Required Hardware
- [Raspberry PI 3](https://www.amazon.de/exec/obidos/ASIN/B07231SHZB/wwwgeschenke-inspiration-21)
- [PI 3 Case](https://www.amazon.de/exec/obidos/ASIN/B00MQLB1N6/wwwgeschenke-inspiration-21)


## Other interesting stuff
- [Pi Cap](https://www.amazon.de/exec/obidos/ASIN/B06XWCC18F/wwwgeschenke-inspiration-21)
- [Electric Paint](https://www.amazon.de/exec/obidos/ASIN/B00CSMDT8S/wwwgeschenke-inspiration-21)
- [Touch screen](https://www.amazon.de/exec/obidos/ASIN/B06X191RX7/wwwgeschenke-inspiration-21)


## Features

- Smallest possible homebrew bluetooth receiver
- Controllable via buttons / touch screen (Play, Pause, Next, Previous, Volume, etc.)
- Auto reconnect the last connected bluetooth device
- TODO: Airplay Support (bluetooth and airplay cannot be used together*)
- TODO: USB Port for Playing MP3
- TODO: FM Transmitter via GPIO

* Raspberry pi zero w or raspberry pi 3 have a single chip for bluetooth and wifi. Unfortunately at the moment it is not possible to get bluetooth audio and wifi work together without problems (bluetooth audio works, but with bad quality and lags - I'm not sure if this is a driver or hardware issue).

## Soldering PHAT DAC

PHAT DAC is a higher quality audio hat for raspberry pi zero, that is relatively cheap, but worth the money. In order save space and use the case mentioned in the hardware recommendations, you could solder the PHAT DAC directly on the pins: 

- todo: picture

Now drill a hole for the audio jack in the top of the case and see, if everything fits.

## Soldering Adafruit 12-Key Capacitive Touch Sensor

- todo: describe installation of touch sensor

# Setup

Download the latest release of Raspian Lite (https://www.raspberrypi.org/downloads/raspbian/) and flash it to your sd card.
Before removing the card, be sure to enable ssh and wifi:

## Enable SSH
Open the `/boot` partition of the sd card and create an empty file named `ssh`. That's it, ssh should be enabled on first boot.

## Enable Wifi

Open the `/boot` partition of the sd card and create a file named `wpa_supplicant.conf` with following content:
country=<your two letter country code - e.g. DE for germany>
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="<your wifi name (SSID)>"
	psk="<your password>"
}

## Enable overclocking (optional)

For raspberry pi zero (w) you could use following overclocking settings to improve performance, if you use at least passive cpu cooling.

Open the `/boot` partition of the sd card and append following to your `config.txt`:

```
arm_freq=1000
gpu_freq=500
core_freq=500
sdram_freq=500
sdram_schmoo=0x02000020
over_voltage=2
sdram_over_voltage=2
```

# First boot and initial setup

Unmount your sd card and insert it into the raspberry pi, then power on
First boot should resize the partitions, second boot should provide you a login prompt.

Use following credentials (if you are not using ssh, note that the `y` in raspberry sometimes can be a `z` depending on the used keyboard layout):

```
Username: pi
Password: raspberry
```

## Install PHAT DAC drivers

To install the PHAT DAC and disable internal audio, just run this command

```
curl https://get.pimoroni.com/phatdac | bash
```

and follow the instructions. To test, if your audio is working, plugin a headphone or speaker and run

```
speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
```

You should hear a voice saying "Front - Center". Press CTRL+C to quit the test.

## Preparation

```
apt install -y git
cd /home/pi
git clone https://github.com/sandreas/raspberry-bluetooth-receiver
```


## Bluetooth audio

Bluetooth on Linux is tricky - especially when using audio. So, before you begin, you should know some things about the raspberry pi, bluetooth and audio:

- bluetooth audio and wifi won't work together - see `Features` for details
- to use bluetooth with audio, you will need `bluez` (linux bluetooth stack), `pulseaudio` (linux sound server) and `alsa` (Advanced Linux Sound Architecture) to work together
- bluez / pulseaudio is unter heavy development - api is kind of limited and changes are likely, so this docs might be out of date soon
- to manage, connect and trust devices, you could use `bluetoothctl`, but beware - most of the commands are used async, automation and shell usage is tricky
- pulseaudio can be configured for high quality audio, but raspberry pi zero w does not perform well enough to provide best quality - see `audio qualiy`

So the principle is simple:

- Pair and trust a bluetooth device
- Let pulseaudio/alsa create an extra audio sink for the bluetooth device
- Create a loopback device for redirecting the input from the bluetooth audio sink to the audio jack (via dbus rule)
- Remove the loopback device when disconnecting the bluetooth device

### Audio quality

The performance of the raspberry pi zero w is very limited. Therefore you cannot use the best audio quality settings possible - but you can improve the quality by using this settings (gets most of PulseAudio):

```
# /etc/pulse/daemon.conf
resample-method =  ffmpeg
enable-remixing = no
enable-lfe-remixing = no
default-sample-format = s32le
default-sample-rate = 192000
alternate-sample-rate = 176000
default-sample-channels = 2
```

### Package installation

```
# Install BlueZ-5  and PulseAudio-5 with Bluetooth support:
apt --no-install-recommends install pulseaudio pulseaudio-module-bluetooth bluez bluez-firmware
```

### Configuring pulse


```
# granting permissions
adduser root pulse-access
adduser pi pulse-access
```

```
# Authorize PulseAudio run as user pulse use BlueZ D-BUS
cat <<EOF >/etc/dbus-1/system.d/pulseaudio-bluetooth.conf
<busconfig>

  <policy user="pulse">
    <allow send_destination="org.bluez"/>
  </policy>

</busconfig>
EOF
```

```
# Load  Bluetooth discover module in SYSTEM MODE
cat <<EOF >> /etc/pulse/system.pa
#
### Bluetooth Support
.ifexists module-bluetooth-discover.so
load-module module-bluetooth-discover
.endif
EOF
```

```
# Create a systemd service for running pulseaudio in System Mode as user "pulse".
cat <<EOF >/etc/systemd/system/pulseaudio.service
[Unit]
Description=Pulse Audio

[Service]
Type=simple
ExecStart=/usr/bin/pulseaudio --system --disallow-exit --disable-shm --exit-idle-time=-1

[Install]
WantedBy=multi-user.target
EOF
```


```
# reload daemons
systemctl daemon-reload
systemctl enable pulseaudio.service
```

```
# start pulseaudio service
systemctl start pulseaudio.service
```

### Connecting a bluetooth audio device

```
# restart bluetooth service
systemctl restart bluetooth

# to pair a bluetooth device, run bluetoothctl, which opens an extra command shell 
# don't forget to take a look at the pairing status of your device
bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
[bluetooth]# pair <device mac, e.g. DE:AD:BE:EF:DE:AD>
[bluetooth]# trust <device mac, e.g. DE:AD:BE:EF:DE:AD>
[bluetooth]# connect <device mac, e.g. DE:AD:BE:EF:DE:AD>
[bluetooth]# exit
```


### Adding a udev rule for auto loopback

Before you add a udev rule, there is an issue, you should know about. On current raspbian releases, udev does not accept rules because of using a readonly filesystem, that is caused by udev not recognizing the rw-state of the filesystem. This can be fixed by adding following to you `/etc/rc.local`:

```
# /etc/rc.local - bottom
# added
service udev restart
exit 0 # this line should already exist
```

Now add a rule that runs a script everytime a bluetooth device gets connected
```
# /etc/udev/rules.d/99-com.rules
SUBSYSTEM=="input", GROUP="input", MODE="0660"
#added
KERNEL=="input[0-9]*", RUN+="/home/pi/raspberry-bluetooth-receiver/scripts/udev-bluetooth"

SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0660"
```


# to connect last device on startup, add a reboot cronjob as root
```
sudo -s
crontab -e

#added
@reboot /home/pi/raspberry-bluetooth-receiver/scripts/autoconnect-bluetooth > /home/pi/raspberry-bluetooth-receiver/logs/autoconnect-bluetooth.log 2>&1 &
```


# Resources and links

## Scripts and tutorials
- USB Audio: https://gist.github.com/oleq/24e09112b07464acbda1
- bluez5 (current): https://github.com/davidedg/NAS-mod-config/blob/master/bt-sound/bt-sound-Bluez5_PulseAudio5.txt
- bluez4 (old): https://www.raspberrypi.org/forums/viewtopic.php?f=38&t=68779
- All-in-one-script: https://github.com/BaReinhard/Super-Simple-Raspberry-Pi-Audio-Receiver-Install (did not work for me, but it is a nice resource for ideas)

## API Docs
- Bluez media api: https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/media-api.txt

