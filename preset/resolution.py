import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

#--------------------------------------------------Change resolution--------------------------------------------------#
def changeRes(width,height):
    #live vid
    capture.set(3,width)
    capture.set(4,height)

def changeRes(width, height):
    # This is exactly the same as capture.set(3, width)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
    
    # This is exactly the same as capture.set(4, height)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)

# --- OPENCV CAPTURE PROPERTY QUICK CHEAT SHEET ---
# Usage: capture.get(ID) or capture.set(ID, value)

# ID | OpenCV Property Name             | What it controls
# ---------------------------------------------------------------------
# 0  | cv.CAP_PROP_POS_MSEC            | Video position (milliseconds)
# 1  | cv.CAP_PROP_POS_FRAMES          | Next frame index (0-based)
# 2  | cv.CAP_PROP_POS_AVI_RATIO       | Video relative position (0.0 to 1.0)
# 3  | cv.CAP_PROP_FRAME_WIDTH         | Frame width
# 4  | cv.CAP_PROP_FRAME_HEIGHT        | Frame height
# 5  | cv.CAP_PROP_FPS                 | Frame rate (Frames Per Second)
# 6  | cv.CAP_PROP_FOURCC              | 4-character codec code (e.g., 'MJPG')
# 7  | cv.CAP_PROP_FRAME_COUNT         | Total frame count (video files)
# 8  | cv.CAP_PROP_FORMAT              | Mat image format
# 10 | cv.CAP_PROP_BRIGHTNESS          | Camera brightness
# 11 | cv.CAP_PROP_CONTRAST            | Camera contrast
# 12 | cv.CAP_PROP_SATURATION          | Camera saturation
# 13 | cv.CAP_PROP_HUE                 | Camera hue
# 14 | cv.CAP_PROP_GAIN                | Camera gain
# 15 | cv.CAP_PROP_EXPOSURE            | Camera exposure (often negative)
# 16 | cv.CAP_PROP_CONVERT_RGB         | Boolean flag to convert to RGB
# 17 | cv.CAP_PROP_WHITE_BALANCE_BLUE_U| White balance temperature
# 32 | cv.CAP_PROP_RECTIFICATION       | Stereo camera rectification flag
# 38 | cv.CAP_PROP_ZOOM                | Camera hardware zoom
# 39 | cv.CAP_PROP_FOCUS               | Camera hardware focus
# 40 | cv.CAP_PROP_AUTO_EXPOSURE       | Auto exposure mode (0=manual, 1=auto)

#--------------------------------------------------Video Show--------------------------------------------------#

capture = cv.VideoCapture('Code - Computer Vision\Sequence 01.mp4') # read from file dir

while(capture.isOpened()): 
    ret, frame = capture.read() 
    if ret == True:
        frame_resized = changeRes(320, 240) # change resolution to 320x240
        cv.imshow('Frame', frame)
        key =  cv.waitKey(33)
        if key == ord('d'): 
             break
        if cv.waitKey(25) & 0xFF == ord('d'):
            break
    else:
        break
    
capture.release() 
cv.destroyAllWindows()