import math
import cv2
import pyautogui
import numpy as np
import time

time.sleep(1)
# Load the images
img1 = cv2.imread("base.png")
while 1:
    cv2.imshow("r1",img1)
    img2 = pyautogui.screenshot(region=(1360, 330, 480, 400))
    img2=np.array(img2)
    cv2.imshow("r2",img2)
    # Convert the images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Binarize the images
    _, thresh1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_OTSU)
    _, thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_OTSU)

    # Perform a bitwise AND operation
    and_result = cv2.bitwise_and(thresh1, thresh2)
    cv2.imshow("test",and_result)

    # Count the number of non-zero pixels
    non_zero_count = cv2.countNonZero(and_result)

    # If the number of non-zero pixels is above a certain threshold, conclude that the images overlap
    if non_zero_count > 100:
        print("The images overlap.{}".format(non_zero_count))
    else:
        print("The images do not overlap.{}".format(non_zero_count))

#while 1:
    if cv2.waitKey(1) == 27:
        break