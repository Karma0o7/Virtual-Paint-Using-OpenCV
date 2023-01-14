import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

myColor = [[23,3,255,43,209,255]]
myColorValue = [[67, 229, 254]]
myPoints = []  # [x, y, colorId]

def findColor(img, myColor, myColorValue, Display=False):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColor:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgContour, (x, y), 10, myColorValue[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        if Display:
            cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def drawOnCanvas(myPoints, myColorValue):
    for point in myPoints:
        cv2.circle(imgContour, (point[0], point[1]), 10, myColorValue[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgContour = img.copy()
    newPoints = findColor(img, myColor, myColorValue)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValue)
    cv2.imshow("Result", cv2.flip(imgContour, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
