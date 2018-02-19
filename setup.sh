#!/bin/bash

CONFIG_FILE="/boot/config.txt"
KERNAL_FILE="/boot/cmdline.txt"

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



#install packages
apt-get update -y
apt-get install python3-pip -y
apt-get install omxplayer -y
apt-get update && sudo apt-get install -y libdbus-1{,-dev} -y
pip3 install requests
pip3 install omxplayer-wrapper
