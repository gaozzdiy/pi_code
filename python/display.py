#!/usr/bin/python

import os
import time
import smbus
from bmp180.BMP180 import BMP180
from lcd1602_i2c.lcd1602_i2c import lcd1602_i2c

BUS = smbus.SMBus(1)
bmp = BMP180()
LCD1602 = lcd1602_i2c()

cnt=0
while 1:
    dt=time.strftime("%Y-%m-%d %H:%M", time.localtime())
    tsp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    temp = bmp.read_temperature()
    pressure = bmp.read_pressure()
    altitude = bmp.read_altitude()
    LCD1602.print_lcd(0, 0, dt)
    LCD1602.print_lcd(0, 1, str(temp)+" C")
    LCD1602.print_lcd(7, 1, str(pressure)+"hPa")
    print tsp,temp,pressure,altitude
    cnt+=1
    if cnt>5:
        #datastring='\"{\\"timestamp\\":\\"'+str(tsp)+'\\",\\"T\\":'+str(temp)+'\\",\\"P\\":'+str(pressure)+'}\"'
        #os.system("echo "+datastring+" >>test.log")
        #print datastring 
        cnt=0
        LCD1602.light_lcd(0)
    time.sleep(1)
