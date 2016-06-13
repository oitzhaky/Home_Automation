from app import *
from flask import redirect, request, render_template
import os
import threading
from datetime import datetime
from datetime import timedelta
import serial
from gcm import GCM
import time

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
    return render_template('index.html', title='Home Page', first_time=True)


@app.route('/lightsOn', methods=['POST'])
def lightsOn():
    writeToFile("1")
    return render_template('index.html', title='Home Page')


@app.route('/lightsOff', methods=['POST'])
def lightsOff():
    writeToFile("0")
    return render_template('index.html', title='Home Page')


@app.route('/playMusic', methods=['POST'])
def turnMusicOn():
    file_path = os.path.normpath('app/static/music.mp3')
    os.startfile(file_path)
    return render_template('index.html', title='Home Page')


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


@app.route('/setAlarm')
def setAlarm():
    threading.Timer(0, motionDetector).start()
    return render_template('index.html', title='Home Page')

@app.route('/motionDetector')
def motionDetector():
    ser = serial.Serial('COM5', 9600)
    ser.timeout = 5
    connected = False

    while not connected:
        serin = ser.read()
        connected = True

    ser.write(b'm')

    print('Serial Opened')
    while 1:
        print('before line')
        line = ser.readline().decode("utf-8")
        print(line)
        if line == "Intruder detected":
            file_path = os.path.normpath('app/static/music.mp3')
            os.startfile(file_path)


@app.route('/addCommand', methods=['POST', 'GET'])
def addCommand():
    return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())


@app.route('/receiveCommandFromArduino', methods=['POST'])
def recieveCommandFromArduino():
    ser = serial.Serial('COM5', 9600)
    ser.timeout = 5
    connected = False

    while not connected:
        serin = ser.read()
        connected = True

    print('Arduino is connected')
    time.sleep(2)
    print('Arduino starts listening...')

    print('Server is sending a trigger command...')
    ser.write(b'r')
    time.sleep(0.5)
    count = ser.readline().decode("utf-8")
    print('Arduino says:', count)
    time.sleep(0.5)
    dataSize = ser.readline()
    print('Data Size is:', int(dataSize))

    data = []
    x = 1
    while x <= int(dataSize):
        data.append(ser.readline().strip())
        x = x + 1

    print('closing port')
    ser.close()

    print('unsigned int raw[', end="")
    print(int(dataSize), end="")
    print('] = ', end="")
    print('{ ', end="")
    for x in range(int(dataSize) - 1):
        print(data[x], end="")
        print(',', end="")
    print(' };')

    command_name = request.form['command']
    code = str(data)
    Command.create(name=command_name, code=code, length=dataSize)
    return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())


@app.route('/sendOrDeleteCommand', methods=['POST'])
def sendCommandToArduino():
        command_id = request.form['id']
        action = request.form['action']
        if action == "send":
            command = Command.get(Command.id == command_id)
            data = command.code.split(',')

            ser = serial.Serial("COM5", 9600)
            ser.timeout = 5
            connected = False

            while not connected:
                serin = ser.read()
                connected = True

            var = command.length
            ser.write(b's')
            ser.write(str(var).encode())
            time.sleep(0.5)

            print('unsigned int raw[', end="")
            print(command.length, end="")
            print('] = ', end="")
            print('{ ', end="")
            for x in range(command.length - 1):
                print(data[x], end="")
                print(',', end="")
            print(' };')

            for x in range(command.length - 1):
                ser.write(str(data[x]).encode())
                time.sleep(0.5)

            ser.close()

        else:
            command = Command.delete().where(Command.id == command_id)
            command.execute()

        return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())
