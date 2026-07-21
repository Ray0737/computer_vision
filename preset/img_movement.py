import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

#--------------------------------------------------Image Movement--------------------------------------------------#
img = cv.imread('Code - Computer Vision\img.jpg',1)

def translate(img,x,y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1],img.shape[0])
    return cv.warpAffine(img,transMat,dimensions)

# -x left -y up | x right y down
translated = translate(img,100,100)
cv.imshow("translated",translated) 
cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

# alternative
mat = np.float32([[1,0,100], # move img 100 pixels to the right and 100 pixels down | 1 is the scale factor for x-axis, 0 is the shear factor for x-axis, 100 is the translation factor for x-axis | 0 is the shear factor for y-axis, 1 is the scale factor for y-axis, 100 is the translation factor for y-axis
                 [0,1,100]]) 
rotate = cv.warpAffine(img,mat,(img.shape[1],img.shape[0]))
cv.imshow('rotated_90', rotate)

#--------------------------------------------------Image Rotation--------------------------------------------------#

def rotate(img, angle, rotPoint=None):
    (height,width)=img.shape[:2] # Extracitng first 2 index | height = 0, width = 1
    if rotPoint is None: # rotPoint is rotating point
        rotPoint = (width//2,height//2) # default rotation point is the center of the img
    rotMat = cv.getRotationMatrix2D(rotPoint,angle,1.0) # rotation point, angle, scale
    dimensions = (width,height)
    return cv.warpAffine(img,rotMat,dimensions)

rotated = rotate(img,45) # img, degree
cv.imshow('rotated',rotated)
cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

#--------------------------------------------------Image Rotation--------------------------------------------------#

# (R, theta) coordinate system can be use to replace xy coordinate system in rotation
rotated_90 = cv.rotate(img, cv.ROTATE_90_CLOCKWISE) # rotate 90 degree clockwise
cv.imshow('rotated_90', rotated_90)
cv.waitKey(0)
cv.destroyAllWindows