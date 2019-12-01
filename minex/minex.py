import cv2
import time
import RPi.GPIO as GPIO

LINE_Y = 400
BR_VAL = 70
ADJ_MOTO_VAL = 3
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
def moto(x,col):
    left = GPIO.input(35)
    right = GPIO.input(37)
    if left == 1 or right == 1:
       GPIO.output(MOTOB, GPIO.HIGH)
       GPIO.output(MOTOA, GPIO.HIGH)
       return
    
    if x < col/2 - ADJ_MOTO_VAL and x > 0 :
       GPIO.output(MOTOA, GPIO.LOW)
       GPIO.output(MOTOB, GPIO.HIGH)
       print("turn left")
    elif x > col/2 + ADJ_MOTO_VAL and x < col :
       GPIO.output(MOTOB, GPIO.LOW)
       GPIO.output(MOTOA, GPIO.HIGH)
       print("turn right")
    else :
       GPIO.output(MOTOB, GPIO.HIGH)
       GPIO.output(MOTOA, GPIO.HIGH)
       print("no move")
    #time.sleep(0.2)

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
        #while ii < FETCH_LINE * 2:
        #    edagedval = edagedval + dest[ii][i]
        #    brightval = brightval + brdest[ii][i]
        #    ii = ii + 1
        #print("per pix:",dest[0][i],brdest[0][i])
        while ii <= FETCH_COL:
            befor_val = befor_val + dest[0][i-ii]
            after_val = after_val + dest[0][i+ii]
            ii = ii + 1
        if befor_val / FETCH_COL == 255 and after_val / FETCH_COL == 0:
            post = i
            print("the point: ",i)
        #if edagedval/(FETCH_LINE * 2) > 255/FETCH_LINE and brightval/(FETCH_LINE * 2) > BR_VAL:
        #    #if dest[0][i] > 200 and brdest[0][i] > BR_VAL/2:
        #    print("the point: ",i,brdest[0][i])
        #    post = i
        #    cnt = cnt + 1
        #    #circle(img,(i,LINE_Y),3,(0,255,0))
        i = i + 1
    #print("check:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    moto(post,col)
    print(post,col)
    #time.sleep(0.2)
