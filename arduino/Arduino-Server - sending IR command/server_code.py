
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
    message = ser.readline().decode("utf-8")
    print('Arduino says:', message)
    time.sleep(0.5)
    dataSize = ser.readline()
    print('Data Size is:', int(dataSize))

    data = []
    x = 1
    while x <= int(dataSize):
        var = ser.readline().strip()
        var = var.decode("utf-8")
        data.append(int(var))
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
    print(str(data))
    code = str(data).replace(" ", "")
    Command.create(name=command_name, code=code, length=dataSize)
    return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())


@app.route('/sendOrDeleteCommand', methods=['POST'])
def sendCommandToArduino():
        command_id = request.form['id']
        action = request.form['action']

        if action == "send":
            command = Command.get(Command.id == command_id)
            data = command.code.strip('[]')
            #data = data.split(',')
            print(data)

            ser = serial.Serial("COM5", 9600)
            ser.timeout = 5
            connected = False
            while not connected:
                serin = ser.read()
                connected = True

            print("server size")
            print(len(data.split(',')))
            ser.write(b's')
            ser.write(str(len(data.split(','))).encode())
            var2 = ser.readline()
            print("arduino size ")
            print(var2)
            time.sleep(0.5)

            # print('unsigned int raw[', end="")
            # print(len(data), end="")
            # print('] = ', end="")
            # print('{ ', end="")
            # for x in range(len(data)):
            #     print(data[x].encode(), end="")
            #     print(',', end="")
            # print(' };')

            #for x in range(len(data)):
                #ser.write(data[x].encode())
                #time.sleep(0.3)
                #var = ser.readline()
                # print("next byte is:")
                # print(var)

            ser.write(data.encode())
            print(ser.readline())
            time.sleep(20)
            ser.close()

        else:
            command = Command.delete().where(Command.id == command_id)
            command.execute()

        return render_template('addCommand.html', title='Listening to Arduino', commands=Command.select())
