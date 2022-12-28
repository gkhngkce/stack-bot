import cv2
import pyautogui
import numpy as np
import time


while (True):
    img = pyautogui.screenshot(region=(570, 375, 480, 360))
    frame = np.array(img)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Resmi oku
    image = frame
    # Gri seviyelerine dönüştür
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Gradient filtresi uygula
    #gradient = cv2.Laplacian(gray, cv2.CV_64F)
    edges = cv2.Canny(gray, threshold1=30, threshold2=120)
    

    # Gradient resmini binary seviyelerine dönüştür
    _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Dilate işlemini uygula (kenarları kalınlaştır)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(thresh, kernel)

    # Tresholding işlemini uygula (üst üste gelen iki şeklin kenarlarının çok yakın olduğu alanları tespit et)
    _, thresh2 = cv2.threshold(dilated, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Tespit edilen alanları göster
    cv2.imshow("Result", thresh2)
    #cv2.waitKey(0)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
