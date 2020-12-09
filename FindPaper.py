import sys
import numpy as np
import cv2
import math

class VideoCapture():

    def __init__(self, *namedWindows):
        self.capture = cv2.VideoCapture(0)
        self.currentWindow = ''
        self.namedWindows = namedWindows
        while self.currentWindow in self.namedWindows:
            cv2.namedWindow(self.currentWindow)
        
    def castom(self):
        #wl = (0,50,0)
        #wh = (50,100,255)
        buff = 0
        self.wl = (15,0,165)
        self.wh = (25,255,255)
        self.ret, self.frame = self.capture.read()        
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.h,self.s,self.v = cv2.split(self.hsv)
        for i in range(len(self.s)):
            for j in range(len(self.s[0])):
                buff += self.s[i][j]
        
        count = len(self.s) * len(self.s[0])
        Smiddle = buff / count
        #print("SMIDDLE = {}".format(round(Smiddle, 1)))
        light = ((256 - (buff / count)) / 256) * 100
        print("LIGHT = {}%".format(round(light, 1)))
        #print(self.v)
        #hsv = cv2.GaussianBlur(hsv, (3, 3), 0)
        cv2.imshow('hsv', self.hsv)
        self.w = cv2.inRange(self.hsv,self.wl,self.wh) 
        #b,g,r = cv2.split(hsv)
        #ret,thresh = cv2.threshold(self.w,50,255,cv2.THRESH_BINARY_INV)
        canny = cv2.Canny(self.w, 10, 100)
        #edged = cv2.Canny(gray, 10, 250)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
        
        _, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        #for cur_contours in contours:
        #    pass
        for c in cnts:
            
            #print("c is {}".format(c))
            #print("len c is {}".format(len(c)))
            #print("rect = {}".format(rect))
            #area = int(rect[1][0]*rect[1][1])
            # аппроксимируем (сглаживаем) контур
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            #cv2.drawContours(self.frame, approx, -1, (255, 255, 0), 5)
            square = isitsquare(approx)
            if square:
                rect = cv2.minAreaRect(c)
                #print("RECT = {}".format(rect))
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                #print("BOX = {}".format(box))
                #hill = cv2.convexHull(c)
                #print("approx is {}".format(approx))
                #cv2.drawContours(self.frame, [box], -1, (0, 255, 255), 5)
                cv2.drawContours(self.frame, [approx], -1, (0, 255, 0), 2)
                #cv2.drawContours(self.frame, hill, -1, (0, 255, 255), 5)
        
        #cv2.imshow('castom', self.w)
        #cv2.imshow('something', thresh)
        cv2.imshow('closed', closed)
        cv2.imshow('release', self.frame)
    
    def __del__(self):
        self.capture.release()
        cv2.destroyAllWindows()
        #print("The program is over")
 
def isitsquare(mass):
    square = False
    count = 0
    sharp = 0
    perim = 0
    maxlenV = 0
    lenV = []
    per = 0
    area = 0
    #print("start square")
    #print("mass is {}".format(mass[0]))
    #print(len(mass))
    for cnt in range(1,len(mass) - 1):
        #if (len(mass) < 2): continue
        rect = cv2.minAreaRect(mass)
        #print("rect = {}".format(rect))
        area = int(rect[1][0]*rect[1][1])
        a = mass[cnt - 1][0]
        b = mass[cnt][0]
        if (cnt == len(mass) - 1):
            c = mass[0][0]
        else:
            c = mass[cnt + 1][0]
        #print("angle between a = {}, b = {}, c = {}".format(a,b,c))
        ab = [a[0] - b[0], (a[1] * (-1)) - (b[1] * (-1))]
        #print(ab)
        cb = [c[0] - b[0], (c[1] * (-1)) - (b[1] * (-1))]
        #print(cb)
        scalar = ab[0] * cb[0] + ab[1] * cb[1]
        #print(scalar)
        lenvectorAB = np.sqrt(ab[0] ** 2 + ab[1] ** 2) 
        lenvectorCB = np.sqrt(cb[0] ** 2 + cb[1] ** 2)
        lenvectors = lenvectorAB * lenvectorCB
        #print(lenvectors)
        angle = np.degrees(np.arccos(scalar / lenvectors))
        #print(angle)
        perim += lenvectorAB
        #print("AB = {}".format(lenvectorAB))
        #print("CB = {}".format(lenvectorCB)) 
        #print("perim = {}".format(perim))
        lenV.append(lenvectorAB)
        
        if (lenvectorAB > maxlenV): maxlenV = lenvectorAB
        #print("maxlenV = {}".format(maxlenV))
        if (angle <= 119 and angle >= 61):
            count+=1
        if (angle <= 60 or angle >= 120):
            sharp+=1
    # try:
        # per = maxlenV / perim
    # except ZeroDivisionError:
        # print("lenV = {}".format(lenV))
        # print("DBZ max = {}, perim = {}".format(maxlenV, perim))
    #print("PER = {}".format(per))
    #print("SHARP = {}".format(sharp))
    if (count >= 2 and sharp == 0 and area > 1000):# and per > 0.25):
        #print("lenV = {}".format(lenV))
        square = True
        #print("===================find square")
        return square
    #print("finish square")
 
VC = VideoCapture("release","something", "castom", "gray", "closed")
while True:
    VC.castom()
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        VC.__del__()
        break
cv2.destroyAllWindows()








