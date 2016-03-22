import time
import sys
import glob,json
import os
from datetime import datetime
import threading
from Serial import Serialport
from  Tkinter import *
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from hashlib import md5
from uuid import getnode as get_mac


class Logger():
    def __init__(self, Platform):
        """This is for encry the data and decry
        """
        self.Platform = Platform
        self.UploadKey = 9600
        self.TempKey="5475731930WireLA5475731930WireLA"

        #self.AutoSendState=0
        self.AutoCommandList={}
        self.ModemLogFile=None
        self.GPSLogState = False
        self.ModemLogState=False
        self.GPSLogFile=None
        self.MAC=get_mac()
        self.Version=1.0
        self.RSAPrivateKey=None
        self.username=None

        #address the LogSetup.conf here
        if os.path.exists('.//Setting//LogSetup.conf'):
            print 'LogSetup.conf exists'
            fd = open('.//Setting//LogSetup.conf', 'r')
            variables = fd.readline().strip('\n')
            for line in fd.readlines():
                variables += "&"+line.strip('\n')
            # print 'variables:'+variables
            self.SplitTokenAndSave(variables)
        else:
            self.username='this is pc'

        if os.path.exists("priv.pem"):
            print "get RSAsignature key from file"
            fd = open('priv.pem', 'r')
            self.RSAPrivateKey = fd.read()
            fd.close()
        else:
            print "get RSAsignature default key"
            self.RSAPrivateKey = "-----BEGIN RSA PRIVATE KEY-----\n\
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\n\
-----END RSA PRIVATE KEY-----\n"

        print "self.RSAPrivateKey"+self.RSAPrivateKey
        
    def derive_key_and_iv(self,password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + self.TempKey + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def Tencrypt(self,in_file, out_file, key_length=32):
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))
        key, iv = self.derive_key_and_iv(self.TempKey, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))

    def Tdecrypt(self,in_file, out_file, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = self.derive_key_and_iv(self.TempKey, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)    

    def RSAsignature(self,in_file, out_file):
        """create RSA signature 
        """
        # Load private key
        priv_key = RSA.importKey(self.RSAPrivateKey)
        
        # Create PKCS1 handler
        priv_cipher = PKCS1_v1_5.new(priv_key)
        # Read test file    
        message = in_file.read()
        # Create SHA1 hash object
        h = SHA.new(message)
        print 'hash',h
        # write signature into file
        out_file.write(priv_cipher.sign(h)) 
    
    
    
    def SetGPSLogState(self,state):
        self.GPSLogState=state
        print "Log.GPSLogState:",self.GPSLogState
    
    def SetModemLogState(self,state):
        self.ModemLogState=state
        print "Log.ModemLogState:",self.ModemLogState
    
    def SetAutoSendState(self,state):
        """function.py will set this variable
        """
        self.AutoSendState=state
    
    def SetAutoCommandList(self,list):
        self.AutoCommandList.clear()
        self.AutoCommandList=list.copy()
        
    def SetScrollText(self,frame):
        """get the GUI fram
        """
        self.txt=frame
    
    def SetModemLogFile(self,file,mode):
        """open or close the file
        mode1: open
        mode2: close

        """
        if mode==1:
            myUTCtime = datetime.strftime(datetime.utcnow(),'%Y-%m-%d %H-%M-%S')
            self.ModemLogFile = open(".//Log//"+myUTCtime+"-"+file,"w")
        else:
            if self.ModemLogFile != None :
                filename=self.ModemLogFile.name
                self.ModemLogFile.close()
                #self.Encrypt_file(filename,2)
                
                # with open(filename, 'rb') as in_file, open(filename+'.enc', 'wb') as out_file:
                #     self.Tencrypt(in_file, out_file)
                self.ModemLogFile = None
    
    def SetGPSLogFile(self,mode):
        """open or close the log
        mode1: open
        mode2: close

        """
        if mode==1:
            myUTCtime = datetime.strftime(datetime.utcnow(),'%Y-%m-%d %H-%M-%S')
            self.GPSLogFile = open(".//Log//"+myUTCtime+"-GPS","w")
        else:
            if self.GPSLogFile != None :
                filename=self.GPSLogFile.name
                self.GPSLogFile.close()
                #self.Encrypt_file(filename,2)
                
                # with open(filename, 'rb') as in_file, open(filename+'.enc', 'wb') as out_file:
                #     self.Tencrypt(in_file, out_file)
                self.GPSLogFile = None
    
    def StartAutoThread(self):
        self.AutoThread=threading.Thread(target=self.AutoSendThread)
        self.AutoThread.start()
    
    def StartGPSThread(self):
        self.GPSThread=threading.Thread(target=self.GPSLogThread)
        self.GPSThread.start()
    
    def Setcommandserial(self,serial):
        """get serial controll fomr function.py
        """
        self.commandserial=serial
    
    def SetGPSserial(self,serial):
        self.GPSserial=serial
    
    def SetAutoSendTimeInterval(self,interval):
        self.AutoSendTimeInterval=interval
    
    def ReadUserInPut(self,input):
        """get user input from function
        """
        output = self.commandserial.SendSerialCommand(mess)
        self.txt.insert(END,"UserInput:"+mess+"\nOutput:"+output+"\r\n")
        self.txt.yview(END)
        
        """if self.ModemLogFile != None:
                                    myUTCtime = datetime.strftime(datetime.utcnow(),'%Y-%m-%d %H-%M-%S')
                                    self.ModemLogFile.write(myUTCtime+":"+output+"\r\n")"""
    
    
    def AutoSendThread(self):
        while self.AutoSendState:
            for mess in self.AutoCommandList.keys():
                output = self.commandserial.SendSerialCommand(mess+"\r")
                        
                self.txt.insert(END,"UserInput:"+mess+"\nOutput:"+output+"\r\n")
                if self.Platform is "win":
                    self.txt.insert(END,"\r")
                self.txt.insert(END,"\n")
                
                self.txt.yview(END)
                if self.ModemLogFile != None:
                    dt = datetime.now()
                    sec_since_epoch = time.mktime(dt.timetuple()) + dt.microsecond/1000000.0

                    myUTCtime = sec_since_epoch * 1000
                    #myUTCtime = datetime.strftime(datetime.utcnow(),'%Y-%m-%d %H-%M-%S')
                    self.ModemLogFile.write(str(int(myUTCtime))+":"+output)
            	time.sleep(0.002)   
            time.sleep(self.AutoSendTimeInterval)   
            pass
            
    def GPSLogThread(self):
        """log the gps data from serial by threading
        TODO make sure the serial can readline
        """
        
        #print "GPSLogThread GPSLogState:",self.GPSLogState,"  ModemLogState:",self.ModemLogState
        while  self.GPSLogState and self.ModemLogState :
            #print "in thread"
            output = self.GPSserial.GetSerialReadline()
            if len(output) >10:
            #print output
                dt = datetime.now()
                sec_since_epoch = time.mktime(dt.timetuple()) + dt.microsecond/1000000.0
                myUTCtime = sec_since_epoch * 1000
                self.GPSLogFile.write(str(dt)+","+output)
                #self.GPSLogFile.write(str(int(myUTCtime))+","+output)
    

    
    def ToJson(self,signal,gps,modem):
        """parse the signal and gps into one json file
        assume the gps log and signal are both as same timestamp formate 
        """
        GPSFile=None
        GPSLines=None
        self.modem=modem
        if gps!=None:
            #self.Decrypt_file(".//Upload//"+gps+'.enc')
            #with open(".//Upload//"+gps+'.enc', 'rb') as in_file, open(".//Upload//"+gps, 'wb') as out_file:
            #    self.Tdecrypt(in_file, out_file)
            GPSFile=open(".//Upload//"+gps,"r")
            
            #GPSLines=GPSFile.readlines()
            gpsstate=1
        #SignalFile = open('.//Log//'+signal,'r')
        #SignalLines=SignalFile.readlines()
        
        WriteFile = open('.//Upload//'+signal,'w')
        
        
        
        timestamp=None
        jsonArray=[]
        jsonElement={}
        
        #self.Decrypt_file('.//Log//'+signal+'.enc')
        #with open('.//Log//'+signal+'.enc', 'rb') as in_file, open('.//Log//'+signal, 'wb') as out_file:
        #        self.Tdecrypt(in_file, out_file)
                
        with open('.//Log//'+signal) as SignalFile:
            
            CommandResultList = self.modem.GetCommandResultList()#TODO need to dynamic change the modem 
            print 'open ',signal,CommandResultList
            for SignalLine in SignalFile:
                #print "SignalLine:",SignalLine
                if len(SignalLine) >15:#remove empty line
                    SignalLine = SignalLine.strip() 
                    SignalLine=SignalLine.replace(':',',')
                    SignalLine=SignalLine.replace('"','')
                   # SignalLine=SignalLine.replace('/','')
                    line=SignalLine.split(',')#first is timestamp,second is command, other is result
                    if line[1] not in CommandResultList or len(line)<3:
                        #if is not a command result, pass to next one
                        continue
                    if timestamp == None:
                        #initial the time stamp
                        jsonElement.clear()
                        jsonElement=self.JsonReset()
                        #print jsonElement
                        timestamp= long(float(line[0])) #get minisceond
                        if GPSFile!=None:
                            #if GPS is available, check the time is correct or not
                            GPSLine=GPSFile.readline()
                            GPSLine=GPSLine.split(',')
                            GPStime = long(float(GPSLine[0]))/1000#use second to divide the data,not minisceond
                            #print 'GPS time=',GPStime
                            while timestamp/1000 > GPStime:
                                # if the GPS time is less than signal. then search the right one
                                GPSLine=GPSFile.readline()
                                if not GPSLine:#end of file, no data
                                    GPSFile.close()
                                    GPSFile=None
                                    GPSLine=None
                                    break
                                GPSLine=GPSLine.split(',')
                                GPStime = long(float(GPSLine[0]))/1000
                    
                    if long(float(line[0]))/1000 != timestamp/1000:#next timestamp
                        timestamp=long(line[0])
                        jsonArray.append(jsonElement.copy())
                        jsonElement.clear()
                        jsonElement=self.JsonReset()
                    
                    
                    command = CommandResultList[line[1]] #todo need to dynamic detect the right command list, now only get the choose one
                    
                    jsonElement['CellularInfo'][0]['Time']=timestamp
                    
                    #print timestamp,jsonElement['Time']
                    for index, response in enumerate(command):
                        #index start with 0
                        if line[index+2]=='D':
                            #don't care
                            continue
                        if response in jsonElement['CellularInfo'][0]:
                            jsonElement['CellularInfo'][0][response]=str(line[index+2])
                        else:
                            jsonElement['other'][0][response]=line[index+2]
                    
                    if GPSFile != None:
                        #if GPS is available, check the time is correct or not
                        #print timestamp/1000,GPStime
                        while timestamp/1000 > GPStime:
                            # if the GPS time is less than signal. then search the right one
                            GPSLine=GPSFile.readline()
                            if not GPSLine:#end of file, no data
                                GPSFile.close()
                                GPSFile=None
                                GPStime=None
                                break
                            GPSLine=GPSLine.split(',')
                            GPStime = long(float(GPSLine[0]))/1000
                        
                        if timestamp/1000 == GPStime:#check if is in the same sceond.  don't care minisceond
                            jsonElement['Lat']=GPSLine[1]
                            jsonElement['Lng']=GPSLine[3]
                            
                        
                    #print line
                    
        jsonArray.append(jsonElement.copy())     #last data       
        json.dump(jsonArray, WriteFile,indent=2)        
        
        #SignalFile.close()
        WriteFile.close()
        
        with open('.//Upload//'+signal, 'rb') as in_file, open('.//Upload//'+signal+'.sig', 'wb') as out_file:
            self.RSAsignature(in_file, out_file)

        if GPSFile != None:
            GPSFile.close()
        #os.rename('.//Log//'+signal,'.//Log//'+signal+'-Uploaded')
        
    def JsonReset(self):
        jsonElement={}
        jsonElement.clear()
        seq = ("AppicationType", "ApplicationVersion", "Account","IMEI","Lat", "Lng","CellularInfo","other","equipmentId")
        jsonElement=dict.fromkeys(seq)
        jsonElement["AppicationType"]=self.commandserial.GetPlatformOS()
        jsonElement["ApplicationVersion"]=self.Version
        jsonElement["Account"]=self.username
        jsonElement["equipmentId"]=self.MAC
        jsonElement["CellularInfo"]=[]
        cellseq=( "Time","CellID","CellMCC","CellMNC","CellPCI","CellTAC","RSSI","SINR","RSRQ","RSRP")
        cell=dict.fromkeys(cellseq)
        jsonElement["CellularInfo"].append(cell)
        jsonElement["other"]=[]
        jsonElement["other"].append({})
        return jsonElement

    def GetModemLogFile(self):
        return self.ModemLogFile

    def GetGPSLogFile(self):
        return self.GPSLogFile

    def SaveLogSetupConfig(self, variables):
        self.SplitTokenAndSave(variables)
        
        outfile = open('.//Setting//LogSetup.conf', 'w')
        outfile.write('username='+self.username)
        outfile.close()
        pass

    def SplitTokenAndSave(self, variables):
        token = variables.split("&")
        for t in token:
            print 't=',t
            SysToken = t.split("=")
            if( SysToken[0] == 'username' ):
                print 'SysToken[0]',SysToken[0]
                self.username = str(SysToken[1])
        pass

    def GetUserName(self):
        return self.username