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

#[[259.5, 0.2727077007293701], [278.0, 0.9599311], [-68.0, 2.1816616], [542.0, 0.9599311], [321.0, 2.1816616]]  
#[[269.75, 0.11999138444662094], [196.0, 2.1816616], [542.0, 0.9599311], [-68.0, 2.1816616], [321.0, 2.1816616]] 
#[[202.5, 0.2727077007293701], [278.0, 0.9599311], [542.0, 0.9599311], [321.0, 2.1816616], [-68.0, 2.1816616]]

#[269.75, 0.11999138444662094], [196.0, 2.1816616], [-68.0, 2.1816616], [542.0, 0.9599311], [321.0, 2.1816616]
#[[312.25, 0.23998276889324188], [227.0, 2.1816616], [-117.0, 2.1816616], [-148.0, 2.1816616], [321.0, 2.1816616], [309.0, 0.9599311], [-37.0, 2.1816616]]
#[[551.5, 0.47996553778648376], [227.0, 2.1816616], [247.0, 2.1816616], [309.0, 0.9599311], [-37.0, 2.1816616], [543.0, 0.9599311]]
#base_arr_hor=[[244.25, 0.0], [138.0, 2.1816616], [-103.0, 2.1816616], [252.0, 2.1816616], [418.0, 0.9599311], [178.0, 0.9599311]]
#base_arr_hor=[[-68.0, 2.1816616], [542.0, 0.9599311], [321.0, 2.1816616],[259.5, 0.2727077007293701]]
base_arr_hor=[[542.0, 0.9599311], [196.0, 2.1816616],[278.0, 0.9599311],  [-130.0, 2.1816616],[133.0, 2.1816616],[164.0, 2.1816616],[-68.0, 2.1816616] ]#[-68.0, 2.1816616]
#[[187.0, 0.0], [538.0, 0.9599311], [192.0, 2.1816616], [286.0, 2.1816616], [275.0, 0.9599311], [-71.0, 2.1816616], [255.0, 2.1816616], [725.0, 0.9599311]]
#[[358.5, 0.0], [-130.0, 2.1816616], [133.0, 2.1816616], [196.0, 2.1816616], [227.0, 2.1816616], [479.0, 0.9599311], [216.0, 0.9599311], [667.0, 0.9599311]]
#[[358.5, 0.0], [133.0, 2.1816616], [196.0, 2.1816616], [479.0, 0.9599311], [227.0, 2.1816616], [-130.0, 2.1816616], [216.0, 0.9599311], [667.0, 0.9599311]]
#[[301.25, 0.0], [-130.0, 2.1816616], [479.0, 0.9599311], [133.0, 2.1816616], [216.0, 0.9599311], [321.0, 2.1816616], [667.0, 0.9599311], [164.0, 2.1816616]]
#[[301.25, 0.0], [-130.0, 2.1816616], [133.0, 2.1816616], [479.0, 0.9599311], [216.0, 0.9599311], [321.0, 2.1816616], [667.0, 0.9599311]]

# [[358.5, 0.0], [247.0, 0.9599311], [-99.0, 2.1816616], [196.0, 2.1816616], [227.0, 2.1816616], [165.0, 2.1816616], [510.0, 0.9599311], [667.0, 0.9599311]]
# [[301.5, 0.0], [196.0, 2.1816616], [278.0, 0.9599311], [393.0, 0.9599311], [227.0, 2.1816616], [165.0, 2.1816616], [657.0, 0.9599311], [-98.0, 2.1816616]]
#[[301.25, 0.0], [408.0, 0.9599311], [196.0, 2.1816616], [439.0, 0.9599311], [164.0, 2.1816616], [227.0, 2.1816616], [542.0, 0.9599311], [144.0, 0.9599311], [667.0, 0.9599311], [-99.0, 2.1816616]]
#[[301.5, 0.0], [196.0, 2.1816616], [278.0, 0.9599311], [165.0, 2.1816616], [227.0, 2.1816616], [681.0, 0.9599311], [650.0, 0.9599311], [-98.0, 2.1816616]]
#

#base_arr_vert=[[244.25, 0.0], [149.0, 0.9599311], [390.0, 0.9599311], [252.0, 2.1816616], [-11.5, 2.181661605834961]]
base_arr_vert=[[530.0, 0.0], [73.0, 0.0],[358.5, 0.0], [247.0, 0.9599311] , [510.0, 0.9599311], [321.0, 2.1816616], [301.0, 0.0], [541.0, 0.9599311], [513.0, 0.94247776]]

while (True):
    st=time.time()
    img = pyautogui.screenshot(region=(660, 270, 600, 600))
    image = np.array(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection to the image
    edges = cv2.Canny(gray, 30, 120)
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
                    overlapval1=abs(m - m_merged).round()
                    overlapval2=abs(b - b_merged).round()
                    
                    
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
        if(overlap):
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
                if(np.count_nonzero(np.isin(np.array(merged_lines),base_arr_hor)) >=2 ):
                    time.sleep(1.46)
                    pyautogui.click(duration=0)
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
                    direction=1
            elif(direction==1):
                if(np.count_nonzero(np.isin(np.array(merged_lines),base_arr_vert)) >=2 ):
                    time.sleep(1.46)
                    pyautogui.click(duration=0)
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
                    direction=0
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
        #if(np.allclose(merged_lines,base_arr)):
        cv2.imshow("Image with Merged Lines", image)
            
        if cv2.waitKey(1) == 27:
                break
cv2.destroyAllWindows()