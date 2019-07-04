# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:48:43 2019

@author: ROBERTO MARIO
"""

import serial
import pynmea2

serialCropCircle=serial.Serial('COM13',9600)
for i in range(10):
    message=serialCropCircle.readline().strip()
    parsedMessage=pynmea2.parse(message)
    print(parsedMessage.longitude)
    print(parsedMessage.latitude)
serialCropCircle.close()