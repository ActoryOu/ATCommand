
import webbrowser
from  Tkinter import *
from Function import Function
   
class GUIDemo():
    def __init__(self, master=None):
        #self.commandserial = Serialport()
        #self.GPSserial = Serialport()
        #self.modem = Command()
        self.function = Function()
        self.ModemSerialList=["Choose"]
        self.GPSSerialList=["choose"]
        self.ModemList=self.function.GetModemList()
        self.ModemCommandList=[]
        self.ModemCommandListState=[]
        self.UploadFileList=[]
        self.UploadFileListState=[]
        #master.minsize(width=666, height=666)
        
        self.myParent = master

        self.main_container = Frame(master, bg="green",width=800, height=666)
        self.main_container.grid()

        self.top_frame = Frame(self.main_container, bg="red",width=666, height=666)
        self.top_frame.grid()
        
        self.bottom_frame = Frame(self.main_container, bd=2, bg="yellow",width=666, height=666)
        self.bottom_frame.grid(row=2, column=0)

        self.top_left = Frame(self.top_frame, bd=2)
        self.top_left.grid(row=0, column=0)

        self.top_right = Frame(self.top_frame, bd=2)
        self.top_right.grid(row=0, column=2)
        
        self.popwindows=[]
        # for page in range(4):
            # self.popwindows.append(Toplevel(master))
        
        self.createTopWidgets()
        self.createButtomWidgets()
        #self.ModemSerialrefreshevent()
    
        
        
    def createTopWidgets(self):
        self.createUserInputButton()
        self.createLogButton()
        self.createAutoSendButton()
        self.createModemButton()
        self.createGPSButton()
        self.createUploadButton()
        self.createSystemLabel()    
        self.createSignInSignUpButton()
        
    
    def createUserInputButton(self):
        self.inputText = Label(self.top_frame)
        self.inputText["text"] = "Input Command:"
        self.inputText.grid(row=0, column=0)
        self.inputField = Entry(self.top_frame)
        self.inputField["width"] = 50
        self.inputField.grid(row=0, column=1, columnspan=5)
        self.inputField.bind('<Return>',  self.EntryEnterEvent )
        
        self.enter = Button(self.top_frame,command = self.Enterevent) 
        self.enter["text"] = "Enter"
        self.enter.grid(row=0,column=6,sticky=E)   
        
    def createSystemLabel(self):
        self.systiminfoText = Label(self.top_frame, text = "System Info: ")
        self.systiminfoText.grid(row=4, column=0)
        
        self.displayText = Label(self.top_frame)
        self.displayText["text"] = "something happened"
        self.displayText.grid(row=4, column=1)
    
    def createLogButton(self):
        myrow=0
        self.logstate = IntVar()
        self.logbutton = Checkbutton(self.top_frame, text="Log Data", variable=self.logstate,command = self.Logevent)
        self.logbutton.grid(row=2, column=0)
        
        self.logconfig = Button(self.top_frame, text="Log Config", command = self.Logconfigevent)
        self.logconfig.grid(row=3, column=0)
        
        #self.top.append(Toplevel())
        #self.top[0].geometry("%dx%d%+d%+d" % (300, 200, 250, 125))
        
        
        
    def createAutoSendButton(self):
        self.autosendstate = IntVar()
        self.autosend = Checkbutton(self.top_frame, text="AutoSend", variable=self.autosendstate, command = self.Autosendevent)
        self.autosend.grid(row=2, column=1)
        
        self.autosendconfig = Button(self.top_frame, text="AutoSend Config", command = self.Autosendconfigevent)
        self.autosendconfig.grid(row=3, column=1)
        
        #self.top.append(Toplevel())
        #self.top[0].geometry("%dx%d%+d%+d" % (300, 200, 250, 125))
    
    def createModemButton(self):
        self.modemconfig = Button(self.top_frame, text="Modem Config", command = self.Modemconfigevent)
        self.modemconfig.grid(row=2, column=2)
        
    def createModemSerialButton(self,frame,myrow,mycolumn):
        self.Modemserialchoosestate = StringVar(frame)
        self.Modemserialchoosestate.set(self.ModemSerialList[0]) # default value
        self.Modemserialportmenu =  OptionMenu(frame, self.Modemserialchoosestate, self.ModemSerialList, command = self.ModemSerialchooseevent )
        self.Modemserialportmenu.grid(row=myrow, column=mycolumn+1)
        
        self.Modemserialrefresh = Button(frame, text = "Serial refresh", command=self.ModemSerialrefreshevent )
        self.Modemserialrefresh.grid(row=myrow, column=mycolumn)
        
    def createModemChooseButton(self,frame,myrow,mycolumn):
        self.Modemchoosestate = StringVar(frame)
        self.Modemchoosestate.set(self.ModemList[0]) # default value
        self.Modemchoosemenu =  OptionMenu(frame, self.Modemchoosestate, *self.ModemList, command = self.Modemchooseevent )
        self.Modemchoosemenu.grid(row=myrow, column=mycolumn+1)
        
        
        
    def createGPSButton(self):
        
        self.logGPSstate = IntVar()
        logFileText = Checkbutton(self.top_frame,text="Log GPS file", variable=self.logGPSstate,command = self.GPSlogevent)
        logFileText.grid(row=2,column=3)
        
        self.gps = Button(self.top_frame, text = "GPS Config", command = self.GPSConfigevent)
        self.gps.grid(row=3, column=3)
        
        #self.top.append(Toplevel())
        #self.top[0].geometry("%dx%d%+d%+d" % (300, 200, 250, 125))
        
    def createGPSSerialButton(self,frame,myrow,mycolumn):
        self.GPSserialchoosestate = StringVar(frame)
        self.GPSserialchoosestate.set(self.GPSSerialList[0]) # default value
        self.GPSserialportmenu =  OptionMenu(frame, self.GPSserialchoosestate, self.GPSSerialList, command = self.GPSSerialchooseevent )
        self.GPSserialportmenu.grid(row=myrow, column=mycolumn+1)
        
        self.GPSserialrefresh = Button(frame, text = "Serial refresh", command=self.GPSSerialrefreshevent )
        self.GPSserialrefresh.grid(row=myrow, column=mycolumn)    
        
    def createUploadButton(self):
        myrow=0
        self.upload = Button(self.top_frame, text = "Upload", command = self.Uploadevent)
        self.upload.grid(row=2, column=4 )
        
        self.uploadconfig = Button(self.top_frame,text="Upload Config", command = self.Uploadconfigevent)
        self.uploadconfig.grid(row=3, column=4)
        
        #self.top.append(Toplevel())
        #self.top[0].geometry("%dx%d%+d%+d" % (300, 200, 250, 125))
        

    def createSignInSignUpButton(self):
        self.SignUp = Button(self.top_frame,text="Sign Up", command = self.SignUpevent)
        self.SignUp.grid(row=4, column=3)
        self.SignIn = Button(self.top_frame,text="Sign In", command = self.SignInevent)
        self.SignIn.grid(row=4, column=4)
    
    def createButtomWidgets(self):
        self.txt = Text(self.bottom_frame, height=20)
        
        self.txt.grid(row=0, column=0, columnspan=7)
        # self.txt.insert(END,"456")
        # for i in range(100):
            # self.txt.insert(END,"789\n\n")
        self.scroll = Scrollbar(self.bottom_frame,command=self.txt.yview)
        self.txt.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=7, sticky='Ens')
        self.function.SetScrollText(self.txt)
    def Logevent(self):
        """handle the modem log state. if the log state=0, then close the gps log as well
        """
        if self.logstate.get()==0:
            self.logGPSstate.set(0)
            self.GPSlogevent()
            self.autosendstate.set(0);
            self.Autosendevent()
        self.function.SetModemLog(self.logstate.get())
        
        #self.displayText["text"] = "Logevent" + str(self.logstate.get())
        pass
    
    def Logconfigevent(self):
        myrow=0
        #self.popwindows.append(Toplevel())
        self.Logpopwindows = Toplevel()
        self.Logpopwindows.title("Log Config")
        msg = Label(self.Logpopwindows, text="Log configure window")
        msg.grid(row=myrow, column=0)
        myrow+=1
        
        ModemLogText = Label(self.Logpopwindows,text="Log path:")
        ModemLogText.grid(row=myrow,column=0)
        
        self.ModemLogField = Entry(self.Logpopwindows,width=30)
        self.ModemLogField.grid(row=myrow,column=1)
        myrow+=1
        
        
        Cancel = Button(self.Logpopwindows, text="Cancel", command=self.Logpopwindows.destroy)
        Cancel.grid(row=myrow, column=1)
        
        Save = Button(self.Logpopwindows, text="Save", command=self.LogconfigSaveevent)
        Save.grid(row=myrow, column=0)

        
        #self.displayText["text"] = "Logconfigevent" + str(self.logstate.get())
        pass
    
    def Autosendevent(self):
        print "self.autosendstate:",self.autosendstate.get()
        self.function.SetAutoSendState(self.autosendstate.get())
        pass
    
    def Autosendconfigevent(self):
        """Set time interval, and command list. will del the old history command list
        """
        timeinterval, CommandList = self.function.GetAutoSendConfig()
        print timeinterval, CommandList
        #change autosend to stop
        #self.autosendstate.set(0)
        #self.function.SetAutoSendState(0)
        
        myrow=0
        self.Autosendpopwindows=Toplevel()
        self.Autosendpopwindows.title("Auto Config")
        msg = Label(self.Autosendpopwindows, text="AutoSend configure window")
        msg.grid(row=myrow, column=0)
        myrow+=1
        
        AutoTimeIntervalText = Label(self.Autosendpopwindows,text="Sending Interval (ms):")
        AutoTimeIntervalText.grid(row=myrow,column=0)
        
        self.AutoTimeIntervalField = Entry(self.Autosendpopwindows,width=10)
        self.AutoTimeIntervalField.grid(row=myrow,column=1)
        self.AutoTimeIntervalField.insert(0,timeinterval)
        myrow+=1
        
        self.AutoSendMB=Menubutton ( self.Autosendpopwindows, text="Command", relief=RAISED )
        self.AutoSendMB.grid(row=myrow, column=0)
        myrow+=1
        self.AutoSendMB.menu = Menu ( self.AutoSendMB, tearoff = 0 )
        self.AutoSendMB["menu"] = self.AutoSendMB.menu
        
        del self.ModemCommandList[:]
        
        self.ModemCommandList[:]= CommandList[:]
        del self.ModemCommandListState[:]
        for i in range(len(CommandList)):
            self.ModemCommandListState.append(IntVar())
            self.AutoSendMB.menu.add_checkbutton (label=self.ModemCommandList[i],variable=self.ModemCommandListState[i],command=lambda choice=i: self.ModemCommandListChoose(choice))
            

        button = Button(self.Autosendpopwindows, text="Cancel", command=self.Autosendpopwindows.destroy)
        button.grid(row=myrow, column=1)
        
        Save = Button(self.Autosendpopwindows, text="Save", command=self.AutosendconfigSaveevent)
        Save.grid(row=myrow, column=0)
        

        #self.displayText["text"] = "Autosendconfigevent" + str(self.autosendstate.get())
        pass
    
    def Modemconfigevent(self):
        myrow=0
        
        #self.popwindows.append(Toplevel())
        self.Modempopwindows = Toplevel()
        self.Modempopwindows.title("Modem Config")
        msg = Label(self.Modempopwindows, text="Modem configure window")
        msg.grid(row=myrow, column=0)
        myrow+=1
        
        self.createModemSerialButton(self.Modempopwindows,myrow,0)
        myrow+=1
        
        ModemText = Label(self.Modempopwindows,text="Choice Modem:")
        ModemText.grid(row=myrow,column=0)
        self.createModemChooseButton(self.Modempopwindows,myrow,0)
        myrow+=1
        
        
        self.ModemDebugButton = Button(self.Modempopwindows, text="Debug mode",state=DISABLED ,command=self.Modemdebugevent)
        self.ModemDebugButton.grid(row=myrow,column=0)
        myrow+=1
        
        
        Cancel = Button(self.Modempopwindows, text="Cancel", command=self.Modempopwindows.destroy)
        Cancel.grid(row=myrow, column=1)
        
        Save = Button(self.Modempopwindows, text="Save", command=self.ModemconfigSaveevent)
        Save.grid(row=myrow, column=0)

        
        # self.displayText["text"] = "Logconfigevent" + str(self.logstate.get())

    
    def ModemSerialevent(self):
        pass
    
    def ModemSerialrefreshevent(self):
        """Get the abailable serial list from Serial.py
        """
        self.ModemSerialList[:]=[] #refres list
        self.ModemSerialList = self.function.GetSerialPort()
        print self.ModemSerialList
        #update the optionbutton
        self.Modemserialportmenu['menu'].delete(0, 'end')
        for choice in self.ModemSerialList:
            #self.Modemserialchoosestate.set(choice)
            #self.Modemserialportmenu['menu'].add_command(label=choice, command=lambda v=choice: self.Modemserialchoosestate.set(v) )
            #self.Modemserialportmenu['menu'].add_command(label=choice, command=self.ModemSerialchooseevent )
            self.Modemserialportmenu['menu'].add_command(label=choice, command=lambda v=choice: self.ModemSerialchooseevent(v) )
        #self.Modemserialportmenu['command']=self.ModemSerialchooseevent
        
        # self.displayText["text"] = "ModemSerialrefreshevent" + str(self.ModemSerialList) + str(self.Modemserialchoosestate.get())
        
    def ModemSerialchooseevent(self,value=0):
        """User choose a serial port
        """
        print value,self.Modemserialchoosestate.get()
        self.function.SetModemSerialPort(value)
        
        # self.displayText["text"] = "ModemSerialchooseevent" + str(self.ModemSerialList) + str(value)
        pass
    
    def Modemchooseevent(self,value=0):
        """user choice a modem
        """
        self.ModemDebugButton['state']='normal'
        print value,self.Modemchoosestate.get()
        self.function.SetModem(self.Modemchoosestate.get())
       
        
        # self.displayText["text"] = "Modemchooseevent"  + str(self.Modemchoosestate.get())
    
    def GPSlogevent(self):
        """Log the GPS data only after the log data is activated
        """
        if self.logGPSstate.get()==1:
            self.logstate.set(1)
            self.Logevent()

        if self.logGPSstate.get()==0:
            self.autosendstate.set(0);
            self.Autosendevent()
        self.function.SetGPSLog(self.logGPSstate.get())
        
        # self.displayText["text"] = "Logevent" + str(self.logGPSstate.get())
    
    def GPSConfigevent(self):
        myrow=0
        self.GPSpopwindows=Toplevel()
        self.GPSpopwindows.title("Log Config")
        msg = Label(self.GPSpopwindows, text="GPS configure window")
        msg.grid(row=myrow, column=0)
        myrow+=1
        
        self.createGPSSerialButton(self.GPSpopwindows,myrow,0)
        myrow+=1
        

        button = Button(self.GPSpopwindows, text="Cancel", command=self.GPSpopwindows.destroy)
        button.grid(row=myrow, column=1)
        
        Save = Button(self.GPSpopwindows, text="Save", command=self.GPSSaveevent)
        Save.grid(row=myrow, column=0)

        # self.displayText["text"] = "GPSevent" 
        pass
        
    def GPSSerialrefreshevent(self):
        """Get the abailable serial list from Serial.py
        """
        self.GPSSerialList[:]=[] #refres list
        self.GPSSerialList = self.function.GetSerialPort()
        print self.GPSSerialList
        #update the optionbutton
        self.GPSserialportmenu['menu'].delete(0, 'end')
        for choice in self.GPSSerialList:
            #self.GPSserialchoosestate.set(choice)
            #self.GPSserialportmenu['menu'].add_command(label=choice, command=lambda v=choice: self.GPSserialchoosestate.set(v) )
            self.GPSserialportmenu['menu'].add_command(label=choice, command=lambda v=choice: self.GPSSerialchooseevent(v) )
        #self.Modemserialportmenu['command']=self.ModemSerialchooseevent
        
        # self.displayText["text"] = "ModemSerialrefreshevent" + str(self.GPSSerialList) + str(self.GPSserialchoosestate.get())
    
    def GPSSerialchooseevent(self,value=0):
        """User choose a GPS serial port
        """
        print value,self.GPSserialchoosestate.get()
        self.function.SetGPSSerialPort(value)
        
        # self.displayText["text"] = "GPSSerialchooseevent" + str(self.GPSSerialList) + str(value)
        pass
        
    def Uploadevent(self):
        self.function.GetUploadConfig()
        self.function.UploadFile()
        # self.displayText["text"] = "Uploadevent" 
        pass
       
    def Uploadconfigevent(self):
        myrow=0
        self.Uploadpopwindows=Toplevel()
        self.Uploadpopwindows.title("Upload Config")
        msg = Label(self.Uploadpopwindows, text="Upload configure window")
        msg.grid(row=myrow, column=0)
        myrow+=1
        
        self.UploadMB=Menubutton ( self.Uploadpopwindows, text="Upload File List", relief=RAISED )
        self.UploadMB.grid(row=myrow, column=0)
        myrow+=1
        self.UploadMB.menu = Menu ( self.UploadMB, tearoff = 0 )
        self.UploadMB["menu"] = self.UploadMB.menu
        
        del self.UploadFileListState[:]
        del self.UploadFileListState[:]
        self.UploadFileList= self.function.GetUploadFileList()
        
        for i in range(len(self.UploadFileList)):
            self.UploadFileListState.append(IntVar())
            self.UploadMB.menu.add_checkbutton (label=self.UploadFileList[i],variable=self.UploadFileListState[i],command=lambda choice=i: self.UploadFileListChoose(choice))
            

        
        button = Button(self.Uploadpopwindows, text="Cancel", command=self.Uploadpopwindows.destroy)
        button.grid(row=myrow, column=1)
        
        Save = Button(self.Uploadpopwindows, text="Save", command=self.UploadconfigSaveevent)
        Save.grid(row=myrow, column=0)
        

        # self.displayText["text"] = "Uploadconfigevent" 
        pass
    
    def UploadFileListChoose(self,value):
        
        self.function.SetUploadFile(self.UploadFileList[value],self.UploadFileListState[value].get())
        print self.UploadFileList[value],value,self.UploadFileListState[value].get()
        pass
    
    def Enterevent(self):
        # self.displayText["text"] = "This is Enter."
        mess = self.inputField.get() + "\r"
        output = self.function.SetUserInPut(mess)
        #self.txt.insert(END,output)
        #self.txt.yview(END)
        
    def EntryEnterEvent(self,event):
        print "click"
        # self.displayText["text"] = "entry enter"
        mess = self.inputField.get() + "\r\n"
        self.txt.insert(END,mess)
        
    def LogconfigSaveevent(self):
        self.Logpopwindows.destroy()
        # self.displayText["text"] = "LogconfigSaveevent" 
        pass
        
    def AutosendconfigSaveevent(self):
        self.Autosendpopwindows.destroy()
        # self.displayText["text"] = "AutosendconfigSaveevent" 
        pass
        
    def ModemconfigSaveevent(self):
        print "Modem",self.Modemserialchoosestate.get()
        self.function.SetModemSerialPort(self.Modemserialchoosestate.get())
        self.Modempopwindows.destroy()
        # self.displayText["text"] = "ModemconfigSaveevent" 
    
    def GPSSaveevent(self):
        self.GPSpopwindows.withdraw()
        # self.displayText["text"] = "GPSSaveevent" 
        pass
        
    def UploadconfigSaveevent(self):
        self.Uploadpopwindows.withdraw()
        # self.displayText["text"] = "UploadconfigSaveevent" 
        pass
    
    def ModemCommandListChoose(self,i):
        
        #self.ModemCommandListState[3].set(1)
        self.function.SetAutoSendCommand(self.ModemCommandList[i],self.ModemCommandListState[i].get())
        print self.ModemCommandList[i],i,self.ModemCommandListState[i].get()
    
    def Modemdebugevent(self):
        # self.displayText["text"] = "Modemdebugevent" 
        pass

    def SignUpevent(self):
        new = 2 # open in a new tab, if possible
        # open a public URL, in this case, the webbrowser docs
        url = "https://140.113.216.37/accounts/register/"
        webbrowser.open(url,new=new)

    def SignInevent(self):myrow=0
        self.SignInWindows=Toplevel()
        self.SignInWindows.title("Sign In")
        
        self.SignInMB=Menubutton ( self.SignInWindows, text="Upload File List", relief=RAISED )
        self.SignInMB.grid(row=myrow, column=0)
        myrow+=1
        self.UploadMB.menu = Menu ( self.UploadMB, tearoff = 0 )
        self.UploadMB["menu"] = self.UploadMB.menu
        
        del self.UploadFileListState[:]
        del self.UploadFileListState[:]
        self.UploadFileList= self.function.GetUploadFileList()
        
        for i in range(len(self.UploadFileList)):
            self.UploadFileListState.append(IntVar())
            self.UploadMB.menu.add_checkbutton (label=self.UploadFileList[i],variable=self.UploadFileListState[i],command=lambda choice=i: self.UploadFileListChoose(choice))
        
        button = Button(self.SignInWindows, text="Cancel", command=self.SignInWindows.destroy)
        button.grid(row=myrow, column=1)
        
        Save = Button(self.SignInWindows, text="Save", command=self.SignInWindows.destroy)
        Save.grid(row=myrow, column=0)
 
if __name__ == '__main__':
    root = Tk()
    #root.geometry("800x600")
    root.title("AT-Command")
    app = GUIDemo(master=root)
    root.mainloop()
    # root.title("Test UI")
    # myapp = MyApp(root)
    # root.mainloop()
