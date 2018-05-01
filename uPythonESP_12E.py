#
# Micropython ESP8266 code to Publish knob-pot data to an Adafruit IO Feed using the MQTT protocol
# Also publishes statistics on the number of free bytes on the micropython Heap
#
# Hardware used:
# - NodeMCU dev board powered by the widely popular ESP-12E, running micropython version esp8266-20171101-v1.9.3.bin(as of 30th April 2018)
# - A Knob-Potentiometer
# 
# Prerequisites:
# - Adafruit account
# - registered to use Adafruit IO

#
# References and Hats-offs
#
# Big thanks to Tony DiCola from Adafruit for excellent tutorials on:
#   Ampy tutorial:  valuable tool to efficiently develop python code on ESP8266 hardware:  
#     https://learn.adafruit.com/micropython-basics-load-files-and-run-code
#   i2c on micropython hardware tutorial:  
#     https://learn.adafruit.com/micropython-hardware-i2c-devices
# 

import network
import time
import machine
from machine import Pin
import gc
from umqtt.simple import MQTTClient

#
# Converting incoming analog values into usable Voltage readings.
#
def knobToDegrees (maxVolt=3.3):
    print('Converting 10-bit digital signals to corresponding analog voltage values(max 3.3V)')
    knobVal = 0
    knobVal = ADC(0).read()
    #simple Unitary Method to map values
    knobVolt = knobVal * (3.3/1024)
    print("Voltage at Pin A0 of NodeMCU",end='')
    print(knobVolt)
    #simple Unitary Method to map values, again!
    knobRotation = knobVolt * (280/1024)
    time.sleep_ms(100);
    return knobRotation

#
# connect the ESP8266 to local wifi network
#
yourWifiSSID = "Manav Rachna"
yourWifiPassword = ""
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(yourWifiSSID, yourWifiPassword)
while not sta_if.isconnected():
  pass
print('Network Configuration:',end='')
print(sta_if.ifconfig()) if sat_if.isconnected() else print('This network sucks! My code is right 4sure.')
  
#
# connect ESP-12E to Adafruit IO using MQTT
#
myMqttClient = "anotherDayInAlife"  # can be anything unique
adafruitIoUrl = "io.adafruit.com" # broker URL
adafruitUsername = "icreate"  # can be found at "My Account" at adafruit.com
adafruitAioKey = "697847b8dfbb4b43b8f06bf7ed037887"  # can be found by clicking on "VIEW AIO KEYS" when viewing an Adafruit IO Feed
c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.connect()

#
# publish temperature and free heap to Adafruit IO using MQTT
#
# note on feed name in the MQTT Publish:  
#    format:
#      "<adafruit-username>/feeds/<adafruitIO-feedname>"
#    example:
#      "icreate/feeds/kno_pot"
#
#
while True:
  knobToDegrees()
  c.publish("icreate/feeds/kno_pot", str(knobToDegrees))  # publish temperature to adafruit IO feed
  c.publish("icreate/feeds/feed-micropythonFreeHeap", str(gc.mem_free()))  #publish num free bytes on the Heap
  c.publish("icreate/feeds/knob_pot", str(knobVolt))
  time.sleep(5)  # number of seconds between each Publish
  
c.disconnect()  

