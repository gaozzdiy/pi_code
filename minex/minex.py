import cv2
import time
import RPi.GPIO as GPIO

liney = 200
BRvalue = 100

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


cma = cv2.VideoCapture(0)
print(cma.isOpened())
while(cma.isOpened()):
    #print("start:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    ret, img = cma.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    edged = cv2.Canny(img,20,25)
    row,col = img.shape
    #print(row,col)
    #print("translate:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
    dest = edged[liney:liney+1,0:col]
    brdest = img[liney:liney+1,0:col]
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print(dest)
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print(brdest)
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    i = 0
    cnt = 0
    post = 0
    while i < col:
        if dest[0][i] > 200 and brdest[0][i] > BRvalue:
            #print("the point: ",i,brdest[0][i])
            post = i
            cnt = cnt + 1
            #circle(img,(i,liney),3,(0,255,0))
        i = i + 1
    #print("check:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    moto(post,col)
    print(post,col)
    time.sleep(0.2)
