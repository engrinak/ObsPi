import time
import spidev
import math
import datetime
import RPi.GPIO as GPIO


max_speed_hz=5000
dt = datetime.datetime

port = 0
device = 0

SPD = spidev.SpiDev()


GPIO.setmode(GPIO.BCM)  #use GPIO numbers, not pin numbers.

GPIO.setup(22, GPIO.IN) #set GPIO 22 to input

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

def leadingzero(binstring):
    if len(binstring) < 8:
        n = 8 - len(binstring)
        binstring = '0' * n + binstring
    return binstring

def to_binary(myval):
    binstring = bin(myval).split('b')[1]
    binstring = leadingzero(binstring)
    return binstring

while True:
    SPD.open(port, device)
    SPD.max_speed_hz=max_speed_hz

    # Default to mode 0.
    SPD.mode = 0
    #Initiate a single measurement
    SPD.xfer2([0x00, 0x70])

    time.sleep(0.02)
    print('sleep 20ms')

    state = GPIO.input(22)
    print('state is ... ' + str(state))
    if (state == 1):
        print('DRDY True')

    time.sleep(0.008)
    print('sleep 8ms')

    regAddr = 0xA4 
    address = 0x80 | regAddr
    mybytes = SPD.xfer2([address, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    print(mybytes)    
    mybins = []

    for b in mybytes[1:]:
        binstring = to_binary(b)
        mybins.append(binstring)

    X2 = mybins[0] + mybins[1] + mybins[2]
    Y2 = mybins[3] + mybins[4] + mybins[5]
    Z2 = mybins[6] + mybins[7] + mybins[8]

    binary_string = X2
    print('X2 Binary = ', X2)
    X2 = twos_comp(int(binary_string,2), len(binary_string))
    print('X2 = ', X2)
    binary_string = Y2
    print('Y2 Binary = ', Y2)
    Y2 = twos_comp(int(binary_string,2), len(binary_string))
    print('Y2 = ', Y2)
    binary_string = Z2
    print('Z2 Binary = ', Z2)
    Z2 = twos_comp(int(binary_string,2), len(binary_string))
    print('Z2 = ', Z2)

    F2 = (X2**2 + Y2**2 + Z2**2)**0.5

    print("Total Field = sqrt(x^2 + y^2 + z^2)")
    print("Total Field = ", str(F2))


    with open('magtest.txt', 'a') as myfile:
        myfile.write(dt.strftime(dt.now(), "%Y-%m-%d %H:%M:%S") + ',' + str(F2) + ',' + str(X2) + ',' + str(Y2) + ',' + str(Z2) + '\n')
        myfile.close()

    SPD.close()
    time.sleep(60)