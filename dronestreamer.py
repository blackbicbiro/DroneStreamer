#!/usr/bin/env python3
import sys
import time
import requests
import threading
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep


STREAM_URI = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov'

player = OMXPlayer (STREAM_URI, args=['--live','-b', '--no-osd'])
print("hello")
print("hello")



print (player.is_playing())

sleep(4)

player.pause()
sleep(4)
player.play()
sleep(4)
print (player.get_source())
player.quit()
