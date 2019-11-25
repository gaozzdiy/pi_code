import cv2

liney = 200
BRvalue = 100

cma = cv2.VideoCapture(0)
ret, img = cma.read()
cv2.imwrite('img.jpg',img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(img,(5,5),3,3)
img = cv2.GaussianBlur(img,(5,5),3,3)
img = cv2.GaussianBlur(img,(5,5),3,3)
img = cv2.GaussianBlur(img,(5,5),3,3)
img = cv2.GaussianBlur(img,(5,5),3,3)
cv2.imwrite('gaussianBlurimg.jpg',img)
edged = cv2.Canny(img,20,25)
row,col = img.shape
cv2.imwrite('Cannyimg.jpg',edged)
dest = edged[liney:liney+1,0:col]
brdest = img[liney:liney+1,0:col]
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(dest)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(brdest)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
