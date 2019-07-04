# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:48:43 2019

@author: ROBERTO MARIO
"""

import serial
import pynmea2

serialGPS=serial.Serial('COM13',9600)
i=0
while(i<10):
    message=serialGPS.readline().strip().decode()
    print(message)
    if(message[0:6]=='$GPGGA' or message[0:6]=='$GPGLL'):
        i+=1
        parsedMessage=pynmea2.parse(message)
        print(parsedMessage.lon)
        print(parsedMessage.lat)
serialGPS.close()
