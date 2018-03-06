#!/bin/bash

CONFIG_FILE="/boot/config.txt"
KERNAL_FILE="/boot/cmdline.txt"
RC_LOCAL="/etc/rc.local"


#install packages
#apt-get update -y
#apt-get install python3-rpi.gpio -y
#apt-get install fbi -y
#apt-get install python3-pip -y
#apt-get install omxplayer -y
#apt-get update && sudo apt-get install -y libdbus-1{,-dev} -y
#sudo pip3 install requests
#sudo pip3 install omxplayer-wrapper




#setup ssh
if service ssh status | grep -q running;
then
	echo "ssh already running"
else
	touch /boot/ssh		#add ssh file to /boot/ to enable ssh on first startup
	echo "ssh will be enabled on the next boot"
fi



#set up GPU memory allocation to 128MB
if grep -q "gpu_mem=" $CONFIG_FILE; then
	sed -i '/gpu_mem/c\gpu_mem=128' $CONFIG_FILE
        echo "Set GPU memory to 128Mb"

else
	echo "gpu_mem=128" >> $CONFIG_FILE
	echo "Set GPU memory to 128Mb"
fi




#set HDMI output to CEA standard
if grep -q "hdmi_group=" $CONFIG_FILE;then
	 sed -i '/hdmi_group=/c\hdmi_group=1' $CONFIG_FILE
else
	echo "SET HDMI mode to CEA"
	echo "hdmi_group=1" >> $CONFIG_FILE
fi
#Set HDMI output to 1280x720p60
if grep -q "hdmi_mode=" $CONFIG_FILE;then
         sed -i '/hdmi_mode=/c\hdmi_mode=4' $CONFIG_FILE
else
        echo "SET HDMI output to 1200x720p50"
        echo "hdmi_mode=4" >> $CONFIG_FILE #set consumer electronics assosiati
fi
#hdmi signle boost
if grep -q "hdmi_group=" $CONFIG_FILE;then
         sed -i '/config_hdmi_boost=/c\config_hdmi_boost=4' $CONFIG_FILE
else
        echo "SET HDMI output to 1200x720p50"
        echo "config_hdmi_boost=4" >> $CONFIG_FILE #set consumer electronics assosiati
fi



#Disable screen blanking
if grep -q "consoleblank=" $KERNAL_FILE; then
	echo "edited console blank time to 0"
	sed -E -i 's/consoleblank=[0-9]+/consoleblank=0/' $KERNAL_FILE
else
	echo "added consoleblank=0 to" $KERNAL_FILE
	sed -i 's/$/ consoleblank=0/' $KERNAL_FILE
fi


#Disable pi logo blanking
if grep -q "logo.nologo" $KERNAL_FILE; then
	echo "logo.nologo already in file"
else
	echo "added logo.nologo to" $KERNAL_FILE
	sed -i 's/$/ logo.nologo/' $KERNAL_FILE
fi

#Disable pi boot color test
if grep -q "disable_splash=" $CONFIG_FILE; then
	echo "disable_splash=1 already in file"
	sed -E -i 's/disable_splash=[0-9]+/disable_splash=1/' $CONFIG_FILE
else
	echo "added disable_splash=1 to" $CONFIG_FILE
	sed -i 's/$/ disable_splash=1/' $CONFIG_FILE
fi




#Auto start script on boot

if grep -q "/usr/bin/python3 /home/pi/DronerStreamer/dronestreamer.py" $RC_LOCAL; then
	echo "script already in rc.local file"
else
	echo "added player script to" $RC_LOCAL
	sed -i '$i \/usr/bin/python3 /home/pi/DronerStreamer/dronestreamer.py \n' /etc/rc.local
fi

