#/usr/bin/python

import time
import smbus

BUS = smbus.SMBus(1)

LCD_ADDR = 0x3F

class lcd1602_i2c(object):
  LCD_BGLIGHT =0x08
  def send_command(self, comm):
        # Send bit7-4 firstly
        buf = comm & 0xF0
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)
        
        # Send bit3-0 secondly
        buf = (comm & 0x0F) << 4
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)

  def send_data(self, data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)
        
        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        buf |= self.LCD_BGLIGHT        # Set light
        BUS.write_byte(LCD_ADDR ,buf)


  def __init__(self):
                self.send_command(0x38) # Must initialize to 8-line mode at first
                time.sleep(0.005)
                self.send_command(0x32) # Then initialize to 4-line mode
                time.sleep(0.005)
                self.send_command(0x28) # 2 Lines & 5*7 dots
                time.sleep(0.005)
                self.send_command(0x0C) # Enable display without cursor
                time.sleep(0.005)
                self.send_command(0x01) # Clear Screen
                self.light_lcd(1) # open bglight for Screen

  def clear_lcd(self):
        self.send_command(0x01) # Clear Screen
        time.sleep(1)

  def print_lcd(self, x, y, str):
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
        self.send_command(addr)
        
        for chr in str:
                self.send_data(ord(chr))

  def light_lcd(self,stat):
       if stat :
           self.LCD_BGLIGHT=0x08
       else : 
           self.LCD_BGLIGHT=0x00
