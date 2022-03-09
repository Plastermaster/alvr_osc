#~proudly copy and pasted together~
import os
import json
import websocket
import time
from pythonosc.udp_client import SimpleUDPClient

clear = lambda: os.system('cls')
clear()
def display_data(alvr_data):
	clear()
	print("Quest2 Battery		:",int(alvr_data["batteryHMD"]))
	print("Left controller		:",int(alvr_data["batteryLeft"]))
	print("Right controller	:",int(alvr_data["batteryRight"]))
	print("Quest2 FPS		:",float(alvr_data["clientFPS"]))
	print("Server FPS		:",float(alvr_data["serverFPS"]))
	print("\nCTRL+C to exit")

def send_osc(alvr_data): #sends data to the specified parameters
	client.send_message("/avatar/parameters/battery_hmd",int(alvr_data["batteryHMD"]))
	client.send_message("/avatar/parameters/battery_controller_left",int(alvr_data["batteryLeft"]))
	client.send_message("/avatar/parameters/battery_controller_right",int(alvr_data["batteryRight"]))
	client.send_message("/avatar/parameters/fps_quest",float(alvr_data["clientFPS"]))
	client.send_message("/avatar/parameters/fps_server",float(alvr_data["serverFPS"]))
	

def on_message(wsapp, message):
	#to trim off the timecode and unneeded characters
	message = message[27:]	
	message = message[:-1]	
	#turn whatever that mess of a string is into something usable
	temp = json.loads(message)
	#ignore the graph specific statistics
	if (temp["id"]) == "Statistics":
		alvr_data = temp["data"]	#unpack the nested json
#		print(alvr_data)			#optional, for debugging
		send_osc(alvr_data)			#gotta send it all to vrc
		display_data(alvr_data)		#give visual feedback

ip="127.0.0.1"
print("Starting OSC client and connecting to ALVR...\nIf ALVR is not running this script will close itself shortly.")

#createst osc client on the specified IP and port
client = SimpleUDPClient(ip, 9000) 
#connects to alvr and stays running
wsapp = websocket.WebSocketApp("ws://localhost:8082/api/log", on_message=on_message) 
wsapp.run_forever()
clear()
