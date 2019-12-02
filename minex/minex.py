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
    if pos < col/2 - ADJ_MOTO_VAL and pos > 0 and left == 0:
        motoleft()
        #print("moto: right~~~~ pos ,col,ADJ_MOTO_VAL",pos,col,ADJ_MOTO_VAL)
        print("moto: left~~~~ pos ,col/2 - ADJ_MOTO_VAL",pos,col/2-ADJ_MOTO_VAL)
    elif pos > col/2 + ADJ_MOTO_VAL and pos < col and right == 0:
        motoright()
        #print("moto: left ~~~~ pos ,col,ADJ_MOTO_VAL",pos,col,ADJ_MOTO_VAL)
        print("moto: right ~~~~ pos ,col/2 + ADJ_MOTO_VAL",pos,col/2+ADJ_MOTO_VAL)
    elif pos > col/2 - ADJ_MOTO_VAL and pos < col/2 + ADJ_MOTO_VAL:
        motostop()
        print("moto: in the pos")
    else :
        motostop()
        print("other unknow status:(left,right,pos)",left,right,pos)
    #time.sleep(0.2)
    return

def motoright():
    GPIO.output(MOTOB, GPIO.HIGH)
    GPIO.output(MOTOA, GPIO.LOW)
    return

def motoleft():
    GPIO.output(MOTOA, GPIO.HIGH)
    GPIO.output(MOTOB, GPIO.LOW)
    return

def motostop():
    GPIO.output(MOTOB, GPIO.HIGH)
    GPIO.output(MOTOA, GPIO.HIGH)
    return

def checkborder():
    left = GPIO.input(RAILB)
    right = GPIO.input(RAILA)
    return left,right
    

#graph trans
def imgtrans(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    #edged = cv2.Canny(img,10,3)
    ret,thresh = cv2.threshold(img,BR_VAL,255,0)
    row,col = img.shape
    #print(row,col)
    return img,thresh,col

def getpos(img):
    img,edged,col = imgtrans(img)
    dest = edged[LINE_Y - FETCH_LINE:LINE_Y + FETCH_LINE,0:col]
    brdest = img[LINE_Y - FETCH_LINE:LINE_Y + FETCH_LINE,0:col]
    
    i = FETCH_COL
    cnt = 0
    pos = 0
    while i < col - FETCH_COL:
        ii, befor_val, after_val = 1, 0, 0
        while ii <= FETCH_COL:
            befor_val = befor_val + dest[0][i-ii]
            after_val = after_val + dest[0][i+ii]
            ii = ii + 1
        if befor_val / FETCH_COL == 255 and after_val / FETCH_COL == 0:
            pos = i
            #print("the point: ",i)
        i = i + 1
        #print("check:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #cv2.imwrite('edgedimg.jpg',edged)
    return pos,col

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOA,GPIO.OUT)
    GPIO.setup(MOTOB,GPIO.OUT)
    GPIO.setup(RAILA,GPIO.IN)
    GPIO.setup(RAILB,GPIO.IN)
    try:
        cma = cv2.VideoCapture(0)
        while(cma.isOpened()):
            ret, img = cma.read()
            ret, img = cma.read()
            ret, img = cma.read()
            ret, img = cma.read()
            ret, img = cma.read()
            pos, col = getpos(img)
            print("pos, col =",pos,col)
            moto(pos,col)
            #print(pos,col)
            #time.sleep(0.1)
    finally:
        motostop()

if __name__ == "__main__":
    sys.exit(main())
