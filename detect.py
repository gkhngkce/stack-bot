import math
import cv2
import pyautogui
import numpy as np
import time
import random as rnd

print("waiting for 4 seconds")
time.sleep(3)
print("recording has started")

#This variable we use to store the pixel location
refPt = []
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.putText(cdstP, strXY, (x,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("Overlapped Edges", cdstP)

while (True):
    img = pyautogui.screenshot(region=(1360, 350, 480, 480))
    
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("org",frame)
    edges = cv2.Canny(frame, threshold1=30, threshold2=120)
    
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    #dilated = cv2.dilate(edges, kernel)
    

    dst = cv2.Canny(frame, 30, 120, None,3)
    cv2.imshow("edges",dst)
    #dst=cv2.dilate(edges, kernel)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)


    lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
            if(x0==36 and y0<=230):
                print("pt1: {} pt2: {}".format(pt1,pt2))
                cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
                if(i==2 and x0>=30):
                    cv2.imwrite("./captured/{}.jpg".format(rnd.randint(0,99999999999999)),dst)
                #cv2.imwrite("./captured/{}.jpg".format(rnd.randint(0,99999999999999)),dst)
    
    #print(len(lines))
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50,None, 20, 1)

    #print("//////////////////////////////////////////////////////////////")
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if(1):#(l[0]>=36 and l[0]<=37) and (l[2]>=36 and l[2]<=37) and (l[3]<=170 and l[1]<=400)
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
                #print("1: {} 2:{} 3:{} 4:{}".format(l[0], l[1],l[2], l[3]))
                #counted=(np.array(linesP).flatten()==37).sum()
                #print(counted)
                #counted+=(np.array(linesP).flatten()==37).sum()
                #if(counted>2):
                    #pyautogui.click()
                    #time.sleep(0.5)               
    #print("//////////////////////////////////////////////////////////////")
    cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    cv2.setMouseCallback("Detected Lines (in red) - Probabilistic Line Transform", click_event)

    # find the contours in the binary image
    #contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort the contours by area in decreasing order
    #contours = sorted(contours, key=cv2.contourArea, reverse=True)
    #print(len(edges))
    #overlap = np.zeros_like(frame)
    #contour_image = np.zeros(frame.shape)
    #colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    #here is my attempt to figure out if i can discriminate based on the contours and visualise this with colours
    #for i, contour in enumerate(contours):
    #    cv2.drawContours(contour_image, contours, i, colours[i % len(colours)], 1)

    #cv2.imshow('Contours', contour_image) #doesnt show the colours for whatever reason

    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    #dilated = cv2.dilate(contour_image, kernel)
    #cv2.imshow("dilated", dilated)

    #for c in contours:
        #print(cv2.contourArea(c))
    #    if (cv2.contourArea(c)>200): #clear out the small particles
    #        cv2.drawContours(overlap, [c], -1, (255, 255, 255), -1)

    #if(len(overlap)<5):
   
        #pyautogui.click()

    
    #perform a bitwise AND operation between the original image and the image with the drawn contours
    #result = cv2.bitwise_and(frame, overlap)
    #cv2.imshow('Overlapped Edges', result)

    #dilated2 = cv2.dilate(result, kernel)
    #cv2.imshow("dilated 2", dilated2)
    #cv2.setMouseCallback("Overlapped Edges", click_event)

    # if ESC is pressed exit, must have one of the imshow windows as the active window
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
