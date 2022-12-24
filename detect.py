import cv2
import pyautogui
import numpy as np
import time

print("waiting for 4 seconds")
time.sleep(5)
print("recording has started")

#This variable we use to store the pixel location
refPt = []
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.putText(result, strXY, (x,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("Overlapped Edges", result)

while (True):
    img = pyautogui.screenshot(region=(570, 375, 480, 360))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(frame, threshold1=30, threshold2=120)

    # find the contours in the binary image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort the contours by area in decreasing order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    overlap = np.zeros_like(frame)
    contour_image = np.zeros(frame.shape)
    colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    #here is my attempt to figure out if i can discriminate based on the contours and visualise this with colours
    for i, contour in enumerate(contours):
        cv2.drawContours(contour_image, contours, i, colours[i % len(colours)], 1)

    cv2.imshow('Contours', contour_image) #doesnt show the colours for whatever reason


    for c in contours:
        print(cv2.contourArea(c))
        if (cv2.contourArea(c)>200): #clear out the small particles
            cv2.drawContours(overlap, [c], -1, (255, 255, 255), -1)

    #perform a bitwise AND operation between the original image and the image with the drawn contours
    result = cv2.bitwise_and(frame, overlap)
    cv2.imshow('Overlapped Edges', result)
    cv2.setMouseCallback("Overlapped Edges", click_event)

    # if ESC is pressed exit, must have one of the imshow windows as the active window
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
