#!/usr/bin/env python3
import time
import sys
import socket, struct
import signal
import requests
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep


#STREAM_URI = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov'
Stream_Url = 'rtsp://172.25.40.240/video1'


#get local IP and Default route IP

#build player instance
def startPlayer(Stream):
	playerName = OMXPlayer (Stream, args=['--live','-b', '--no-osd', '--threshold','0'])
	return playerName

def exit_streamer(player):
	try:
		player.quit()
		sys.exit()
	except:
		sys.exit("Exited OMXplayer and closing application")

def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))




def main():
	try:
		GWaddr = get_default_gateway_linux()
		print(GWaddr)
		player1 = startPlayer(Stream_Url)
		print(player1)
		print (player1.get_source())	#print current playing stream
		print (player1.is_playing())	#check if player is playing and print output

		while True:
			pass
	except KeyboardInterrupt:		#gracefull shutdown
		exit_streamer(player1)






if __name__ == "__main__":	#main program loop
	main()
