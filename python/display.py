#!/usr/bin/python

import time
import smbus
from bmp180.BMP180 import BMP180

BUS = smbus.SMBus(1)
LCD_ADDR = 0x3F
LCD_BGLIGHT =0x08

bmp = BMP180()

#LCD_ADDR = 0x3F sudo i2cdetect -y -a 0

def send_command(comm):
        # Send bit7-4 firstly
        buf = comm & 0xF0
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)
        
        # Send bit3-0 secondly
        buf = (comm & 0x0F) << 4
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)

def send_data(data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)
        
        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= LCD_BGLIGHT        # set bglight
        BUS.write_byte(LCD_ADDR ,buf)


def init_lcd():
        try:
                send_command(0x38) # Must initialize to 8-line mode at first
                time.sleep(0.005)
                send_command(0x32) # Then initialize to 4-line mode
                time.sleep(0.005)
                send_command(0x28) # 2 Lines & 5*7 dots
                time.sleep(0.005)
                send_command(0x0C) # Enable display without cursor
                time.sleep(0.005)
                send_command(0x01) # Clear Screen
        except:
                return False
        else:
                return True

def clear_lcd():
        send_command(0x01) # Clear Screen
        time.sleep(1)

def print_lcd(x, y, str):
        if x < 0:
                x = 0
        if x > 15:
                x = 15
        if y <0:
                y = 0
        if y > 1:
                y = 1

        # Move cursor
        addr = 0x80 + 0x40 * y + x
        send_command(addr)
        
        for chr in str:
                send_data(ord(chr))

if __name__ == '__main__':
    init_lcd()
    while 1:
        dt=time.strftime("%Y-%m-%d %H:%M", time.localtime())
        temp = bmp.read_temperature()
        pressure = bmp.read_pressure()
        altitude = bmp.read_altitude()
        print_lcd(0, 0, dt)
        print_lcd(0, 1, str(temp)+" C")
        print_lcd(7, 1, str(pressure)+"hPa")
        time.sleep(1)
