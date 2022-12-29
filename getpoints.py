import cv2
import numpy as np
import pyautogui
import time
import random as rnd
import math

refPt = []
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.putText(img, strXY, (x,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("Overlapped Edges", img)


base_arr_hor=[[301.25, 0.0], [196.0, 2.1816616], [278.0, 0.9599311], [542.0, 0.9599311], [-68.0, 2.1816616]]
base_arr_vert=[[530.0, 0.0], [73.0, 0.0],[358.5, 0.0], [247.0, 0.9599311] , [510.0, 0.9599311], [321.0, 2.1816616], [301.0, 0.0], [541.0, 0.9599311], [513.0, 0.94247776]]
base_arr_hor2=[[196.0, 2.1816616], [278.0, 0.9599311], [542.0, 0.9599311], [-68.0, 2.1816616]]
base_arr_hor2=[[[196.0, 2.1816616],[278.0, 0.9599311]],[[196.0, 2.1816616],[542.0, 0.9599311]],[[-68.0, 2.1816616],[278.0, 0.9599311]],[[-68.0, 2.1816616],[542.0, 0.9599311]],[[196.0, 2.1816616], [278.0, 0.9599311], [542.0, 0.9599311]],[[278.0, 0.9599311], [542.0, 0.9599311],[278.0, 0.9599311]],[[196.0, 2.1816616], [278.0, 0.9599311], [542.0, 0.9599311],[278.0, 0.9599311]]]
merged_lines=[]

img=cv2.imread("./captured/0.jpg")
img = np.array(img)

for merged_line in base_arr_hor2:
    rho, theta = merged_line
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

for merged_line in merged_lines:
    rho, theta = merged_line
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)

cv2.imshow("result",img)
cv2.setMouseCallback("result", click_event)
cv2.waitKey(0)