#!/bin/bash

CONFIG_FILE="/boot/config.txt"


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
