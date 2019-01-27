#!/usr/bin/python
import os, time

while True:
    if '192' not in os.popen('sudo wpa_cli status').read():
        print '\n****** wifi is down, restart... ******\n'
        os.system('sudo ifup wlan0')
    time.sleep(60) #5 minutes
