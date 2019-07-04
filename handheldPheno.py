# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 18:36:56 2019

@author: ROBERTO MARIO
"""

import wx
import sys
import glob
import time
import serial
import pynmea2
import datetime

class PreferencesDialog(wx.Dialog):
    
    def __init__(self, settings, *args, **kw):
        super(PreferencesDialog, self).__init__(*args, **kw)
        self.InitUI()
        self.SetSize((650, 300))
        self.SetTitle('Preferences')
        self.settings=settings
        
    def InitUI(self):
        ports=['']+self.GetSerialPorts()
        
        pnl = wx.Panel(self)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(pnl, label='Multispectral', size=(120,30))
        hbox1.Add(st1, proportion=0, flag=wx.ALL)
        self.chb1=wx.CheckBox(pnl, label='Connected')
        hbox1.Add(self.chb1, proportion=1, flag=wx.ALL|wx.EXPAND)
        self.chb1.Bind(wx.EVT_CHECKBOX, self.OnChecked1)
        self.cb1=wx.ComboBox(pnl, choices=ports)
        hbox1.Add(self.cb1, proportion=1, flag=wx.ALL|wx.EXPAND)        
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(pnl, label='Ultrasonic', size=(120,30))
        hbox2.Add(st2, proportion=0, flag=wx.ALL)
        self.chb2=wx.CheckBox(pnl, label='Connected')
        hbox2.Add(self.chb2, proportion=1, flag=wx.ALL|wx.EXPAND)
        self.chb2.Bind(wx.EVT_CHECKBOX, self.OnChecked2)
        self.cb2=wx.ComboBox(pnl, choices=ports)
        hbox2.Add(self.cb2, proportion=1, flag=wx.ALL|wx.EXPAND)
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(pnl, label='GPS', size=(120,30))
        hbox3.Add(st3, proportion=0, flag=wx.ALL)
        self.chb3=wx.CheckBox(pnl, label='Connected')
        hbox3.Add(self.chb3, proportion=1, flag=wx.ALL|wx.EXPAND)
        self.chb3.Bind(wx.EVT_CHECKBOX, self.OnChecked3)
        self.cb3=wx.ComboBox(pnl, choices=ports)
        hbox3.Add(self.cb3, proportion=1, flag=wx.ALL|wx.EXPAND)
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='OK')
        cancelButton = wx.Button(self, label='Cancel')
        hbox4.Add(okButton)
        hbox4.Add(cancelButton, flag=wx.LEFT, border=5)
        okButton.Bind(wx.EVT_BUTTON, self.OnSave)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        vbox2.Add(hbox1, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.EXPAND, border=10)
        vbox2.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.EXPAND, border=10)
        vbox2.Add(hbox3, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.EXPAND, border=10)
        pnl.SetSizer(vbox2)
        
        vbox1.Add(pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox1.Add(hbox4, proportion=0, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        self.SetSizer(vbox1)
        
    def OnSave(self, e):
        self.settings.WriteBool('multispectralConnected', self.chb1.GetValue())
        self.settings.Write('multispectralPort', self.cb1.GetStringSelection())
        self.settings.WriteBool('ultrasonicConnected', self.chb2.GetValue())
        self.settings.Write('ultrasonicPort', self.cb2.GetStringSelection())
        self.settings.WriteBool('GPSConnected', self.chb3.GetValue())
        self.settings.Write('GPSPort', self.cb3.GetStringSelection())
        self.EndModal(wx.ID_OK)
        #self.Destroy()
    
    def OnCancel(self, e):
        self.EndModal(wx.ID_CANCEL)
        #self.Destroy()
    
    def OnChecked1(self, e):
        chb=e.GetEventObject()
        if(chb.GetValue()):
            self.cb1.Enable(True)
        else:
            self.cb1.Enable(False)
    
    def OnChecked2(self, e):
        chb=e.GetEventObject()
        if(chb.GetValue()):
            self.cb2.Enable(True)
        else:
            self.cb2.Enable(False)
            
    def OnChecked3(self, e):
        chb=e.GetEventObject()
        if(chb.GetValue()):
            self.cb3.Enable(True)
        else:
            self.cb3.Enable(False)
            
    def GetSettings(self):
        return self.settings
    
    #https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    def GetSerialPorts(self, maxNum=30):
        """ Lists serial port names
    
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(maxNum)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    
class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.cfg = wx.Config('HHPconfig')
        if not self.cfg.Exists('multispectralConnected'):
            self.cfg.WriteBool('multispectralConnected', False)
            self.cfg.Write('multispectralPort', '')
            self.cfg.WriteBool('ultrasonicConnected', False)
            self.cfg.Write('ultrasonicPort', '')
            self.cfg.WriteBool('GPSConnected', False)
            self.cfg.Write('GPSPort', '')
        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
                
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit')
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        menubar.Append(fileMenu, '&File')
        
        settingsMenu = wx.Menu()
        preferencesmi = wx.MenuItem(settingsMenu, wx.ID_PREFERENCES, '&Preferences')
        settingsMenu.AppendItem(preferencesmi)
        self.Bind(wx.EVT_MENU, self.OnPreferences, preferencesmi)
        menubar.Append(settingsMenu, '&Settings')
        
        helpMenu = wx.Menu()
        aboutmi = wx.MenuItem(helpMenu, wx.ID_ABOUT, '&About')
        helpMenu.AppendItem(aboutmi)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutmi)
        menubar.Append(helpMenu, '&Help')
        
        self.SetMenuBar(menubar)

        backgroundPanel = wx.Panel(self)
        backgroundPanel.SetBackgroundColour('#ededed')

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
                                            
        outerBox = wx.BoxSizer(wx.HORIZONTAL)
        
        leftBox = wx.BoxSizer(wx.VERTICAL)
        st1 = wx.StaticText(backgroundPanel, label='Map:')
        panel1 = wx.Panel(backgroundPanel)
        panel1.SetBackgroundColour('#4f0000')
        st2 = wx.StaticText(backgroundPanel, label='Log:')
        self.logText = wx.TextCtrl(backgroundPanel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        leftBox.Add(st1, proportion=0, flag=wx.ALL)
        leftBox.Add(panel1, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        leftBox.Add(st2, proportion=0, flag=wx.ALL)
        leftBox.Add(self.logText, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        
        middleBox = wx.BoxSizer(wx.VERTICAL)
        panel3 = wx.Panel(backgroundPanel)
        panel3.SetBackgroundColour('#005000')
        middleBox.Add(panel3, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        
        rightBox = wx.BoxSizer(wx.VERTICAL)
        panel4 = wx.Panel(backgroundPanel)
        panel4.SetBackgroundColour('#000049')
        btn1 = wx.Button(backgroundPanel, label='Start')
        btn2 = wx.Button(backgroundPanel, label='Measure')
        btn3 = wx.Button(backgroundPanel, label='Erase')
        btn4 = wx.Button(backgroundPanel, label='Stop')
        btn1.Bind(wx.EVT_BUTTON, self.OnStart)
        btn2.Bind(wx.EVT_BUTTON, self.OnMeasure)
        btn3.Bind(wx.EVT_BUTTON, self.OnErase)
        btn4.Bind(wx.EVT_BUTTON, self.OnStop)
        rightBox.Add(panel4, proportion=3, flag=wx.EXPAND | wx.ALL, border=20)
        rightBox.Add(btn1, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        rightBox.Add(btn2, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        rightBox.Add(btn3, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        rightBox.Add(btn4, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
                           
        outerBox.Add(leftBox, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        outerBox.Add(middleBox, proportion=2, flag=wx.EXPAND | wx.ALL, border=20)
        outerBox.Add(rightBox, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        backgroundPanel.SetSizer(outerBox)
        
        self.SetSize((1000, 850))
        self.SetTitle('HandHeld Plant Phenotyping')
        self.Centre()

    def OnQuit(self, e):
        self.Close()
        
    def OnAbout(self, e):
        dial = wx.MessageBox(("HandHeld Plant Phenotyping \n"
                             "Made by Roberto Buelvas\n"
                             "McGill University, 2019\n"
                             "Version 0.01\n"),
                             'About', wx.OK | wx.ICON_INFORMATION)
        dial.Show()
    
    def OnPreferences(self, e):
        pDialog = PreferencesDialog(self.cfg, self)
        dialogFlag=pDialog.ShowModal()
        if(dialogFlag==wx.ID_OK):
            results=pDialog.GetSettings()
            self.cfg.WriteBool('multispectralConnected', results.ReadBool('multispectralConnected'))
            self.cfg.Write('multispectralPort', results.Read('multispectralPort'))
            self.cfg.WriteBool('ultrasonicConnected', results.ReadBool('ultrasonicConnected'))
            self.cfg.Write('ultrasonicPort', results.Read('ultrasonicPort'))
            self.cfg.WriteBool('GPSConnected', results.ReadBool('GPSConnected'))
            self.cfg.Write('GPSPort', results.Read('GPSPort'))
        pDialog.Destroy()
        
    def OnStart(self, e):
        #createThread(freq, OnMeasure)
        pass
    
    def OnMeasure(self, e):
        if(self.cfg.ReadBool('multispectralConnected')):
            mr=self.getMultispectralReading()
            self.updateUI(mr)
        if(self.cfg.ReadBool('ultrasonicConnected')):        
            ur=self.getUltrasonicReading()
            self.updateUI(ur)
        if(self.cfg.ReadBool('GPSConnected')):        
            gr=self.getGPSReading()
            self.updateUI(gr)
            #updateMap(gr)
            
    def OnErase(self, e):
        if(self.logText.GetValue()!=''):
            latestLineLength=self.logText.GetLineLength(self.logText.GetNumberOfLines()-1)
            lastPosition=self.logText.GetLastPosition()
            self.logText.Remove(lastPosition-latestLineLength, lastPosition)
        
    def OnStop(self, e):
        #killThread(all)
        pass
    
    def getMultispectralReading(self, numValues=10):
        try:
            serialCropCircle=serial.Serial(self.cfg.Read('multispectralPort'),38400)
            red=[]
            redEdge=[]
            nir=[]
            ndvi=[]
            ndre=[]
            for i in range(numValues):
                message=serialCropCircle.readline().strip()
                measurements=message.split(',')
                measurements=[float(i) for i in measurements]
                red+=measurements[0]
                redEdge+=measurements[1]
                nir+=measurements[2]
                ndvi+=measurements[3]
                ndre+=measurements[4]
                #print(message)
            finalMeasurement=[sum(red),sum(redEdge),sum(nir),sum(ndvi),sum(ndre)]
            finalMeasurement=[i/numValues for i in finalMeasurement]
            serialCropCircle.close()
            return finalMeasurement
        except Exception as e:
            pass
        
    def getUltrasonicReading(self, numValues=10):
        try:
            serialUltrasonic=serial.Serial(self.cfg.Read('ultrasonicPort'),38400)
            count=-1
            finalMeasurement=0
            index=0
            message=b''
            charList=[b'0',b'0',b'0',b'0',b'0']
            while(count<numValues):
                newChar=serialUltrasonic.read()
                #print(newChar)
                if(newChar==b'\r'):
                    count+=1
                    message=b''.join(charList)
                    measurement=0.003384*25.4*int(message)
                    finalMeasurement+=measurement
                    message=b''
                    index=0
                else:
                    charList[index]=newChar
                    index+=1
                    if(index>5):
                        index=0
                        print("Something happened")
            return finalMeasurement/numValues
            serialUltrasonic.close()
        except Exception as e:
            pass
        
    def getGPSReading(self, numValues=15):
        try:
            serialGPS=serial.Serial(self.cfg.Read('GPSPort'),9600)
            for i in range(numValues):
                message=serialGPS.readline().strip()
                parsedMessage=pynmea2.parse(message)
            finalMeasurement = [parsedMessage.longitude,parsedMessage.latitude]
            return finalMeasurement
            serialGPS.close()
        except Exception as e:
            pass
        
    def updateUI(self, someValue):
        if(someValue!=None):
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            if(isinstance(someValue, list)):
                if(len(someValue)>=5):
                    #cropCircle
                    self.logText.AppendText("m;"+ts+";"+str(someValue)[1,-1])
                else:
                    #gps
                    self.logText.AppendText("g;"+ts+";"+str(someValue)[1,-1])
            else:
                #ultrasonic
                self.logText.AppendText("m;"+ts+";"+str(someValue))
        else:
            #None
            pass
    
def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()