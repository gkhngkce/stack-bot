import cv2
import pyautogui
import numpy as np
import time

print("waiting for 4 seconds")
time.sleep(5)
print("recording has started")
screen_size = tuple(pyautogui.size())

fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 20

out = cv2.VideoWriter("output.avi", fourcc, fps, screen_size)


while(True):
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(frame, threshold1=30, threshold2=100)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    out.write(edges)
    if cv2.waitKey(1) == ord("q"):
        break
out.release()