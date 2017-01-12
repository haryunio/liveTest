#-*-coding:utf-8
import serial
import time
import json
import urllib
import urllib.request
import RPi.GPIO as GPIO

import pygame

red   = 17      #color pins
green = 18      #color pins
blue  = 27      #color pins
Freq  = 100
delaycount = 0
bookcaseNumber = 100

data       = []
url_rfid   = "https://ll.0o0.moe/API/takeMyBooks"
url_rgb    = "https://ll.0o0.moe/API/getMyLights"
Token      = "SOMBMsCSDOFKOrUxG3qjTpmpdemj9z1SWKmievcHqU7j7MYmVsTEorBZqfpWWrgD5FQpXePDW6j8LkM5f8qkNW0Rc8HgzmL59rOV575hXMULQNHVO2EljSUiM3ve14QA"



ser = serial.Serial('COM5', 9600, timeout=10)

class RGB:
    def off():
        this.on(0,0,0)

    def on(R, G, B):
        R = int((R/255)*100)
        G = int((G/255)*100)
        B = int((B/255)*100)
        RED.ChangeDutyCycle(R)
        GREEN.ChangeDutyCycle(G)
        BLUE.ChangeDutyCycle(B)
    
    def led():
        js = json.loads(server.req_rgb())
        if js["success"] == True and js["lightColor"] != None:
            RGB.on(int(js["lightColor"][1:3], 16), 
                   int(js["lightColor"][3:5], 16), 
                   int(js["lightColor"][5:7], 16))
        else:
            RGB.off()

class server:
    def __init__():
        self.sdata = {'libraryAPIToken' : Token, 
                      'bookcaseNumber'  : bookcaseNumber}
    def __init__(dat):
        self.sdata = {'libraryAPIToken' : Token, 
                      'bookcaseNumber'  : bookcaseNumber, 
                      'bookCodes'       : dat}

    def req_rgb():
        sdata = {'libraryAPIToken' : Token, 
                 'bookcaseNumber'  : bookcaseNumber}

        request = urllib.request.Request(url_rgb)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata        = json.dumps(sdata)
        jsondataasbytes = jsondata.encode('utf-8')
        request.add_header('Content-Length', len(jsondataasbytes))

        f = urllib.request.urlopen(request, jsondataasbytes)
        return f.read().decode('utf-8')
    
    def req_rfid(dat):
        sdata = {'libraryAPIToken' : Token, 
                 'bookcaseNumber'  : bookcaseNumber, 
                 'bookCodes'       : dat}

        request = urllib.request.Request(url_rfid)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata        = json.dumps(sdata)
        jsondataasbytes = jsondata.encode('utf-8')
        request.add_header('Content-Length', len(jsondataasbytes))

        f = urllib.request.urlopen(request, jsondataasbytes)
        return f.read().decode('utf-8')

try:
 while 1:
     delaycount += 1
     response = str(ser.readline())[4:12]

     if (len(response) == 11) and (data.count(response) == 0):
            data.append(response)
            print(response)
     if delaycount > 4:
         delaycount = 0
         server.req(Data)
         server.led()
     
except KeyboardInterrupt:
    print("QUITTTING")
    RUNNING = False
    ser.close()
    GPIO.cleanup()
