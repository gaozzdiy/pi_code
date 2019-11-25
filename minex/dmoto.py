import time
import RPi.GPIO as GPIO


MOTOA = 36
MOTOB = 38

RAILA = 35
RAILB = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOA,GPIO.OUT)
GPIO.setup(MOTOB,GPIO.OUT)
GPIO.setup(RAILA,GPIO.IN)
GPIO.setup(RAILB,GPIO.IN)

def moto(x,col):
    if x < col/2 - 5 and x > 0 :
       GPIO.output(MOTOA, GPIO.LOW) 
       GPIO.output(MOTOB, GPIO.HIGH) 
    elif x > col/2 + 5 and x < col :
       GPIO.output(MOTOB, GPIO.LOW) 
       GPIO.output(MOTOA, GPIO.HIGH) 
    else :
       GPIO.output(MOTOB, GPIO.HIGH) 
       GPIO.output(MOTOA, GPIO.HIGH) 

moto(1,400)
time.sleep(0.5)
moto(0,400)
time.sleep(0.5)
moto(301,400)
time.sleep(1)
moto(0,400)
