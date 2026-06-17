import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

# dir: R.jpg

#--------------------------------------------------Image Show--------------------------------------------------#

img = cv.imread('Code - Computer Vision\img.jpg',1) # after the file dir the num will be (1/0/-1)
# 1 RGB 0 grayscale -1 original
cv.imshow("caption",img)
cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

#--------------------------------------------------Video Show--------------------------------------------------#

capture = cv.VideoCapture('Code - Computer Vision\Sequence 01.mp4') # read from file dir
capture = cv.VideoCapture(0) # read from webcam | 0 is the default webcam, if you have multiple webcams, you can use 1, 2, etc. to access them

while True: # NOT REOCMMENDED
    isTrue, frame = capture.read() # capture frame by frame
    cv.imshow('Video',frame) # show every frame
    if cv.waitKey(20) & 0xFF ==ord('d'): # if press d to destroy window
        break

while(capture.isOpened()): # check if the video is opened | SAFER 
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


#--------------------------------------------------Resize--------------------------------------------------#

#alternative
h, w, _ = frame.shape()
frame_resized = cv.resize(frame, (w//2, h//2)) # resize to half the size | interpolation = method of resizing (INTER_AREA for smaller, INTER_CUBIC for larger but slower)

#Scale
def rescaleFrame(frame, scale):
    # .shape = height[0], width[1], layers/channel [2]
    width=int(frame.shape[1]*scale)
    height=int(frame.shape[0]*scale)
    dimension=(width,height)
    return cv.resize(frame,dimension, interpolation=cv.INTER_AREA)

cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

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

# === INTERPOLATION CHEAT SHEET ===
# Shrink -> cv.INTER_AREA (Prevents jagged edges/moiré)
# Enlarge -> cv.INTER_CUBIC (Sharp/smooth, slow) or cv.INTER_LINEAR (Default, fast)
# Pixel Art / AI Masks -> cv.INTER_NEAREST (No blur, keeps crisp blocks)
# Max Quality Zoom -> cv.INTER_LANCZOS4 (8x8 neighborhood, slowest)
# NOTE: img.shape is (H, W) but cv.resize() needs (W, H)

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

# Error 215 = dir no find 

#---------------------------------Example vid---------------------------------------------#

img = cv.imread('Code - Computer Vision\img.jpg',1) # after the file dir the num will be (1/0/-1)
# 1 RGB 0 grayscale -1 original
resized_img = rescaleFrame(img,scale=0.5)
cv.imshow("caption",resized_img)
cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

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


#--------------------------------------------------Draw Write--------------------------------------------------#

blank = np.zeros((500,500),dtype='uint8') #blank canvas | 1 channel | 500x500 dimension
cv.imshow('blank',blank)
img = cv.imread('Code - Computer Vision\img.jpg',1) # after the file dir the num will be (1/0/-1)
# 1 RGB 0 grayscale -1 original
cv.imshow("caption",img)

# === QUICK SUMMARY ===
# blank = np.zeros(img.shape, dtype='uint8')     -> 3-Channel Black Image (For Color Drawing)
# blank = np.zeros(img.shape[:2], dtype='uint8') -> 1-Channel Black Image (For Masking / Stencils)

#paint img certain color
blank[:] = 0,255,0
cv.imshow('green',blank)

# draw rectangle
cv.rectangle(blank,(0,0),(250,250),(0,250,0),thickness=2)
# (0,0) start coord | (250,250) Dimension | (0,250,0) Color
cv.rectangle(blank,(0,0),(250,250),(0,250,0),thickness=cv.FILLED)
cv.rectangle(blank,(0,0),(250,250),(0,250,0),thickness=cv-1)
cv.rectangle(blank,(0,0),(blank.shape[1]//2,blank.shape[0]//2),(0,250,0),thickness=cv-1) # quadrant 2
cv.imshow('rectangle',blank)

# circle
cv.circle(blank,(250,250),(blank.shape[1]//2,blank.shape[0]//2),40,(0,250,0),thickness=-1) # 40 is the radiyus
cv.imshow('circle',blank)

#line
cv.line(blank,(0,0),(blank.shape[1]//2,blank.shape[0]//2),(255,250,255),thickness=3)
cv.line(blank,(0,0),(300,400),(255,250,255),thickness=3) # coord 1 - 2
cv.imshow('line',blank)

# text on img
cv.putText(blank,'hello',(255,255),cv.FONT_HERSHEY_COMPLEX,1.0,(255,255,0), 2)
cv.imshow('text',blank)
# text payload, init position, font,scale,color,thickness

cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

#--------------------------------------------------Basic function--------------------------------------------------#

# Grayscale converter
img = cv.imread('Code - Computer Vision\img.jpg') # after the file dir the num will be (1/0/-1)
# 1 BGR 0 grayscale -1 original
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow("gray",gray)

cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

#Blur
blur = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT) # Odd number in blur control
cv.imshow("blur", blur)

# Flow: Detect Edge (Canny) -> Highlight it (Dialte) -> Precision Marking (Eroding)
# Edge Cascade | Canny
canny = cv.Canny(img,125,175) # threshold value
canny = cv.Canny(blur,125,175) # use blur if want les edges
cv.imshow("canny",canny)

# Dialating image | expand or thicken the white edgeafter edge detection (+)
dialated = cv.dialate(canny,(3,3),iterations=1)
cv.imshow("dialated",dialated)

# Eroding  image | make the edge detection thinner (-)
eroded = cv.erode(dialated,(3,3),iterations=1)
cv.imshow("eroded",eroded)


# Cropping
cropped = img[50:200,200:400] # (x,y) ps. 00 is topleft 
cv.imshow("crop",cropped)

# translation
def translate(img,x,y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1],img.shape[0])
    return cv.warpAffine(img,transMat,dimensions)

# -x left -y up | x right y down
translated = translate(img,100,100)
cv.imshow("translated",translated) 
cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows

# Rotation
rotated_90 = cv.rotate(cropped, cv.ROTATE_90_CLOCKWISE) #Alternative rotate 90 degree clockwise ROTATE_90_COUNTERCLOCKWISE | ROTATE_180

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


mat = np.float32([[0.5,0,0], #shrink img by 50% | 0.5 is the scale factor for x-axis, 0 is the shear factor for x-axis, 0 is the translation factor for x-axis | 0 is the shear factor for y-axis, 0.5 is the scale factor for y-axis, 0 is the translation factor for y-axis
                 [0,0.5,0]])
rotate = cv.warpAffine(img,mat,(img.shape[1],img.shape[0]))
cv.imshow('rotated_90', rotate)

mat = np.float32([[1,0,100], # move img 100 pixels to the right and 100 pixels down | 1 is the scale factor for x-axis, 0 is the shear factor for x-axis, 100 is the translation factor for x-axis | 0 is the shear factor for y-axis, 1 is the scale factor for y-axis, 100 is the translation factor for y-axis
                 [0,1,100]]) 
rotate = cv.warpAffine(img,mat,(img.shape[1],img.shape[0]))
cv.imshow('rotated_90', rotate)

# (R, theta) coordinate system can be use to replace xy coordinate system in rotation


rotated_90 = cv.rotate(img, cv.ROTATE_90_CLOCKWISE) # rotate 90 degree clockwise
cv.imshow('rotated_90', rotated_90)
cv.waitKey(0)
cv.destroyAllWindows




#flipping
flip = cv.flip(img,0) # 0 vertical | 1 horizontal | -1 both
cv.imshow("flip",flip)

# cropping 
cropped = img[200:400,300:500] # (y,x) ps. 00 is topleft
cv.imshow("crop",cropped)



# === THE VISION PIPELINE LAYER ===
# 1. cv.threshold() -> BINARIZES: Converts image to clean, solid black & white blocks.
# 2. cv.Canny()     -> PLOTS EDGES: Scans blocks and highlights individual boundary pixels.
# 3. findContours() -> CONNECTS DOTS: Links those pixels into an organized list of shapes.

# contours (its a list btw) | maybe be blur it before doing contour
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow("gray",gray)
canny = cv.Canny(img,125,175) # posible to use threshold instead of canny
cv.imshow("canny",canny)

# thresholding
ret,thresh = cv.threshold(gray,150,255,cv.THRESH_BINARY) # threshold value | black and white value | type of threshold
cv.imshow("thresh",thresh)

# here you can choose canny or thresh for contour detection, but canny is more common for edge detection
contours,hierarchies = cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_NONE) # RETR reutrieval mode | CHAIN_APPROX contour approximation method 
#chain approx give all contour points | chain approx simple give start and end point of contour

blank = np.zeros(img.shape[:2],dtype='uint8')
cv.drawContours(blank,contours,-1(0,0,255),2) # page, point, how many data, color, thickness
cv.imshow("contours drawn",blank)

cv.waitKey(0) # press 0 to destroy window
cv.destroyAllWindows()

#--------------------------------------------------Color spaces--------------------------------------------------#

# BGR -> Grayscale
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow("gray",gray)

# BGR -> HSV
hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
cv.imshow("hsv",hsv)

# BGR -> LAB
lab = cv.cvtColor(img,cv.COLOR_BGR2LAB)
cv.imshow("lab",lab)

# BGR -> RGB
rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
cv.imshow("rgb",rgb)

plt.imshow(rgb) # use plt to show rgb img because cv.imshow will show in bgr
plt.show()

