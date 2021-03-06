#!/usr/bin/env python3
import socket
import Adafruit_DHT
import time
import sys
import http.client as http
import urllib
import json
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)
GPIO_PIN = 4

deviceId = "DyKg0wqU"
deviceKey = "6mv09evG6uibcDKB" 
def post_to_mcs(payload): 
        headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
        not_connected = 1 
        while (not_connected):
                try:
                        conn = http.HTTPConnection("api.mediatek.com:80")
                        conn.connect() 
                        not_connected = 0 
                except (http.HTTPException, socket.error) as ex: 
                        print ("Error: %s" % ex)
                        time.sleep(10)
			 # sleep 10 seconds 
        conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
        response = conn.getresponse() 
        print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
        data = response.read() 
        conn.close() 

try:
    while True:
        h0, t0= Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, GPIO_PIN)
        if h0 is not None and t0 is not None:
            print('Temp={0:0.1f}*  '.format(t0))
        
            payload = {"datapoints":[{"dataChnId":"Temperature","values":{"value":t0}}]} 
            post_to_mcs(payload)
            time.sleep(1) 
        else:
            print('Failed to get reading. Try again!')
            sys.exit(1)
except KeyboardInterrupt:
    print('關閉程式')
