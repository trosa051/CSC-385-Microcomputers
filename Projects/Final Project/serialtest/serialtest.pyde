add_library('serial')
from random import random
global myPort, lf , myString
lf = 10
myString = ""

def setup():
    global myPort, lf , myString
    lf = 126
    myString = ""
    try:
        #setup the serial port
        print Serial.list()
        portIndex = 0
        LF = 10
        print " Connecting to ", Serial.list()[portIndex]
        myPort = Serial(this, Serial.list()[portIndex], 9600)
        myPort.clear()
        #myString = None;
        myString = myPort.readStringUntil(lf)
    except:
        print("no serial")
        
    
def draw():
    global myPort, lf , myString
    myString = "Buns";
    myString = myPort.readStringUntil(lf)
    if myString != None:
        println(myString)
    myPort.write(str(lf)+"~");
    lf = lf -1
