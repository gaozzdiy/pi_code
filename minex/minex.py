import cv2
import time

liney = 200
br = 100

cma = cv2.VideoCapture(0)

while(cma.isOpened()):
    ret, img = cma.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img,(5,5),3,3)
    edged = cv2.Canny(img,20,25)
    row,col = img.shape
    print(row,col)
    
    dest = edged[liney:liney+1,0:col]
    brdest = img[liney:liney+1,0:col]
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print(dest)
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print(brdest)
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    i = 0
    while i < col:
        if dest[0][i] > 200 and brdest[0][i] > 150:
            print("the point: ",i,brdest[0][i])
            #circle(img,(i,liney),3,(0,255,0))
        i = i + 1

    #time.sleep(1)

