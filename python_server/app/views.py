from app import app
from flask import redirect, request
import os
import threading
from datetime import datetime
from datetime import timedelta

def writeToFile(s):
	 file_path = os.path.normpath('app/static/file.txt')
	 file = open(file_path, 'w')
	 file.write(s)
	 num = file.close()
	 print(num)

@app.route('/')
@app.route('/index')
def index():
	return app.send_static_file('index.html')
@app.route('/timer')
def timer():
	return app.send_static_file('timer.html')
@app.route('/lightsOn', methods=['POST'])
def lightsOn():
	writeToFile("1")
	return "lights on"
@app.route('/lightsOff', methods=['POST'])
def lightsOff():
	writeToFile("0")
	return "lights off"
@app.route('/playMusic', methods=['POST'])
def turnMusicOn():
    file_path = os.path.normpath('app/static/music.mp3')
    os.startfile(file_path)
    return "playing music..."
@app.route('/setTimer', methods = ['POST'])
def setTimer():
    str_time = request.form['time']
    hours = int(str_time[:-3])
    minuts = int(str_time[3:])
    timer_date = datetime.now().replace(hour=hours, minute=minuts, second=0)
    time_to_wait_in_seconds = (timer_date - datetime.now()).seconds
    threading.Timer(time_to_wait_in_seconds, turnMusicOn).start()
    return "Time Was Set..."	
@app.route('/pushNotification', methods=['POST'])
def pushNotification():
    endpoint = request.form['endpoint']
    if endpoint.startswith('https://android.googleapis.com/gcm/send'):
        endpointParts = endpoint.split('/')
        registrationId = endpointParts[len(endpointParts) - 1]
        endpoint = 'https://android.googleapis.com/gcm/send'
