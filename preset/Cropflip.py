import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale


img = cv.imread('Code - Computer Vision\img.jpg')

#flipping
flip = cv.flip(img,0) # 0 vertical | 1 horizontal | -1 both
cv.imshow("flip",flip)

# cropping 
cropped = img[200:400,300:500] # (y,x) ps. 00 is topleft
cv.imshow("crop",cropped)