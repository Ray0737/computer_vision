import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

#--------------------------------------------------Resized Hardcode size--------------------------------------------------#

capture = cv.VideoCapture('Code - Computer Vision\Sequence 01.mp4') # read from file dir

while(capture.isOpened()): # check if the video is opened | SAFER 
    ret, frame = capture.read() # ret is boolean value to check if the frame is read correctly, frame is the actual frame
    h, w, _ = frame.shape()
    frame_resized = cv.resize(frame, (w//2, h//2))
    if ret == True:
        cv.imshow('Frame', frame_resized)
        key =  cv.waitKey(33)
        if key == ord('d'): # if press d to destroy window
             break
        if cv.waitKey(25) & 0xFF == ord('d'): # wait key is how many sec u transition
            break
    else:
        break
    
capture.release() 
cv.destroyAllWindows()

#--------------------------------------------------Resized Function--------------------------------------------------#

#Scale Method
def rescaleFrame(frame, scale):
    # .shape = height[0], width[1], layers/channel [2]
    width=int(frame.shape[1]*scale)
    height=int(frame.shape[0]*scale)
    dimension=(width,height)
    return cv.resize(frame,dimension, interpolation=cv.INTER_AREA)

#---------------------------------Example vid---------------------------------------------#

capture = cv.VideoCapture('Code - Computer Vision\Sequence 01.mp4') # read from file dir

while True:
    isTrue, frame = capture.read() # capture frame by frame
    frame_resized = rescaleFrame(frame,scale=0.5)
    cv.imshow('Video',frame) # show every frame
    cv.imshow("resized",frame_resized) # show every resized frame
    if cv.waitKey(20) & 0xFF ==ord('d'): # if press d to destroy window
        break
    
capture.release() 
cv.destroyAllWindows()

#---------------------------------Example Img---------------------------------------------#

img = cv.imread('Code - Computer Vision\img.jpg',1) # after the file dir the num will be (1/0/-1)
# 1 RGB 0 grayscale -1 original
resized_img = rescaleFrame(img,scale=0.5)
cv.imshow("caption",resized_img)
cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

#--------------------------------------------------Resized Other method--------------------------------------------------#

# Resize Hard coded
resize = cv.resize(img,fx=0.5,fy=0.5,dsize=(0,0),interpolation=cv.INTER_AREA) #scle method hardcode | dsize = (0,0) means no specific size, just use fx and fy to scale | interpolation = method of resizing (INTER_AREA for smaller, INTER_CUBIC for larger but slower)
resized = cv.resize(img,(500,500)) # resize to 500x500
resized = cv.resize(img,(500,500), interpolation=cv.INTER_AREA)
resized = cv.resize(img,(500,500), interpolation=cv.INTER_CUBIC)
cv.imshow("resized",resized)

#resized 
# (x,y) = targeted dimension | interpolation = method of resizing (INTER_AREA for smaller, INTER_CUBIC for larger but slower)
resized_smaller = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA) 
resized_larger  = cv.resize(img, (1500, 1500), interpolation=cv.INTER_CUBIC) # larger but took longer time to process
resized_larger2  = cv.resize(img, (1500, 1500), interpolation=cv.INTER_LINEAR)
cv.imshow("resized larger", resized_larger2)

mat = np.float32([[0.5,0,0], #shrink img by 50% | 0.5 is the scale factor for x-axis, 0 is the shear factor for x-axis, 0 is the translation factor for x-axis | 0 is the shear factor for y-axis, 0.5 is the scale factor for y-axis, 0 is the translation factor for y-axis
                 [0,0.5,0]])
rotate = cv.warpAffine(img,mat,(img.shape[1],img.shape[0]))
cv.imshow('rotated_90', rotate)

# === INTERPOLATION CHEAT SHEET ===
# Shrink -> cv.INTER_AREA (Prevents jagged edges/moiré)
# Enlarge -> cv.INTER_CUBIC (Sharp/smooth, slow) or cv.INTER_LINEAR (Default, fast)
# Pixel Art / AI Masks -> cv.INTER_NEAREST (No blur, keeps crisp blocks)
# Max Quality Zoom -> cv.INTER_LANCZOS4 (8x8 neighborhood, slowest)
# NOTE: img.shape is (H, W) but cv.resize() needs (W, H)
