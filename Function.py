
import time
import sys
import glob
import threading,json
import ftplib
import os
from datetime import datetime
from Serial import Serialport
from Modem import ModemCommand 
from Serial import Serialport
from GPS import GPSCommand
from datetime import datetime
from Log import Logger
from  Tkinter import *

count =0

class Function():
    def __init__(self):
        """
        """
        self.OPENFILE = 1;
        self.CLOSEFILE = 2;

        self.commandserial = Serialport()
        self.GPSserial = Serialport()
        
        self.GPSLogState = False
        self.GPSThread=None
        
        self.ModemLogState=False
        self.ModemLogFile=None
        self.ModemThread=None
        
        self.AutoSendState=None
        self.AutoCommandList={}

        self.AutoSendTimeInterval=1 #second
        self.ModemCommandList={}
        
        self.UploadConfigList={}
        self.UploadFileList={}

        self.Platform = self.commandserial.GetPlatform()
        self.modem = ModemCommand()
        self.GPSControll = GPSCommand(self.Platform)
        self.logger=Logger(self.Platform)

    def GetPlatform(self):
        return self.Platform

    def SetModemLog(self,state):
        """log the modem and the gps same time
        """
        if state ==1 :
            self.ModemLogState = True
            self.logger.SetModemLogState(True)
        else:
            self.ModemLogState = False
            self.logger.SetModemLogState(False)
        print "Function.ModemLogState:",self.ModemLogState

    def SetScrollText(self,frame):
        self.logger.SetScrollText(frame)
        self.txt=frame

    def ParseFileToJson(self, file):
        """cahnge the upload file into json format(both of the signal and gps)
        determine gps need to add in json or not
        """
        # SignalFileList = self.UploadFileList.keys()
        
        # for file in SignalFileList:
        print 'ParseFileToJson with file:',file
        GPSFile = self.CheckGPS(file)
        self.logger.ToJson(file,GPSFile,self.modem)
        # self.ToJson(file,GPSFile)

    def SetAutoSendState(self, state):
        """Set AutoSendState
        """
        if state == 1:
            self.AutoSendState =True
            self.logger.SetAutoSendState(True)
            if len(self.AutoCommandList.keys() )==0:
                raise EnvironmentError('No command choosen')
            print self.AutoCommandList.keys()

            if self.ModemLogState :
                modem = self.modem.GetModemName()
                self.logger.SetModemLogFile(modem,self.OPENFILE)
            if self.GPSLogState:
                self.logger.SetGPSLogFile(self.OPENFILE)
                self.logger.StartGPSThread()
                print "start gps thread"

            self.logger.SetAutoCommandList(self.AutoCommandList)
            self.logger.SetAutoSendTimeInterval(self.AutoSendTimeInterval)
            self.logger.StartAutoThread()
            print "start autosend thread"
            
        else:
            ModemLogFile = self.logger.GetModemLogFile()
            GPSLogFile = self.logger.GetGPSLogFile()

            self.logger.SetModemLogFile(None,self.CLOSEFILE)
            self.logger.SetGPSLogFile(self.CLOSEFILE)

            if ModemLogFile != None:
                fileindex = ModemLogFile.name.rfind('/')
                filename = ModemLogFile.name[fileindex+1:] #remove the directory's name
                print "filename:"+filename
                self.ParseFileToJson(filename)

            self.AutoSendState =False
            self.logger.SetAutoSendState(False)
            self.logger.SetGPSLogState(False)
            print "Set AutoSendState and GPSLogState to False"
            print "Close Log file"
            #self.AutoCommandList.clear()
        
    def SetGPSLog(self,state):
        """only set the GPS state and close the file
        """
        if state ==1 :
            self.logger.SetGPSLogState(True)
            self.GPSLogState = True
        else:
            self.GPSLogState = False
            self.logger.SetGPSLogState(False)
        print "Function.GPSLogState:",self.GPSLogState
        
    def GetAutoSendConfig(self):
        """Read info from AutoSendConfig
        """
        #self.modem.GetModemCommandList
        CommandList=[1,2,3,4,5,6,7]
        print "function ",self.ModemCommandList
        return self.AutoSendTimeInterval*1000, self.ModemCommandList.keys()
        pass
        
    def SetModemSerialPort(self,port):
        """Set ModemSerial
        """
        self.commandserial.SetSerialPort(port)
        self.logger.Setcommandserial(self.commandserial)
        pass
    
    def SetGPSSerialPort(self,port):
        """Set the GPS serial port
        """
        self.GPSserial.SetSerialPort(port)
        self.logger.SetGPSserial(self.GPSserial)

    def GetModemList(self):
        """return the supporeted modem list
        """
        return self.modem.GetModemList()
        
    def SetModem(self,modem):
        """Set which modem will be use
        """
        print "SetModem"
        self.ModemCommandList.clear()
        self.ModemCommandList=self.modem.SetChooseModem(modem)
        
    def GetModemSerialPort(self):
        """Get Modem serial list
        """
        return self.commandserial.GetSerialPortList()
        pass
    
    def GetSerialPort(self):
        """Get  serial list
        """
        return self.commandserial.GetSerialPortList()
        pass
    
        
    def GetUploadConfig(self):
        """Read info from UploadConfig
        """
        self.UploadConfigList.clear()
        file = open('.//Setting//Upload.conf','r')
        
        for line in file.read().splitlines():
            content = line.split(':')
            self.UploadConfigList[content[0]] = content[1]
            #print line
        return self.UploadConfigList
        
        pass
    def GetUploadFileList(self):
        """Get the available upload file list
        """
        filelist = []
        for file in os.listdir('.//Upload'):
            #if not ( file.endswith('GPS') or file.endswith('-Uploaded') or file.endswitch):
            if not file.endswith('GPS') and not file.endswith('.sig'):
                filelist.append(file)
                print file
        return filelist
        pass
    
    def CheckGPS(self,file):
        """check the upload file need gps or not
        """
        
        lasttag=file.rfind('-')
        GPSfile=file[:lasttag]+'-GPS'
        print 'CheckGPS with ',GPSfile
        for gpslist in os.listdir('.//Log'):
            if gpslist==GPSfile:
                self.GPSControll.ValidGPSFile(gpslist)
                return GPSfile
        return None
        
    def UploadFile(self):
        """upload the file to the server
        """
  
        UploadConfig = self.GetUploadConfig()
        # self.ParseFileToJson()
        #session = ftplib.FTP(UploadConfig['Server IP'],UploadConfig['Server ID'],UploadConfig['Server PW'])
        ftp = ftplib.FTP()
        ftp.connect(UploadConfig['Server IP'], 21)
        ftp.login(UploadConfig['Server ID'],UploadConfig['Server PW'])
        print "Logging in"
        

        for filename in self.UploadFileList.keys():
            print 'upload file:',filename
            try:
                #ploadfile=open('.//Upload//'+filename,'rb')
                with open('.//Upload//'+filename,'rb') as uploadfile, open('.//Upload//'+filename+'.sig','rb') as uploadfileSIG:
                    ftp.cwd('/file/data/')
                    ftp.storbinary("STOR " + filename, uploadfile)     # send the file
                    ftp.cwd('/file/sig/')
                    ftp.storbinary("STOR " + filename+'.sig', uploadfileSIG)
            
            
                print 'uploaded ',filename
            except IOError:
                print "failed to upload"
        print 'close ftp'
        ftp.close()
        self.UploadFileList.clear()
        
    def SetUploadFile(self,command,state):
        """set which file will be uploaded
        """
        if command in self.UploadFileList:
            if state == 0:
                del self.UploadFileList[command]
        else:
            if state ==1:
                self.UploadFileList[command]=state
        print "self.UploadFileList:",self.UploadFileList
    
    def SetAutoSendCommand(self,command,state):
        """Set which command will be auto 
        """
        if command in self.AutoCommandList:
            if state == 0:
                del self.AutoCommandList[command]
        else:
            if state ==1:
                self.AutoCommandList[command]=state
        print self.AutoCommandList
        
   
    def SetUserInPut(self,mess):
        """Send the input to the serial port
        """
        self.logger.Setcommandserial(self.commandserial)
        self.logger.ReadUserInPut(mess)
        
        # output = self.commandserial.SendSerialCommand(mess)
        
        # self.txt.insert(END,"UserInput:"+mess+"\nOutput:"+output+"\r\n")
        # self.txt.yview(END)
        
        # if self.ModemLogFile != None:
            # myUTCtime = datetime.strftime(datetime.utcnow(),'%Y-%m-%d %H-%M-%S')
            # self.ModemLogFile.write(myUTCtime+":"+output+"\r\n")

    def LoginSuccess(self, username):
        variables = 'username='+username
        self.logger.SaveLogSetupConfig(variables)
        pass
