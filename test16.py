from operator import le

import cv2 as cv
import numpy as np
import random

# 1. Load the image and verify it exists
canvas = cv.imread('Code - Computer Vision/test2.png', 1)
t = 'Click to draw'
list = []

# 2. Define the callback function
def on_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        global initx, inity, drawing, canvas
        initx, inity = x, y 
        list.append((x, y)) 
        cv.circle(canvas, (initx, inity), 6, (0, 255, 0), thickness=-1)
        cv.imshow(t, canvas)                
        cv.waitKey(1)                                    
    elif event == cv.EVENT_LBUTTONUP:
        # Left button released
        temp_canvas = canvas.copy()
        currentx, currenty = x, y
        cv.line(temp_canvas, (initx, inity), (currentx, currenty), (0, 255, 0), thickness=2)
        cv.imshow(t, temp_canvas) 
        finalx, finaly = x, y
        list.append((finalx, finaly))
        cv.circle(canvas, (finalx, finaly), 6, (0, 255, 0), thickness=-1)
        cv.imshow(t, canvas)                
        cv.waitKey(1)    

        cornerA = initx, inity
        cornerB = finalx, finaly
        cornerC = (initx, finaly)
        cv.line(canvas, cornerA, cornerB, (0, 255, 0), thickness=2)
        cv.line(canvas, cornerA, cornerC, (0, 0, 255), thickness=2)
        cv.line(canvas, cornerB, cornerC, (255, 0, 0), thickness=2)

        cv.imshow(t, canvas)
        cv.waitKey(1) 
# 3. Setup the window and event listener
cv.namedWindow(t)                               # Explicitly create named window
cv.imshow(t, canvas)                      
cv.setMouseCallback(t, on_mouse)             
cv.waitKey(0)                                   
cv.destroyAllWindows()