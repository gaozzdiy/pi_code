#!/usr/bin/python

import os
import time
import smbus
import RPi.GPIO as GPIO

from bmp180.BMP180 import BMP180
from lcd1602_i2c.lcd1602_i2c import lcd1602_i2c

BUS = smbus.SMBus(1)
bmp = BMP180()
LCD1602 = lcd1602_i2c()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN)

cnt=0
while 1:
    dt=time.strftime("%Y-%m-%d %H:%M", time.localtime())
    tsp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    temp = bmp.read_temperature()
    pressure = bmp.read_pressure()
    altitude = bmp.read_altitude()
    BG= GPIO.input(7)
    LCD1602.light_lcd(BG)
    LCD1602.print_lcd(0, 0, dt)
    LCD1602.print_lcd(0, 1, str(temp)+" C")
    LCD1602.print_lcd(7, 1, str(pressure)+"hPa")
    #print tsp,temp,pressure,altitude
    time.sleep(1)
