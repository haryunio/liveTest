#-*-coding:utf-8
import serial
import urllib
import urllib.request
import time
import json
import RPi.GPIO as GPIO


red = 17
green = 18
blue = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100 #Hz

bookcaseNumber = '1'
data = ["BB A3 C3 17","3A AA A7 9B","AA A7 3A 9B","3A 9B AA A7"]
url = "http://henocks.dothome.co.kr/f6.php"
url2 = "https://ll.0o0.moe/API/login"
url_rfid = "https://ll.0o0.moe/API/takeMyBooks"
delaycount = 0
Token = "SOMBMsCSDOFKOrUxG3qjTpmpdemj9z1SWKmievcHqU7j7MYmVsTEorBZqfpWWrgD5FQpXePDW6j8LkM5f8qkNW0Rc8HgzmL59rOV575hXMULQNHVO2EljSUiM3ve14QA"

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)

RED = GPIO.PWM(red, Freq)
RED.start(0)
GREEN = GPIO.PWM(green, Freq)
GREEN.start(0)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(0)

class RGB:
    def on(color):
        print("RGB LED on with color : "+color)
        this.color(100,100,100)

    def off():
        print("RGB LED off")
        this.color(0,0,0)

    def color(R, G, B):
        RED.ChangeDutyCycle(R)
        GREEN.ChangeDutyCycle(G)
        BLUE.ChangeDutyCycle(B)

class server:
    def req(dat):
        sdata = urllib.parse.urlencode({'flag': dat}).encode('utf-8')
        request = urllib.request.Request(url)
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(request, sdata)
        return f.read().decode('utf-8')

    def req_rfid(dat):
        a = 0
        while(len(dat) > a):
            dat[a] = dat[a].replace(" ", "_")
            a += 1
        sdata = {'libraryAPIToken' : Token, 'bookcaseNumber' : bookcaseNumber, 'bookCodes' : dat}
        request = urllib.request.Request(url3)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(sdata)
        jsondataasbytes = jsondata.encode('utf-8')
        request.add_header('Content-Length', len(jsondataasbytes))
        f = urllib.request.urlopen(request, jsondataasbytes) 
        return f.read().decode('utf-8')

    def req_login(dat, URL):
        sdata = urllib.parse.urlencode({"ID": "abcde12345", "password" : "abcde12345"}).encode('utf-8')
        request = urllib.request.Request(URL)
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(request, sdata)
        return f.read().decode('utf-8')

    def checkRequest():
        a = server.req(1)
        print("checked server call : " + a)
        if(int(a) == 1):
            return 1
        else:
            return 0

    def receiveRequest():
        a = server.req(2)
        print("received server call : " + a)
        return a

    def sendData(RfidData):
        server.req(RfidData)
        print("RFID Data Sent")

try:
 while 1:
     delaycount += 1
     response = ser.readline()
     if response != '':
        if data.count(response[2:-3]) == 0:
            data.append(response[2:-3])
            print (response)
     if delaycount > 500:
      if server.checkRequest() == 1:
         delaycount = 0
         stat = str(server.receiveRequest())
         if stat[0:1] == "1":
             server.sendData(data)
         elif stat[0:1] == "2":
             RGB.off()
         else:
             RGB.on(stat)
     

except KeyboardInterrupt:
    print("QUITTTING")
    RUNNING = False
    ser.close()
    GPIO.cleanup()