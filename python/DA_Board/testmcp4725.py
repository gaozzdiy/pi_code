#/usr/bin/python

import time
import smbus

BUS = smbus.SMBus(1)

MCP4725_ADDR = 0x60

class MCP4725(object):
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

