import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt

img = cv.imread('Code - Computer Vision\img.jpg') # after the file dir the num will be (1/0/-1)
# 1 BGR 0 grayscale -1 original
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
canny = cv.Canny(img,125,175)
ret,thresh = cv.threshold(gray,150,255,cv.THRESH_BINARY) # threshold value | black and white value | type of threshold
cv.imshow("thresh",thresh)

contours,hierarchies = cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_NONE) # RETR reutrieval mode | CHAIN_APPROX contour approximation method 
#chain approx give all contour points | chain approx simple give start and end point of contour

blank = np.zeros(img.shape,dtype='uint8')
cv.drawContours(blank,contours,-1,(0,0,255),2) # page, point, how many data, color, thickness
cv.imshow("contours drawn",blank)
cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows
