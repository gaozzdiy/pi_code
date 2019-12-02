import getopt, sys
import time
import cv2
import RPi.GPIO as GPIO

LINE_Y = 280
BR_VAL = 70
ADJ_MOTO_VAL = 20
FETCH_LINE = 2
FETCH_COL = 5


MOTOA = 36
MOTOB = 38

RAILA = 35
RAILB = 37


#motor driver
def moto(pos,col):
    left,right = checkborder()
    print("end : left,right=",left,right)
    if pos < col/2 - ADJ_MOTO_VAL and pos > 0 :
        motoleft()
        #print("moto: right~~~~ pos ,col,ADJ_MOTO_VAL",pos,col,ADJ_MOTO_VAL)
        print("moto: right~~~~ pos ,col/2 - ADJ_MOTO_VAL",pos,col/2-ADJ_MOTO_VAL)
    elif pos > col/2 + ADJ_MOTO_VAL and pos < col :
        motoright()
        #print("moto: left ~~~~ pos ,col,ADJ_MOTO_VAL",pos,col,ADJ_MOTO_VAL)
        print("moto: left ~~~~ pos ,col/2 + ADJ_MOTO_VAL",pos,col/2+ADJ_MOTO_VAL)
    elif pos > col/2 - ADJ_MOTO_VAL and pos < col/2 + ADJ_MOTO_VAL:
        motostop()
        print("moto: in the pos")
    else :
        motostop()
        print("other unknow status:(left,right,pos)",left,right,pos)
    #time.sleep(0.2)
    return

def motoright():
    GPIO.output(MOTOA, GPIO.HIGH)
    GPIO.output(MOTOB, GPIO.LOW)
    return

def motoleft():
    GPIO.output(MOTOB, GPIO.HIGH)
    GPIO.output(MOTOA, GPIO.LOW)
    return

def motostop():
    GPIO.output(MOTOB, GPIO.HIGH)
    GPIO.output(MOTOA, GPIO.HIGH)
    return

def checkborder():
    left = GPIO.input(RAILB)
    right = GPIO.input(RAILA)
    return left,right

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOA,GPIO.OUT)
    GPIO.setup(MOTOB,GPIO.OUT)
    GPIO.setup(RAILA,GPIO.IN)
    GPIO.setup(RAILB,GPIO.IN)
    try:
        while True:
            col = 640
            pos = input("input pos:")
            print("pos, col =",pos,col)
            moto(pos,col)
            #print(pos,col)
            time.sleep(0.2)
            motostop()
    finally:
        motostop()

if __name__ == "__main__":
    sys.exit(main())
