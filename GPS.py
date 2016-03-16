import time
import sys
import glob
from datetime import datetime
from Log import Logger



count =0

class GPSCommand():
    def __init__(self, Platform):
        """In case the GPS has different update rate or baud rate
        updaterate use ms
        """
        self.BaudRate = 9600
        self.UpdateRate = 1000
        self.Platform = Platform
        self.logger=Logger(Platform)
    
    def ValidGPSFile(self,file):
        """Get GNRMC to upload dict file
        """
        print 'ValidGPSFile ', file
        WriteFile = open(".//Upload//"+file,"w")
        #self.logger.Decrypt_file('.//Log//'+file+'.enc')
        #with open('.//Log//'+file+'.enc', 'rb') as in_file, open('.//Log//'+file, 'wb') as out_file:
        #    self.logger.Tdecrypt(in_file, out_file)
        
        with open('.//Log//'+file) as f:
            for line in f.readlines():
                #print line
                line = line.strip() 
                temp = str(line)
                data = temp.split(',')
                #print "ValidGPSFile data: ",data
                output = self.Parsecommand(data)
                if output != None:
                    #print "ValidGPSFile output: ",output
                    WriteFile.write(output+"\r\n")
        WriteFile.close()
        #self.logger.Encrypt_file(".//Upload//"+file,2)
        #with open(".//Upload//"+file, 'rb') as in_file, open(".//Upload//"+file+'.enc', 'wb') as out_file:
        #    self.logger.Tencrypt(in_file, out_file)
        
    def Parsecommand(self,data):
        """parse rmc 
        """
        #print "Parsecommand data: ",data
        time = -1
        output = None
        if data[1] == '$GNRMC' and data[3]=="A":
            time = self.ConvertUTCtolocalTime(int(float(data[2])),int(data[10]))
            #output=str(time[0])+'-'+str(time[1])+'-'+str(time[2])+' '+str(time[3])+'-'+str(time[4])+'-'str(time[5])+':'
            #output=str(data[0])+','
            output=str(int(time))+','
            lat=float(float(data[4])%100/60+int(float(data[4]))/100)
            lon=float(float(data[6])%100/60+int(float(data[6]))/100)
            speed=float(data[8])*1.852#change knots to km/h
            output+=str(lat)+','+str(data[5])+','+str(lon)+','+str(data[7])+','+str(speed)
        return output
    
    
    def GeBaudRate(self):
        """Return baud rate
        """
        return self.BaudRate
    
    def SetBaudRate(self,rate):
        """set baud rate
        """
        self.BaudRate = rate

    def GetUpdateRate(self):
        """Return update rate
        """
        return self.UpdateRate
        
    def SetUpdateRate(self,rate):
        """set update rate
        """
        self.UpdateRate = rate
       
    def ConvertUTCtolocalTime(self,utctime, utcdate):#return list year,month,date,hour,mini,second,nano
        """
        """
        offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        mylocaltime = offset / 60 / 60 * -1
        mytime=[]
        
        UTC=str(utcdate%100+2000)+'-'+str((utcdate/100)%100)+'-'+str(utcdate/10000)+' '+str(int(utctime/10000))+':'+str(int(utctime/100%100))+':'+str(int(utctime%100))
        
        mytime.append(utcdate%100+2000)
        mytime.append( (utcdate/100)%100 )
        mytime.append(utcdate/10000)
        mytime.append(int(utctime/10000))
        mytime.append(int(utctime/100%100))
        mytime.append(int(utctime%100))
        mytime.append(0)
        #print UTC
        dt = datetime.strptime(UTC, '%Y-%m-%d %H:%M:%S')
        sec_since_epoch = time.mktime(dt.timetuple()) + dt.microsecond/1000000.0
        myUTCtime = sec_since_epoch * 1000
        
        
        """
        if mytime[3] + mylocaltime >= 24:
            mytime[3] +=  mylocaltime - 24
            mytime[2] +=1 #bug not check 30 or 31 to change month
        elif mytime[3] + mylocaltime < 0:
            mytime[3] += 24  + mylocaltime
            mytime[2] -=1 #bug not check 30 or 31 to change month
        else:
            mytime[3] += mylocaltime
        """
        return myUTCtime

   
