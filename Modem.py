import time
import sys,os,re
import glob
from datetime import datetime




count =0

class ModemCommand():
    def __init__(self):
        """ModemVailList is support model list
        ModemConfList is the conf file for support command list
        ChooseModem is choosen modem to use
        """
        #self.ModemVailList = []
        self.ModemConfList = {}
        self.ChooseModem = None
        
        #self.GetModemList()
        self.TAGList=[]
        self.CommandList={}
        self.CommandResultList={}
    
    def GetModemList(self):
        """Return support modem
        """
        for company in os.listdir('.//Modem'):
            print company
            for modem in os.listdir('.//Modem//'+company):
                print modem
                modemName = modem.split('.')
                #self.ModemVailList.append(company+" "+modemName[0])
                self.ModemConfList[company+" "+modemName[0]] = ".//Modem//"+company+"//"+modem
                print self.ModemConfList.keys()
        
        
        return self.ModemConfList.keys()
    def GetModemName(self):
        """return choosen modem name
        """
        return self.ChooseModem
    
    def SetChooseModem(self,modem):
        """set  modem to use
        """
        self.ChooseModem = modem
        self.TAGList[:]=[]
        self.CommandList.clear()
        self.GetModemCommandList(self.ModemConfList[self.ChooseModem])
        return self.CommandList

    # def GetModemCommandList(self):
        # """Return available modem command
        # """
        # with open(self.ModemConfList[self.ChooseModem]) as f:
            # CommandList = f.read().splitlines()
        # return CommandList
          
    
    def GetCommandResultList(self):
        """Get the choose modem's command result list
        """
        return self.CommandResultList
    
    def GetModemCommandList(self,FilePath):
        """Get the modem command list from the conf
        """
        with open(FilePath) as file:
            for line in file.readlines():
                line = line.strip() 
                line = line.split(' ') 
                print line
                if len(line) == 1 or line[0].startswith("#"):
                    #is comment
                    continue
                command = line[0]
                response = line[1]#.split(",")
                response = re.split(r'[,\n]',response)
                response = filter(None, response)#remove empty string
                if command == "TAG":
                    #list = response.split(',')
                    for value in response:
                        self.TAGList.append(value)
                else:
                    self.CommandList[command]=response
                    self.CommandResultList[response[0]]=response[1:]
            print self.CommandList, self.CommandResultList