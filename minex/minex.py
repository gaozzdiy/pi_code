import cv2
import time
import RPi.GPIO as GPIO

LINE_Y = 400
BR_VAL = 70
ADJ_MOTO_VAL = 20
FETCH_LINE = 2
FETCH_COL = 5


MOTOA = 36
MOTOB = 38

RAILA = 35
RAILB = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOA,GPIO.OUT)
GPIO.setup(MOTOB,GPIO.OUT)
GPIO.setup(RAILA,GPIO.IN)
GPIO.setup(RAILB,GPIO.IN)

#motor driver
def moto(pos,col):
    left,right = checkborder()
    if left == 1 or right == 1:
        GPIO.output(MOTOB, GPIO.HIGH)
        GPIO.output(MOTOA, GPIO.HIGH)
        return
    
    if pos < col/2 - ADJ_MOTO_VAL and pos > 0 :
        motoright()
        print("moto: go left")
    elif pos > col/2 + ADJ_MOTO_VAL and pos < col :
        motoleft()
        print("moto: go right")
    else :
        motostop()
        print("moto: no move")
    #time.sleep(0.2)

def motoleft():
    GPIO.output(MOTOB, GPIO.LOW)
    GPIO.output(MOTOA, GPIO.HIGH)
    return

def motoright():
    GPIO.output(MOTOA, GPIO.LOW)
    GPIO.output(MOTOB, GPIO.HIGH)
    return

def motostop():
    GPIO.output(MOTOB, GPIO.HIGH)
    GPIO.output(MOTOA, GPIO.HIGH)
    return

def checkborder():
    left = GPIO.input(35)
    right = GPIO.input(37)
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

cma = cv2.VideoCapture(0)
while(cma.isOpened()):
    #print("start:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    ret, img = cma.read()
    img,edged,col = imgtrans(img)

    dest = edged[LINE_Y - FETCH_LINE:LINE_Y + FETCH_LINE,0:col]
    brdest = img[LINE_Y - FETCH_LINE:LINE_Y + FETCH_LINE,0:col]
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print("dest:",brdest[0])
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print("edged",dest[0])
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    i = FETCH_COL
    cnt = 0
    post = 0
    while i < col - FETCH_COL:
        ii, befor_val, after_val = 1, 0, 0
        while ii <= FETCH_COL:
            befor_val = befor_val + dest[0][i-ii]
            after_val = after_val + dest[0][i+ii]
            ii = ii + 1
        if befor_val / FETCH_COL == 255 and after_val / FETCH_COL == 0:
            post = i
            print("the point: ",i)
        i = i + 1
    #print("check:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #cv2.imwrite('edgedimg.jpg',edged)
    moto(post,col)
    print(post,col)
    #time.sleep(1.2)
