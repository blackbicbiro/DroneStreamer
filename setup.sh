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
#Disable screen blanking
if grep -1 "consoleblank" $KERNAL_FILE; then
	echo "edited console blank time to 0"
	sed -i 's/consoleblank=[0-9]/consoleblank=0/' $KERNAL_FILE
else
	echo "added consoleblank=0 to" $KERNAL_FILE
	sed -i 's/$/ consoleblank=0/' $KERNAL_FILE
fi



#install packages
apt-get update -Y
apt-get install python3-pip -y
apt-get install omxplayer -y
pip3 install requests
pip3 install omxplayer-wrapper
