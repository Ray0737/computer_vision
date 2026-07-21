import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

#--------------------------------------------------Image Show--------------------------------------------------#

img = cv.imread('Code - Computer Vision\img.jpg',1) # after the file dir the num will be (1/0/-1)
# 1 RGB 0 grayscale -1 original
cv.imshow("caption",img)
cv.waitKey(0)
cv.destroyAllWindows

#--------------------------------------------------Video Show--------------------------------------------------#

capture = cv.VideoCapture('Code - Computer Vision\Sequence 01.mp4') # read from file dir
capture = cv.VideoCapture(0) # read from webcam | 0 is the default webcam, if you have multiple webcams, you can use 1, 2, etc. to access them

while(capture.isOpened()): 
    ret, frame = capture.read() # ret is boolean value to check if the frame is read correctly, frame is the actual frame
    if ret == True:
        cv.imshow('Frame', frame)
        key =  cv.waitKey(33)
        if key == ord('d'): # if press d to destroy window
             break
        if cv.waitKey(25) & 0xFF == ord('d'): # wait key is how many sec u transition
            break
    else:
        break
    
capture.release() 
cv.destroyAllWindows()

# Error 215 = dir no find 

