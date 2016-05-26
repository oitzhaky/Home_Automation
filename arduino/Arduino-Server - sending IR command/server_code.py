'''
Created on 2011-12-02

@author: Bobby Wood
'''

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

print ('Arduino is hooked!')
time.sleep(2)

## Tell the arduino to send data!
print ('Server is sending data on serial...')
ser.write(b'r')

time.sleep(2)

count = ser.readline().decode("utf-8")  #reads first line
print ('Arduino says:', count)
time.sleep(3)
byteSize = ser.read() #reads 1 bytes(size of data)
size = int.from_bytes(byteSize, byteorder='big')
print('Data Size is:',size)

#printing the array of data
for num in range(0, size):
    print(int.from_bytes(ser.read(), byteorder='big'))
    time.sleep(1)
#arr = ser.read(int(size))

#print ('Data is: ', int(arr))

## Wait until the arduino tells us it
## is finished blinking
##if ser.read() == '1':
##    ser.read()

## close the port and end the program
print ('closing port')
ser.close()