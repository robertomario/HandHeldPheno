# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 14:58:05 2019

@author: ROBERTO MARIO
"""

import serial
serialUltrasonic=serial.Serial('COM7',38400)
count=-1
index=0
message=b''
charList=[b'0',b'0',b'0',b'0',b'0']
while(count<10):
    newChar=serialUltrasonic.read()
    #print(newChar)
    if(newChar==b'\r'):
        count+=1
        message=b''.join(charList)
        measurement=0.003384*25.4*int(message)
        print(measurement)
        message=b''
        index=0
    else:
        charList[index]=newChar
        index+=1
        if(index>5):
            index=0
            print("Something happened")
serialUltrasonic.close()