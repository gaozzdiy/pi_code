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

def edaged():
    left = GPIO.input(35)
    right = GPIO.input(37)
    print(left,right)
    if left == 1 or right == 1:
       GPIO.output(MOTOB, GPIO.HIGH) 
       GPIO.output(MOTOA, GPIO.HIGH) 
    else :
       GPIO.output(MOTOB, GPIO.LOW) 
       GPIO.output(MOTOA, GPIO.HIGH) 



moto(300,400)
while(1):
    edaged()
    time.sleep(0.3)
#moto(0,400)
#time.sleep(0.5)
#moto(301,400)
#time.sleep(1)
#moto(200,400)
