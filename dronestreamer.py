#!/usr/bin/env python3
#import time
import os
import sys
#import socket, struct
#import signal
import requests
import json
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD

droneRxIP="api.myjson.com"
#api.myjson.com/bins/m0k5t
#apiURL="/bins/m0k5t"		#test with 2 working
apiURL="/bins/18fa25"		#test with 1 working 1 wrong url, siulates missing camera feed

GPIO.setmode(GPIO.BCM)     #use GPIO numbers

# Raspberry Pi pin configuration: GPIO numbers
ButtonPin=27
lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 4		##needs connecting to this pin if i want to control LCD  backlight

GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

#os.system("sudo fbi -T 1 --noverbose /home/pi/DronerStreamer/splash.png")  #backgroup picture

sleep(2)


#Check API Connection to Drone Fetch Json file and status code
def fetch_Camera_API(IPaddr, apiSyntax):
	#URL = "http://"+IPaddr
	URL = "http://"+IPaddr+apiSyntax	#build Api URL from IP
	lcd.clear()
	lcd.message('   CONNECTING   ')
	while True:
		print(URL)
		try:
			r = requests.get(URL)
			r.raise_for_status()
			if r.status_code == 200:
				r = json.loads(r.text)	#convert json to python values
				break
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.TooManyRedirects as errrd:
			print ("to many Redirects:",errrd)
		except requests.exceptions.RequestException as err:
			print ("Ops: Something Else",err)
		except:
			print("connection fault unknown")
		sleep(1)

	return r





def Stream_Selection_button(feedList,SelectedStream):
	noOfCameras = len(feedList)
	if SelectedStream > noOfCameras-1:
		SelectedStream = 0
		print("user selected:", SelectedStream)
		return SelectedStream
	else:
		print("user selected:", SelectedStream)
		return SelectedStream


def do_CheckCamUrlStatus(cam,streamNo):	#check camera stream is up by checking rtsp descibe
		streamStatus =os.system("curl -i "+cam[streamNo]['Stream'])
		if streamStatus == 0:
			return True
		else:
			return False

########################### MAIN ######################################
def main():
	
#	os.system("pkill omxplayer") #make sure OMXplayer isnt running
	userSelectedStream = 0
	GPIO.add_event_detect(ButtonPin, GPIO.RISING, bouncetime=500)	#set up button detechtion with debounce

	while True:	##main loop
		while True:


			ApiData = fetch_Camera_API(droneRxIP,apiURL)		#Get Camera list

			if ApiData == None:
				print("No API data, check connection and API again")
			else:
				CamCount = len(ApiData) 		#count number of camera objects in json file
				print("Camera Count: ",CamCount)	#count number of camears
				CamInfo={}
				CamInfo.clear()
				#fetch API Infomation
				for x in range(CamCount):		#get Cam Name, Stream and Drone Named
					CamInfo[x] = {}
					CamInfo[x]['Name'] = ApiData[x]['camera_name']
					CamInfo[x]['Stream'] = ApiData[x]['rtsp_link']
					CamInfo[x]['Flyer'] = ApiData[x]['flyer_name']
					print(CamInfo[x]['Name'], "-", CamInfo[x]['Stream'], "-", CamInfo[x]['Flyer'])
				break



		userSelectedStream = Stream_Selection_button(CamInfo,userSelectedStream)   ##check selected camera number is real



		while True:
			if GPIO.event_detected(ButtonPin):					#check button has been pressed
				print('Button pressed')
				userSelectedStream = userSelectedStream + 1			#increment selected stream
				userSelectedStream = Stream_Selection_button(CamInfo,userSelectedStream)

			try:
				if player1.is_playing() == True:
					if CamInfo[userSelectedStream]['Stream'] != player1.get_source():
						if(do_CheckCamUrlStatus(CamInfo, userSelectedStream)) == True:
							player1.load(CamInfo[userSelectedStream]['Stream'])
							lcd.clear()							#print message to LCD
							lcd.message("Streaming\n")
							lcd.message(CamInfo[userSelectedStream]['Name'])
						else:
							print("stream does not exist")
							break
					else:
						print("Currently Streaming",player1.get_source())



			except:
				if(do_CheckCamUrlStatus(CamInfo, userSelectedStream)) == True:
					player1 = OMXPlayer(CamInfo[userSelectedStream]['Stream'], args=['--live','-b', '--no-osd', '--threshold','0'])
					lcd.clear()							#print message to LCD
					lcd.message("Streaming\n")
					lcd.message(CamInfo[userSelectedStream]['Name'])
				else:
					print("stream does not exist")
					break




				#lcd.clear()							#print message to LCD
				#lcd.message("Streaming\n")
				#lcd.message(CamInfo[userSelectedStream]['Name'])


#			except:
#				print("player stopped / Video disconnected / stream unavaliable")
#				lcd.clear()
#				lcd.message("  Disconnected  \n")
#				lcd.message(" Player Stopped ")
#				try:
#					player1.quit()
#					break
#				except:
#					break

			sleep(.1)



if __name__ == "__main__":	#main program loop
	main()


