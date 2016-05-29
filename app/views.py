from app import *
from flask import redirect, request, render_template
import os
import threading
from datetime import datetime
from datetime import timedelta
import serial
from gcm import GCM 

global registrationIds
registrationIds = []
global API_KEY
API_KEY = "AIzaSyCZ31BrLMpWpdwsKG9nqKQnDpLoERZnvEc"

@app.route('/push')
def push():
    global API_KEY
    gcm = GCM(API_KEY)
    data = {'param1': 'value1', 'param2': 'value2'}

    # Downstream message using JSON request
    global registrationIds
    reg_ids = registrationIds
    response = gcm.json_request(registration_ids=reg_ids, data=data)
    
    return "pushed :-)"

def writeToFile(s):
	 file_path = os.path.normpath('app/static/file.txt')
	 file = open(file_path, 'w')
	 file.write(s)
	 num = file.close()
	 print(num)

@app.route('/')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/addCommand')
def addCommand():
    return render_template('addCommand.html', title='Add Command')

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

@app.route('/timers')
def timers():
    return render_template('timers.html', title='Timers', timers=Timer.select())

@app.route('/setTimer', methods = ['POST'])
def setTimer():
    str_time = request.form['time']
    hours = int(str_time[:-3])
    minuts = int(str_time[3:])
    timer_date = datetime.now().replace(hour=hours, minute=minuts, second=0)
    Timer.create(set_time=datetime.now(), end_time=timer_date)
    time_to_wait_in_seconds = (timer_date - datetime.now()).seconds
    threading.Timer(time_to_wait_in_seconds, turnMusicOn).start()
    return render_template('timers.html', title='Timers', timers=Timer.select())

@app.route('/subscribe', methods = ['POST', 'GET'])
def subscribe():
    if request.method=='POST':
        endpoint = request.form['endpoint']
        if endpoint.startswith('https://android.googleapis.com/gcm/send'):
            endpointParts = endpoint.split('/')
            registrationId = endpointParts[len(endpointParts) - 1]
            global registrationIds
            if registrationIds.count(registrationId) == 0:
                registrationIds.append(registrationId)
            #threading.Timer(10, pushNotification).start()
            #endpoint = 'https://android.googleapis.com/gcm/send'
        print(len(registrationIds))
        print(registrationId)
        return "registration succeeded"
    else:
        return render_template('subscribe.html', title='Subscribe')
        
@app.route('/listeningToArduino', methods=['POST'])
def listeningToArduino():
    return render_template('listeningToArduino.html', title='Listening to Arduino')
