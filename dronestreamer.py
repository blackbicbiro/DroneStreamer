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


#1. check connection to GW
	#loop
		#wait 1 second
#2. check api for camera attached
#3. check switch position
#4. start player
#6. update display
#7. loop
	#1. check player is still playing
		# if player fails start from  begining
	#2. check switch position
		# stop player start again fro begining


#STREAM_URI = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov'
Stream_Url = 'rtsp://172.25.40.240/video1'
API_Url = 'https://jsonplaceholder.typicode.com/todos'



#Exit player and application
def exit_streamer(player):
	try:
		player.quit()
		sys.exit()
	except:
		sys.exit("Exited OMXplayer and closing application")


def signal_handler(signal, frame):
	print("\nprogram exiting gracefully")
	sys.exit(0)




#Get default gateway from /proc/net/route
def get_default_gateway():
	GW = None
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
	#print("\n",r.status_code)	#print status code only

	#data = json.loads(r.text)
#	print(len(data))
#	print(data)
#	print(data[0]['userId'])  #print spercific data from dictionar




def Api_Object_Count(data):
	count = len(data)
	print(count)
	
	return count




########################### MAIN ######################################
def main():

	while True:

		defaultGW = get_default_gateway()
		ApiData = fetch_Camera_API('jsonplaceholder.typicode.com/posts')   #test api url
		
		#print(ApiData)
		
		if ApiData == None:
			print("no api data")
			#start again
		else:
			print("got API data, assign camera URLs")
			CamCount = Api_Object_Count(ApiData)	##count number of camears
			
			CamInfo={}	#diconatry
		for x in range(CamCount):		#get Cam Name and Stream
			CamInfo[x] = {}
			CamInfo[x]['Name'] = ApiData[x]['id']
			CamInfo[x]['Stream'] = ApiData[x]['title']
			
			print(CamInfo[x]['Name'])
			print(CamInfo[x]['Stream'])


			#print(ApiData[x]['id'])
			
			#print(ApiData[x]['camera_name'])
			#print(ApiData[x]['rtsp_link'])



#			print("\n", ApiData[0])
#			print(ApiData[0]['userId'])





		break	#kill while loop while testing


	#print(ApiData.status_code)
	#print(ApiData.text)


	#player1 = OMXPlayer (Stream_Url, args=['--live','-b', '--no-osd', '--threshold','0'])
	#print(player1.is_playing())
	#print(player1.identity())
	#sleep(2)
	#player1.quit()


	#PrintLCD"Waiting for connection"
	#get_defult_gateway():
	#PrintLCD "IP Address = xxx.xxx.xxx.xxx"

	#player2 = OMXPlayer(Stream_Url, dbus_name='org.mpris.MediaPlayer2.omxplayer1	')

	#print(player2.identity())
	#player1.stopEvent = print("hello")
	#sleep(2)
	#player2.quit()




if __name__ == "__main__":	#main program loop
	main()








#notes and work in progress
#	while Te:
#		try:
#			player1.get_source()
#		except:
#			print("broken")
#		signal.signal(signal.SIGINT, signal_handler, player1)


		#check if player is running
			#no = check gateway, fetch api, map api to switch, check switch postion, update LCD
			#yes = check switch hasnt changed
		#default_GW = get_default_gateway_linux()
		#print(default_GW)
		#API_info = fetch_API_cameras(API_Url)
		#print(API_info)
		#GWaddr = get_default_gateway_linux()
		#print(GWaddr)
		#player1 = startPlayer(Stream_Url)
		#print player1)
		#print (player1.get_source())	#print current playing stream
		#print (player1.is_playing())	#check if player i