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

def check_selected_feed(feedList):

	streamSelected = 1
#	switch = 2	#detect buton input

	noOfCameras = len(feedList)
	if streamSelected > noOfCameras-1:
		streamSelected = 0
		return streamSelected
	else:
		return streamSelected

#   if switch > noOfCameras-1:
#		switch = noOfCameras-1
#	stream = feedList[0]['Stream']
#	return switch





########################### MAIN ######################################
def main():

	while True:
		#LCD Print connecting
		defaultGW = get_default_gateway() #dGW is also api server
		#ApiData= fetch_Camera_API('api.myjson.com/bins/l6j55') #http://myjson.com/l6j55 jason emulator
		ApiData = fetch_Camera_API('api.myjson.com/bins/m0k5t') #http://myjson.com/l6j55 jason emulator
		#print(ApiData)
		
		if ApiData == None:
			print("no api data, check connection and API again")
			#start again
		else:
			print("got API data, assign camera URLs")
			CamCount = Api_Object_Count(ApiData)	##count number of camears
			CamInfo={}	#diconatry
			CamInfo.clear()
			#fetch API Infomation
			for x in range(CamCount):		#get Cam Name and Stream
				CamInfo[x] = {}
				CamInfo[x]['Name'] = ApiData[x]['camera_name']
				CamInfo[x]['Stream'] = ApiData[x]['rtsp_link']
				print(CamInfo[x]['Name'])
				print(CamInfo[x]['Stream'])
			break



	selected_Stream = check_selected_feed(CamInfo)
	player1 = OMXPlayer(CamInfo[selected_Stream]['Stream'], args=['--live','-b', '--no-osd', '--threshold','0'])


	while True:
		try:
			if player1.playback_status() == Playing:
				selected_Stream = check_selected_feed(CamInfo)
				if selected_Stream != player1.get_source():
					player1.load(CamInfo[selected_Stream]['Stream'])


		except:
			print("not playing")
			##check connection and start again


#check selected stream
#start player
#check player is playing - if not check connection check api start again
#check switch - is the selected stream same as whats playing - yes do nothing - no stop and start






		player1.stop()
		break

		
		

			#print(ApiData[x]['id'])
			
			#print(ApiData[x]['camera_name'])
			#print(ApiData[x]['rtsp_link'])



#			print("\n", ApiData[0])
#			print(ApiData[0]['userId'])


			#kill while loop while testing






if __name__ == "__main__":	#main program loop
	main()


