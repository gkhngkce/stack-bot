import cv2
import pyautogui
import numpy as np
import time

"""img = cv2.imread("Resources/suiwave.jpg")
print(img.shape)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, threshold1=30, threshold2=100)
cv2.imshow("edges", edges)
cv2.waitKey(0)"""

img = pyautogui.screenshot()
frame = np.array(img)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(frame, threshold1=30, threshold2=100)
with open("test.txt", "w") as file:
    for line in edges:
        for i in line:
            file.write(str(i))
edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
cv2.imwrite("test.png", edges)