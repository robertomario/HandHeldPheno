# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 19:39:25 2019

@author: ROBERTO MARIO
"""

import xlsxwriter

files=range(24)[1:]
varieties={
    '101':'Calmant',
    '102':'Nautica',
    '103':'Mast',
    '104':'Argosy',
    '105':'Dresden',
    '106':'Compass',
    '107':'Apex',
    '108':'Knight Rider',
    '109':'Red Rider',
    '110':'Majesty',
    '111':'Sheek',
    '201':'Mast',
    '202':'Argosy',
    '203':'Red Rider',
    '204':'Apex',
    '205':'Nautica',
    '206':'Dresden',
    '207':'Knight Rider',
    '208':'Calmant',
    '209':'Majesty',
    '210':'Compass',
    '211':'Sheek',
    '301':'Soil'}
workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet()
headers=('Longitude','Latitude','Plot','Variety','NDRE','NDVI','RedEdge','NIR','Red','Distance')
worksheet.write_row(0, 0, headers)
filenames=['HHPLogFile2019-08-20X'+str(i)+'.txt' for i in files]
count=1
for n, name in enumerate(filenames):
    with open(name, 'r') as file:
        aux=file.readlines()
    if(len(aux)%4!=0):
        print('There was an issue with the mmg order')
    for row in aux:
        values=row.strip().split(';')[-1]
        if row[0]=='m':
            readings=values.split(',')
            numVariables=len(readings)
            if(numVariables>1):
                #correct multispectral
                for i in range(numVariables):
                    worksheet.write_number(count,i+4,float(readings[i]))        
            else:
                #failed ultrasonic
                worksheet.write_number(count,9,float(readings[0]))
        elif row[0]=='u':
            worksheet.write_number(count,9,float(values))
        elif row[0]=='g':
            readings=values.split(',')
            worksheet.write_number(count,0,float(readings[0]))
            worksheet.write_number(count,1,float(readings[1]))
            plotIndex=100*(1+((n+1)//11))+(n+1)%11
            if((n+1)%11==0):
                plotIndex=100*((n+1)//11)+11
            else:
                plotIndex=100*(1+((n+1)//11))+(n+1)%11
            worksheet.write_number(count,2,plotIndex)
            worksheet.write_string(count,3,varieties[str(plotIndex)])
            count+=1
        else:
            #worksheet.write(count,0,row.strip())
            #count+=1
            pass
workbook.close()
print("Finished with ", n+1, " plots")