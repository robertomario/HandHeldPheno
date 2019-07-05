# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:48:43 2019

@author: ROBERTO MARIO
"""

import serial

try:
    numValues=10
    serialCropCircle=serial.Serial('COM7',38400)
    red=[]
    redEdge=[]
    nir=[]
    ndvi=[]
    ndre=[]
    for i in range(numValues):
        message=serialCropCircle.readline().strip().decode()
        measurements=message.split(',')
        measurements=[float(i) for i in measurements]
        red.append(measurements[0])
        redEdge.append(measurements[1])
        nir.append(measurements[2])
        ndvi.append(measurements[3])
        ndre.append(measurements[4])
    finalMeasurement=[sum(red),sum(redEdge),sum(nir),sum(ndvi),sum(ndre)]
    finalMeasurement=[i/numValues for i in finalMeasurement]            
    print(finalMeasurement)
finally:
    serialCropCircle.close()
