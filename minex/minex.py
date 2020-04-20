import getopt, sys
import time
import cv2,numpy
import RPi.GPIO as GPIO
import threading
import socket
import os

LINE_Y = 280
BR_VAL = 70
ADJ_MOTO_VAL = 20
FETCH_LINE = 2
FETCH_COL = 5

SRVPORT = 8002

MOTOA = 36
MOTOB = 38

RAILA = 35
RAILB = 37

STAT = "STOP"

#motor driver
def moto(pos,col):
    left,right = checkborder()
    print("end : left,right=",left,right)
    if pos < col/2 - ADJ_MOTO_VAL and pos > 0 and left == 0:
        moto_mv("left")
        print("moto: left~~~~ pos ,col/2 - ADJ_MOTO_VAL",pos,col/2-ADJ_MOTO_VAL)
    elif pos > col/2 + ADJ_MOTO_VAL and pos < col and right == 0:
        moto_mv("right")
        print("moto: right ~~~~ pos ,col/2 + ADJ_MOTO_VAL",pos,col/2+ADJ_MOTO_VAL)
    elif pos > col/2 - ADJ_MOTO_VAL and pos < col/2 + ADJ_MOTO_VAL:
        moto_mv("stop")
        print("moto: in the pos")
    else :
        moto_mv("stop")
        print("other unknow status:(left,right,pos)",left,right,pos)
    #time.sleep(0.2)
    return


def moto_mv(action):
    if action == "left":
        GPIO.output(MOTOA, GPIO.HIGH)
        GPIO.output(MOTOB, GPIO.LOW)
    elif action == "right":
        GPIO.output(MOTOB, GPIO.HIGH)
        GPIO.output(MOTOA, GPIO.LOW)
    else:
        GPIO.output(MOTOB, GPIO.HIGH)
        GPIO.output(MOTOA, GPIO.HIGH)

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
    return pos,col

def rundev():
    global STAT
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOA,GPIO.OUT)
    GPIO.setup(MOTOB,GPIO.OUT)
    GPIO.setup(RAILA,GPIO.IN)
    GPIO.setup(RAILB,GPIO.IN)
    while True:
        if STAT == "STOP":
            runReg()
            print("machine stoped")
            time.sleep(10)
        elif STAT == "RUN":
            try:
                cma = cv2.VideoCapture(0)
                while(cma.isOpened()):
                    cma.read()
                    ret, img = cma.read()
                    pos, col = getpos(img)
                    print("pos, col =",pos,col)
                    moto(pos,col)
                    #print(pos,col)
                    #time.sleep(0.1)
            except Exception as e:
                print("rundev except:",e)
            finally:
                moto_mv("stop")


def runReg():
    global STAT
    cpuserial = os.popen('grep Serial /proc/cpuinfo|awk -F\' \' \'{print $NF}\'').read().split('\n')[0]
    mac = os.popen('ip a|grep ether|awk -F\' \' \'{print $2}\'').read().split('\n')[0]
    conn = createSock()
    regval = "cpu," + cpuserial + ",mac," + mac + ",port," + str(SRVPORT)
    conn.send("regdev".encode('utf-8'))
    conn.send(regval.encode('utf-8'))
    ret = conn.recv(1024).decode()
    if ret == "succ":
        STAT = "REG"
    elif ret == "alre":
        STAT = "REG"
    elif ret == "fail":
        STAT = "STOP"
    conn.send("exit".encode('utf-8'))
    if conn.recv(1024).decode() == "exit":
        print("finish dialog!")
    conn.close()


def createSock():
    address = ('192.168.4.201', 8002)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    return sock


def sendpic(conn):
    capture = cv2.VideoCapture(0)
    capture.read()
    capture.read()
    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    picstrdata = numpy.array(imgencode).tostring()
    conn.send(str.encode(str(len(picstrdata)).ljust(16)))
    conn.send(picstrdata)
    capture.release()


def runCommand(conn, command):
    if command == "camera":
        sendpic(conn)
    elif command == "cfg":
        print("getcfg")


def runServ():
    global STAT
    address = ('0.0.0.0', SRVPORT)
    print("init server! SERV=", address)
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(address)
    serv.listen(5)
    while True:
        try:
            conn, addr = serv.accept()
            while True:
                print('connect from:' + str(addr))
                newbuf = conn.recv(1024)
                if newbuf.decode() == "exit":
                    conn.send(newbuf)
                    print("send finish, exit.")
                    break
                elif not newbuf:
                    break
                else:
                    runCommand(conn, newbuf.decode())
                    break
            conn.close()
        except Exception as e:
            print(e)


def create_thread():
    try:
        print("create thread for running:")
        t_main = threading.Thread(target=rundev)
        t_main.daemon = 1
        t_main.start()
        t_serv = threading.Thread(target=runServ)
        t_serv.daemon = 1
        t_serv.start()
        while True:
            time.sleep(5)
    except Exception as e:
        print(e)
    finally:
        moto_mv("stop")


if __name__ == "__main__":
    print("initing!")
    sys.exit(create_thread())
