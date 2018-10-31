from tkinter import *
from doctest import master
import serial
import signal
import time
import threading

exitThread = False
def handler(signum, frame):
    exitThread = True
def readThread(ser):
    global line
    global exitThread

    while not exitThread:
        rxdata = ser.readline().decode('utf-8')
        len_rxdata = len(rxdata)
        if rxdata:
            if(rxdata[0] == 't'):
                smarthome.temp_(rxdata[2:9])
                smarthome.temp_2(rxdata[11:])
            else:
                print(rxdata)
            #smarthome.temp_(rxdata)
            #print(rxdata)


class MyFrame(Frame):
    def __init__(self, master=None):
        self.master = master
        Canvas.__init__(self, width=800, height=480)

        self.init_ui()

    def init_ui(self):
        img = PhotoImage(file="home.png")
        lbl = Label(image=img)
        lbl.image = img
        lbl.place(x=0, y=0)
        #label
        self.templ = Label(win, text='temp/humi', background='#ddf1fd')
        self.templ.place(x=580, y=205)
		
		
    
        dustl = Label(win, text='fine dust', background='#ddf1fd')
        dustl.place(x=430, y=145)
    
        lightl2 = Label(win, text='light2', background='#ddf1fd')
        lightl2.place(x=265, y=145)
    
        lightl = Label(win, text='light1', background='#ddf1fd')
        lightl.place(x=105, y=205)
    
        lightl3 = Label(win, text='out light', background='#ddf1fd')
        lightl3.place(x=650, y=310)
    
        venl = Label(win, text='ventilator', background='#ddf1fd')
        venl.place(x=25, y=305)
    
        # button
        self.light_1 = PhotoImage(file="light_1.png")
        self.lightb1 = Button(win, width=73, heigh=62, image=self.light_1, command=self.click1, relief=FLAT,borderwidth=0)
        self.lightb1.place(x=80, y=140)
    
        self.light_2 = PhotoImage(file="light_2.png")
        self.lightb2 = Button(win, width=73, heigh=62, image=self.light_2, command=self.click2, relief=FLAT,borderwidth=0)
        self.lightb2.place(x=240, y=75)

    def click1(self):
        str = 'L1Z'
        ser.write(bytes(str.encode()))
        print ('click-1')

    def click2(self):
        str = 'L2Z'
        ser.write(bytes(str.encode()))
        print ('click-2')
    
    def temp_(self, a):
        self.templ2 = Label(win, text=a, background='#ddf1fd')
        self.templ2.place(x=585, y=100)
    def temp_2(self, a):
        self.templ3 = Label(win, text=a, background='#ddf1fd')
        self.templ3.place(x=585, y=115)


win = Tk()
win.title("Smart Home")
win.geometry('800x480+0+0')
win.config(cursor='none')
ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
signal.signal(signal.SIGINT, handler)
thread=threading.Thread(target=readThread, args=(ser,))      # thread 생성
thread.start()
#win.attributes('-fullscreen', True)
smarthome = MyFrame(master=win)
win.mainloop()
