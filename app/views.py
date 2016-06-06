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

# ser = serial.Serial()
# #ser.port = '\\.\COM5'
# ser.port = "COM5"
# ser.baudrate= 9600
# ser.timeout = 2
# ser.open()

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
    # return "playing music..."


@app.route('/timers')
def timers():
    timer = Timer.delete().where(Timer.end_time < datetime.now())
    timer.execute()
    return render_template('timers.html', title='Timers', timers=Timer.select())


@app.route('/setTimer', methods=['POST'])
def setTimer():
    str_time = request.form['time']
    hours = int(str_time[:-3])
    minuts = int(str_time[3:])
    timer_date = datetime.now().replace(hour=hours, minute=minuts, second=0)
    Timer.create(set_time=datetime.now(), end_time=timer_date)
    time_to_wait_in_seconds = (timer_date - datetime.now()).seconds
    threading.Timer(time_to_wait_in_seconds, turnMusicOn).start()
    return render_template('timers.html', title='Timers', timers=Timer.select())


@app.route('/subscribe', methods=['POST', 'GET'])
def subscribe():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        if endpoint.startswith('https://android.googleapis.com/gcm/send'):
            endpointParts = endpoint.split('/')
            registrationId = endpointParts[len(endpointParts) - 1]
            global registrationIds
            if registrationIds.count(registrationId) == 0:
                registrationIds.append(registrationId)
                # threading.Timer(10, pushNotification).start()
                # endpoint = 'https://android.googleapis.com/gcm/send'
        print(len(registrationIds))
        print(registrationId)
        return "registration succeeded"
    else:
        return render_template('subscribe.html', title='Subscribe')


@app.route('/addCommand')
def addCommand():
    return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())


@app.route('/receiveCommandFromArduino', methods=['POST'])
def recieveCommandFromArduino():
    #    ser.write(b'r')
    #
    #    count = ser.readline().decode("utf-8")  #reads first line
    #    print ('Arduino says:', count)
    #    time.sleep(3)
    #    dataSize = ser.readline() #reads 1 bytes(size of data)
    #    print('Data Size is:', int(dataSize))
    #
    #    data = []
    #    x = 1
    #    while x <= int(dataSize):
    #        data.append(ser.readline().strip())
    #        x = x + 1
    #
    #    print('unsigned int raw[',end="")
    #    print(int(dataSize),end="")
    #    print('] = ',end="")
    #    print('{ ',end="")
    #    for x in range(int(dataSize)-1):
    #        print(data[x], end="")
    #        print(',',end="")
    #    print(' };')

    command_name = request.form['command']
    Command.create(name=command_name)
    return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())


@app.route('/sendCommandToArduino', methods=['POST'])
def sendCommandToArduino():
    action_name = request.form.get('send', "delete")
    if action_name =="send":
        command_id = request.form['id']
        #command = Command.get(Command.id == command_id)
    else:
        command_id = request.form['id']
        command = Command.delete().where(Command.id == command_id)
        command.execute()
    return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())



@app.route('/deleteArduinoCommand', methods=['POST'])
def deleteArduinoCommand():
    command_id = request.form['id']
    command = Command.delete().where(Command.id == command_id)
    command.execute()
    return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())
