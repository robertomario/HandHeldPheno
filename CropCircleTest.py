# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:48:43 2019

@author: ROBERTO MARIO
"""

import serial
serialCropCircle=serial.Serial('COM7',38400)
for i in range(10):
    message=serialCropCircle.readline().strip()
    print(message)
serialCropCircle.close()