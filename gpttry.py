import cv2
import numpy as np
import pyautogui
import time
import random as rnd
import math


# Load the image and convert it to grayscale
#image = cv2.imread('image.jpg')
time.sleep(2)
count=0
direction=0
overlapval1=0
overlapval2=0
st=0
et=0
delayTime=1.48
score=0
edgesToCheck=3


refPt = []
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,",",y)
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x)+", "+str(y)
        cv2.putText(image, strXY, (x,y), font, 0.5, (255,255,0), 2)
        cv2.imshow("Overlapped Edges", image)
        print(merged_lines)
        cv2.imwrite("./captured/saved.jpg",image)


#base_arr_hor=[[542.0, 0.9599311], [196.0, 2.1816616],[278.0, 0.9599311],  [-130.0, 2.1816616],[133.0, 2.1816616],[164.0, 2.1816616],[-68.0, 2.1816616]]#[-68.0, 2.1816616]
base_arr_hor=[[[196.0, 2.1816616], [278.0, 0.9599311], [542.0, 0.9599311],[278.0, 0.9599311]]]
base_arr_hor2=[[[133.0, 2.1816616], [216.0, 0.9599311], [479.0, 0.9599311], [-130.0, 2.1816616]]]
base_arr_hor_final=[[[132.0, 2.1816616], [214.0, 0.9599311], [-131.0, 2.1816616], [478.0, 0.9599311]]]
base_arr_hor_final2=[[[133.0, 2.1816616], [215.0, 0.9599311], [-130.0, 2.1816616], [479.0, 0.9599311]]]
#[[163.375, 0.0], [478.0, 0.9599311], [132.0, 2.1816616], [-131.0, 2.1816616], [237.0, 0.9599311]]
#[[301.25, 0.0], [132.0, 2.1816616], [478.0, 0.9599311], [509.0, 0.9599311], [214.0, 0.9599311], [163.0, 2.1816616], [288.0, 2.1816616], [226.0, 2.1816616], [195.0, 2.1816616], [-131.0, 2.1816616], [319.0, 2.1816616]]
horizontalAngleList=[2.18166161,0.95993108]
lowerTrash=5
upperTrash=80
#base_arr_vert=[[244.25, 0.0], [149.0, 0.9599311], [390.0, 0.9599311], [252.0, 2.1816616], [-11.5, 2.181661605834961]]
#base_arr_vert=[[530.0, 0.0], [73.0, 0.0],[358.5, 0.0], [247.0, 0.9599311] , [510.0, 0.9599311], [321.0, 2.1816616], [301.0, 0.0], [541.0, 0.9599311], [513.0, 0.94247776]]
base_arr_vert=[[[247.0, 0.9599311], [-99.0, 2.1816616], [510.0, 0.9599311], [165.0, 2.1816616]]]
base_arr_vert2=[[[215.0, 0.9599311], [-131.0, 2.1816616], [478.0, 0.9599311],[132.0, 2.1816616]]]
base_arr_vert_final=[[[214.0, 0.9599311], [-132.0, 2.1816616], [477.0, 0.9599311],[131.0, 2.1816616]]]
base_arr_vert_final2=[[[215.0, 0.9599311], [-131.0, 2.1816616], [478.0, 0.9599311],[132.0, 2.1816616]]]
#[[132.0, 2.1816616], [478.0, 0.9599311], [215.0, 0.9599311], [-131.0, 2.1816616], [696.0, 0.9599311], [351.0, 2.1816616]]
st=time.time()
#maske = cv2.imread("./captured/mask.jpg",cv2.COLOR_BGR2GRAY)
while (True):
    
    img = pyautogui.screenshot(region=(660, 270, 600, 600))
    image = np.array(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #blurred = cv2.GaussianBlur(image, (1, 1), 0)

    #v = np.median(gray)
    #lower = int(max(0, (1.0 - 0.1) * v))
    #upper = int(min(255, (1.0 + 0.1) * v))
    #edges = cv2.Canny(gray, lower, upper)

    #masked = cv2.bitwise_and(maske, gray)
    #cv2.imshow("masked",gray)
    #gray=cv2.equalizeHist(gray)
    #cv2.imshow("edged",edged)
    #thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
    
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    #dilate = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

    #diff = cv2.absdiff(dilate, thresh)
    #edges = 255 - diff
    #cv2.imshow("test",edges)

    # Apply edge detection to the image
    edges = cv2.Canny(gray, lowerTrash, upperTrash)
    #cv2.imshow("edged",edged)

    #cv2.imwrite("test.jpg",edges)
    # Use the HoughLines function to detect lines in the image
    lines = cv2.HoughLines(edges, 1, np.pi/180, 120, None, 0, 0)

    # Create an empty list to store the merged lines
    merged_lines = []
    
    # Iterate through the list of lines and check for overlaps
    if(lines is not None):
        for line in lines:
            rho, theta = line[0]
            m = -1 * np.cos(theta) / np.sin(theta)
            b = rho / np.sin(theta)
            
            # Check if the current line overlaps with any of the merged lines
            overlap = False
            #print(merged_lines)
            for merged_line in merged_lines:
                m_merged, b_merged = merged_line
                #print("{}  -  {}".format(abs(m - m_merged).round(),abs(b - b_merged).round()))
                #(abs(m - m_merged).round() >= 130.0 and abs(m - m_merged).round() <= 140.0  and abs(b - b_merged).round() >= 130.0 and abs(b - b_merged).round() <= 140.0)) or 
                if (abs(m - m_merged).round() >= math.inf and abs(b - b_merged).round() <= math.inf):
                #if ((abs(m - m_merged).round() >= 130.0 and abs(m - m_merged).round() <= 140.0  and abs(b - b_merged).round() >= 130.0 and abs(b - b_merged).round() <= 140.0)):
                    # The current line overlaps with a merged line, so we update the merged line with the average rho and theta values
                    
                    rho_new = (rho + merged_line[0]) / 2
                    theta_new = (theta + merged_line[1]) / 2
                    merged_line[0] = rho_new
                    merged_line[1] = theta_new
                    overlap = True
                    
                    
                    #print(line)
                    break
            #print("***********")    
            if not overlap:
                # The current line does not overlap with any merged lines, so we add it to the list
                merged_lines.append([rho, theta])

        # Draw the merged lines on the image
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
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        #print(base_arr)
        # Show the image with the merged lines
        #print(np.array(horizontalAngleList,dtype=float))
        #print(np.array(merged_lines,dtype=float)[:,1])
        #print(np.isin(np.array(merged_lines,dtype=float)[:,1].sort(),np.array(horizontalAngleList,dtype=float).sort()))
        #if(merged_lines is not None):
            #print(np.array(merged_lines,dtype=float))
            #print(np.array(merged_lines,dtype=float)[:,1])
        

        #new try
        #print(np.array(lines).flatten())
        #result=np.count_nonzero(np.isin(np.array(lines,dtype=float),np.array(base_arr_hor,dtype=float)).any(axis=1))
        #print(lines)
        #print("------------")
        #print(np.array(base_arr_hor))
        if direction==0:
            if(np.count_nonzero(np.isin(np.array(lines,dtype=float),np.array(base_arr_hor,dtype=float)).any(axis=1))>=edgesToCheck or (np.count_nonzero(np.isin(np.array(lines,dtype=float),np.array(base_arr_hor_final2,dtype=float)).any(axis=1))>=edgesToCheck and score>=2)):
                st=time.time()
                time.sleep(delayTime)
                pyautogui.click()
                #print("hor")
                cv2.imwrite("./captured/{}.jpg".format(count),image)
                
                score+=1
                print(upperTrash)
                lowerTrash=0
                direction=1
                edgesToCheck=3
                print("HORİZONTAL - Count:{} ".format(count))
                print("Merged lines: ",merged_lines)
                count+=1
                #delayTime-=0.1
                if(score==15):
                    delayTime-=0.05
        elif direction==1:
            if(np.count_nonzero(np.isin(np.array(lines,dtype=float),np.array(base_arr_vert,dtype=float)).any(axis=1))>=edgesToCheck or (np.count_nonzero(np.isin(np.array(lines,dtype=float),np.array(base_arr_vert_final2,dtype=float)).any(axis=1))>=edgesToCheck and score>=2)):
                st=time.time()
                time.sleep(delayTime)
                pyautogui.click()
                #print("vert")
                print(upperTrash)
                cv2.imwrite("./captured/{}.jpg".format(count),image)
                
                score+=1
                lowerTrash=0
                direction=0
                edgesToCheck=3
                print("VERTICAL - Count:{} ".format(count))
                print("Merged lines: ",merged_lines)
                count+=1
                #delayTime-=0.1
        if(score==1):
            base_arr_hor=base_arr_hor2
        elif(score==2):
            base_arr_vert=base_arr_vert2
        elif(score==3):
            base_arr_hor=base_arr_hor_final
            #delayTime-=0.1
        elif(score==4):
            base_arr_vert=base_arr_vert_final
        #fail
        '''if overlap:
            #print(np.array(merged_lines,dtype=float)[:,1])
            #print(horizontalAngleList)
            if(np.count_nonzero(np.isin(np.array(merged_lines,dtype=float)[:,1].sort(),np.array(horizontalAngleList,dtype=float).sort())) >=2):
                print("got it")
                print(np.array(merged_lines,dtype=float)[:,1])
                print(horizontalAngleList)
                cv2.imwrite("./captured/{}.jpg".format(count),image)
                count+=1'''

        #meh one
        '''if(overlap):
            #print(count)
            #print(merged_lines)
            #print(base_arr_hor)
            #print(len(merged_lines))
            #cv2.imwrite("./captured/{}.jpg".format(count),image)
            #count+=1
            #if((len(merged_lines)==5 and np.allclose(merged_lines,base_arr_vert)) or (len(merged_lines)==6 and np.allclose(merged_lines,base_arr_hor))):
            #print(np.count_nonzero(np.isin(np.array(merged_lines),base_arr_hor)))
            #if(np.count_nonzero(np.array(merged_lines)==base_arr_hor)>=4 or np.count_nonzero(np.array(merged_lines)==base_arr_vert)>=4):
            if(direction==0):
                if(np.count_nonzero(np.isin(np.array(merged_lines),base_arr_hor2)) >=1 ):
                    #time.sleep(1.45)
                    #pyautogui.click()
                    print("HORİZONTAL - Count:{} Overlap val:{} merged count:{}".format(count,np.count_nonzero(np.isin(np.array(merged_lines),base_arr_hor)),len(merged_lines)))
                    print("Overlap val1:{} Overlap val2:{}".format(overlapval1,overlapval2))
                    print("Merged lines: ",merged_lines)
                    #print(base_arr)
                    #print(np.allclose(merged_lines,base_arr))
                    #if(np.allclose(merged_lines,base_arr)):
                    et=time.time()
                    print("elapsed:",et-st)
                    
                    cv2.imwrite("./captured/{}.jpg".format(count),image)
                    count+=1
                    #direction=1
            elif(direction==1):
                if(np.count_nonzero(np.isin(np.array(merged_lines),base_arr_vert)) >=3 ):
                    time.sleep(1.45)
                    pyautogui.click()
                    print("VERTICAL - Count:{} Overlap val:{} merged count:{}".format(count,np.count_nonzero(np.isin(np.array(merged_lines),base_arr_vert)),len(merged_lines)))
                    print("Overlap val1:{} Overlap val2:{}".format(overlapval1,overlapval2))
                    print("Merged lines: ",merged_lines)
                    #print(base_arr)
                    #print(np.allclose(merged_lines,base_arr))
                    #if(np.allclose(merged_lines,base_arr)):
                    
                    et=time.time()
                    print("elapsed:",et-st)
                    cv2.imwrite("./captured/{}.jpg".format(count),image)
                    count+=1
                    #direction=0
                    #print("-----------------")
                    #pyautogui.click()
        #print("HORİZONTAL - Count:{} Overlap val:{} merged count:{}".format(count,np.count_nonzero(np.isin(np.array(merged_lines),base_arr_hor)),len(merged_lines)))
        #print("Overlap val1:{} Overlap val2:{}".format(overlapval1,overlapval2))
        #print("Merged lines: ",merged_lines)
        #print("")
        
        #print("VERTICAL - Count:{} Overlap val:{} merged count:{}".format(count,np.count_nonzero(np.isin(np.array(merged_lines),base_arr_vert)),len(merged_lines)))
        #print("Overlap val1:{} Overlap val2:{}".format(overlapval1,overlapval2))
        #print("Merged lines: ",merged_lines)
        #print("")
        
        #cv2.imwrite("./captured/{}.jpg".format(count),image)
        #count+=1
        #print(base_arr)
        #print(np.allclose(merged_lines,base_arr))
        #if(np.allclose(merged_lines,base_arr)):'''
        #cv2.imshow("edges", edges)
        cv2.imshow("Image with Merged Lines", image)
        cv2.setMouseCallback("Image with Merged Lines", click_event)
        if(time.time()-st>60.0):
            print("Edges decreasing")
            if(edgesToCheck<=3):
                edgesToCheck-=1
                st=time.time()
            else:
                edgesToCheck=3
                st=time.time()
        if cv2.waitKey(1) == 27:
                break
cv2.destroyAllWindows()