

## import the serial library
import serial
import time

## Boolean variable that will represent 
## whether or not the arduino is connected
connected = False

## open the serial port that your ardiono 
## is connected to.
ser = serial.Serial("COM3", 9600)
ser.timeout = 2;

## loop until the arduino tells us it is ready
## can be either with time.sleep(2)
while not connected:
    serin = ser.read()
    connected = True

print('Arduino is connected!')
time.sleep(2)

print('~~~~Arduino starts listening~~~~')

## Tell the arduino to send data!
print('Server is sending command on serial...')
ser.write(b'r')

time.sleep(2)

count = ser.readline().decode("utf-8")  #reads first line
print ('Arduino says:', count)
time.sleep(3)
dataSize = ser.readline() #reads 1 bytes(size of data)
print('Data Size is:', int(dataSize))

data = []
x = 1

while x <= int(dataSize):
    data.append(ser.readline().strip())
    x = x + 1

print('unsigned int raw[',end="")
print(int(dataSize),end="")
print('] = ',end="")
print('{ ',end="")
for x in range(int(dataSize)-1):
    print(data[x], end="")
    print(',',end="")
print(' };')

# print('unsigned int raw[',end="")
# print(int(dataSize),end="")
# print('] = ',end="")
# print('{ ',end="")
# #printing the array of data
# for num in range(1, int(dataSize)):
#     #print(int.from_bytes(ser.read(), byteorder='big'))
#     print(int(ser.readline()),end="")
#     print(',',end="")
#     time.sleep(0.5)
# print(' };')


## Wait until the arduino tells us it
## is finished blinking
##if ser.read() == '1':
##    ser.read()

print('~~~~Arduino starts sending~~~~')

var=int(dataSize)
ser.write(b's')
ser.write(str(var).encode())
time.sleep(1)
dataSize = ser.readline() #reads 1 bytes(size of data)
print('on Arduino side,data Size is:', int(dataSize))

for x in range(int(dataSize)-1):
    ser.write(str(data[x]).encode())
    time.sleep(0.5)

#count = ser.readline().decode("utf-8")  #reads first line
#print ('Arduino says:', count)
#time.sleep(3)

print('on Arduino side,unsigned int raw[',end="")
print(int(dataSize),end="")
print('] = ',end="")
print('{ ',end="")
for x in range(int(dataSize)-1):
    print(ser.readline().strip(), end="")
    print(',',end="")
print(' };')



## close the port and end the program
print ('closing port')
ser.close()