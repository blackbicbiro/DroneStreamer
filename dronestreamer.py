#!/usr/bin/env python3
import time
import os
import sys
import socket, struct
import signal
import requests
import json
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD


GPIO.setmode(GPIO.BCM)

# Raspberry Pi pin configuration:
ButtonPin=27
lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 4

GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


userSelectedStream = 0


os.system("sudo fbi -T 1 --noverbose /home/pi/DronerStreamer/splash.png")

sleep(2)

#TODO
#selectbutton press
#LCD display

#STREAM_URI = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov'
Stream_Url = 'rtsp://172.25.40.240/video1'
API_Url = 'https://jsonplaceholder.typicode.com/todos'



#Get default gateway from /proc/net/route
def get_default_gateway():
	GW = None
	lcd.clear()
	lcd.message('   CONNECTING   ')
	while GW == None:
		GW = os.popen("ip route | grep default | awk {'print$3'}").read()
		GW = GW.rstrip()
		if len(GW) == 0:
			GW = None
			sleep(1)
	return GW



#Fetch Json file and status code
def fetch_Camera_API(IPaddr):
	URL = "https://"+IPaddr
	#URL = "https://"+IPaddr+"/api/getVideoStreams"	#build Api URL from IP
	print(URL)
	try:
		r = requests.get(URL)
		r.raise_for_status()
	except requests.exceptions.HTTPError as errh:
		print ("Http Error:",errh)
		return None
	except requests.exceptions.ConnectionError as errc:
		print ("Error Connecting:",errc)
		return None
	except requests.exceptions.Timeout as errt:
		print ("Timeout Error:",errt)
		return None
	except requests.exceptions.TooManyRedirects as errrd:
		print ("to many Redirects:",errrd)
		return None
	except requests.exceptions.RequestException as err:
		print ("OOps: Something Else",err)
		return None
	except:
		print("connection fault unknown")
		return None

	if r.status_code == 200:
		r = json.loads(r.text)	#convert json to python values
	else:
		r = None

	return r




def Stream_Selection_button(feedList):
	#streamSelected = 0		#temp untill button code works
	global userSelectedStream
	noOfCameras = len(feedList)
	if userSelectedStream > noOfCameras-1:
		userSelectedStream = 0
		return userSelectedStream
	else:
		return userSelectedStream


########################### MAIN ######################################
def main():
#	os.system("pkill omxplayer") #make sure OMXplayer isnt running
	global userSelectedStream
	GPIO.add_event_detect(ButtonPin, GPIO.RISING, bouncetime=500)	#set up button detechtion with debounce

	while True:	##main loop
		while True:
			#LCD Print connecting
			defaultGW = get_default_gateway() #dGW is also api server
			ApiData = fetch_Camera_API('api.myjson.com/bins/m0k5t') #http://myjson.com/l6j55 jason emulator

			if ApiData == None:
				print("No API data, check connection and API again")
			else:
				CamCount = len(ApiData) #count number of camera objects in json file
				print("Camera Count: ",CamCount)	##count number of camears
				CamInfo={}	#diconatry
				CamInfo.clear()
				#fetch API Infomation
				for x in range(CamCount):		#get Cam Name and Stream
					CamInfo[x] = {}
					CamInfo[x]['Name'] = ApiData[x]['camera_name']
					CamInfo[x]['Stream'] = ApiData[x]['rtsp_link']
					CamInfo[x]['Flyer'] = ApiData[x]['flyer_name']
					print(CamInfo[x]['Name'], "-", CamInfo[x]['Stream'], "-", CamInfo[x]['Flyer'])
				break

		Stream_Selection_button(CamInfo)   ##check selected camera number is real
		try:
			player1 = OMXPlayer(CamInfo[userSelectedStream]['Stream'], args=['--live','-b', '--no-osd', '--threshold','0'])
		except:
			print("Player failed to start")
		print("started player:",CamInfo[userSelectedStream]['Name'],"-",CamInfo[userSelectedStream]['Stream'])
		lcd.clear()
		lcd.message("Streaming\n")
		lcd.message(CamInfo[userSelectedStream]['Name'])


		while True:
			try:
				if player1.playback_status() == "Playing":
					print("players stream",player1.get_source())
					Stream_Selection_button(CamInfo)
					print("got here")
					print(CamInfo[userSelectedStream])
					if GPIO.event_detected(ButtonPin):		##check button has been pressed
   						print('Button pressed')
   						userSelectedStream = userSelectedStream + 1
					if CamInfo[userSelectedStream]['Stream'] != player1.get_source(): # check to see if the selected stream is the same that is plaing
						print("i am here")
						player1.load(CamInfo[userSelectedStream]['Stream'])
						lcd.clear()
						lcd.message("Streaming\n")
						lcd.message(CamInfo[userSelectedStream]['Name'])

			except:
				print("player stopped / Video disconnected / stream unavaliable")
				try:
					player1.quit()
					break
				except:
					break
				#check connection and start again
			#for testing purpses
			#print("stream selected before increment:", userSelectedStream)
			#userSelectedStream = userSelectedStream + 1
			print("stream selection number: ",userSelectedStream)
			sleep(.1)



if __name__ == "__main__":	#main program loop
	main()


