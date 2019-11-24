#!/usr/bin/python

import os
import time
import smbus
import RPi.GPIO as GPIO
import fcntl

#import Adafruit_DHT
from bmp180.BMP180 import BMP180
from lcd1602_i2c.lcd1602_i2c import lcd1602_i2c

lockfile='/var/log/disply.py.lock'

class FLOCK(object):
    def __init__(self, name):
        self.fobj = open(name, 'w')
        self.fd = self.fobj.fileno()

    def lock(self):
        try:
            fcntl.lockf(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            #print 'try lock file!!!'
            return True

        except:
            #print 'lock file failed!!!'
            return False

    def unlock(self):
        self.fobj.close()



if __name__ == "__main__":
    locker=FLOCK(lockfile)
    ret=locker.lock()
    if ret:
        print 'start program success!!!'
    else:
        print 'program already running,please check!!!'
        exit()
    
    BUS = smbus.SMBus(1)
    bmp = BMP180()
    LCD1602 = lcd1602_i2c()
    
    #for AM2302
    #sensor = Adafruit_DHT.DHT22
    pin = 4
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.IN)
    
    LCD1602.light_lcd(1)
    LCD1602.print_lcd(0, 1, '  initing......')
    #temperature_DHT='initi'
    #humidity_DHT='ng...'
    cnt=0
    
    while 1:
        time.sleep(0.1)
        dt=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        time_now=time.strftime("%m-%d %H:%M", time.localtime())
        sec_now=time.strftime("%S", time.localtime())
        min_now=time.strftime("%M", time.localtime()) 
        #led light
        BG = GPIO.input(12)
        LCD1602.light_lcd(BG)
        LCD1602.print_lcd(0, 0, time_now)
        #print(dt,BG)
        #20sec update
        if int(sec_now)%5 == 0 :
          if cnt == 0:
            cnt=1
            #dht22(am2302) read
            #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            #if humidity is not None and temperature is not None:
            #    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            #    humidity_DHT='{:0.1f}% '.format(humidity)
            #    temperature_DHT='{:0.1f}C '.format(temperature)
            #else:
            #    print('read DHT fail!!!')
            cpu_file = open('/sys/class/thermal/thermal_zone0/temp')  
            cpu_temp = float(cpu_file.read())/1000
            cpu_temp_dis = '{:0.1f}C  '.format(cpu_temp)
            cpu_file.close()
            #bmp180 read
            temperature_BMP = '{:0.1f}C  '.format(bmp.read_temperature())
            pressure = '{}hPa '.format(bmp.read_pressure())
            altitude = '{}M'.format(bmp.read_altitude())
            #lcd display
            LCD1602.print_lcd(0, 0, time_now)
            #LCD1602.print_lcd(6, 0, temperature_DHT)
            #LCD1602.print_lcd(11, 0, humidity_DHT)
            LCD1602.print_lcd(12, 0, cpu_temp_dis)
            LCD1602.print_lcd(0, 1, temperature_BMP)
            LCD1602.print_lcd(7, 1, pressure)
            #rec_line = str(dt)+' '+str(humidity_DHT)+' '+str(temperature_DHT)+' '+str(temperature_BMP)+' '+str(pressure)+' '+str(altitude)+'\n'
            rec_line = str(dt)+' '+str(temperature_BMP)+' '+str(pressure)+' '+str(altitude)+'\n'
            #print(rec_line)
            #10min  rec to file
            if int(min_now)%10 == 0 and int(sec_now)%60 == 0:
                fileHandle = open ( '/data/record/sensor_record.txt', 'a' )
                fileHandle.write(rec_line)
                fileHandle.flush()
                fileHandle.close
        else :
            cnt=0
