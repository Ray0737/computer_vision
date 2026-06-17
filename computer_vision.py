"""
============================================================================
 Computer Vision -- TRADITIONAL (procedural) style
============================================================================
Same operations as preset.py, but written the cv.py way: plain inline
functions (rotate, translate, rescale) defined and called directly, top to
bottom. No imports of preset -- everything is here in one runnable script.

Runs section by section: each cv.imshow + cv.waitKey(0) BLOCKS until you
press a key. Video sections quit on 'd'.
============================================================================
"""

import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# paths (resolved next to this file so it runs from anywhere)
HERE = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(HERE, 'img.jpg')
VIDEO_PATH = os.path.join(HERE, 'Sequence 01.mp4')


# ============================================================================
# 1. READ & SHOW AN IMAGE
# ============================================================================
img = cv.imread(IMG_PATH, 1)          # 1 color (BGR) | 0 gray | -1 alpha
cv.imshow('Original', img)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 2. READ & SHOW A VIDEO  (press 'd' to quit)
# ============================================================================
capture = cv.VideoCapture(VIDEO_PATH)     # path for a file, or 0 for webcam
while capture.isOpened():
    ret, frame = capture.read()
    if not ret:                           # no frame -> video ended
        break
    cv.imshow('Video', frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
capture.release()
cv.destroyAllWindows()


# ============================================================================
# 3. RESCALE BY A FACTOR  (function -- works on image or video frame)
# ============================================================================
def rescale(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

img = cv.imread(IMG_PATH, 1)
cv.imshow('Rescaled 0.5x', rescale(img, 0.5))
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 4. RESIZE -- exact size, and via an affine matrix
# ============================================================================
img = cv.imread(IMG_PATH, 1)

resized = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)   # (W, H)
cv.imshow('Resized 500x500', resized)

# resize using the matrix diagonal (0.5 = half) -- same idea as translate/rotate
scale_mat = np.float32([[0.5, 0, 0],
                        [0, 0.5, 0]])
scaled = cv.warpAffine(img, scale_mat, (img.shape[1], img.shape[0]))
cv.imshow('Resized via matrix', scaled)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 5. DRAW SHAPES & TEXT  (on a blank canvas)
# ============================================================================
blank = np.zeros((500, 500, 3), dtype='uint8')   # (H, W, 3) black canvas

cv.rectangle(blank, (50, 50), (200, 200), (0, 255, 0), thickness=2)    # -1 fills
cv.circle(blank, (350, 150), 60, (0, 0, 255), thickness=-1)            # radius 60
cv.line(blank, (0, 0), (500, 500), (255, 255, 255), thickness=3)
cv.putText(blank, 'hello', (120, 420), cv.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 0), 2)
cv.imshow('Drawing', blank)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 6. TRANSFORMS -- crop, translate, rotate, flip  (functions)
# ============================================================================
img = cv.imread(IMG_PATH, 1)

# --- crop (array slicing: [y1:y2, x1:x2]) ---
cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)

# --- translate (shift) ---
def translate(img, x, y):                 # +x right, -x left, +y down, -y up
    mat = np.float32([[1, 0, x], [0, 1, y]])
    return cv.warpAffine(img, mat, (img.shape[1], img.shape[0]))

cv.imshow('Translated', translate(img, 100, 100))

# --- rotate (around a point; center if none) ---
def rotate(img, angle, rotPoint=None):    # angle in degrees, CCW positive
    (height, width) = img.shape[:2]
    if rotPoint is None:
        rotPoint = (width // 2, height // 2)
    mat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    return cv.warpAffine(img, mat, (width, height))

cv.imshow('Rotated 45', rotate(img, 45))

# --- flip ---
flipped = cv.flip(img, 0)                 # 0 vert | 1 horiz | -1 both
cv.imshow('Flipped', flipped)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 7. COLOR SPACES
# ============================================================================
img = cv.imread(IMG_PATH, 1)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

cv.imshow('Gray', gray)
cv.imshow('HSV', hsv)
cv.imshow('LAB', lab)
cv.waitKey(0)
cv.destroyAllWindows()

plt.imshow(rgb)                           # matplotlib needs RGB, not BGR
plt.title('matplotlib (RGB)')
plt.axis('off')
plt.show()


# ============================================================================
# 8. VISION PIPELINE -- gray -> blur -> canny -> contours
# ============================================================================
img = cv.imread(IMG_PATH, 1)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)    # odd kernel
canny = cv.Canny(blur, 125, 175)                           # lower = more edges
cv.imshow('Canny', canny)

# threshold alternative
ret, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
cv.imshow('Threshold', thresh)

# clean up the edges
dilated = cv.dilate(canny, (3, 3), iterations=1)           # thicken
eroded = cv.erode(dilated, (3, 3), iterations=1)           # thin

# find + draw contours
contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found')

blank = np.zeros(img.shape, dtype='uint8')                 # 3-channel for color
cv.drawContours(blank, contours, -1, (0, 0, 255), 2)       # -1 = draw all
cv.imshow('Contours', blank)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 9. COLOR CHANNELS -- split / merge
# ============================================================================
img = cv.imread(IMG_PATH, 1)

b, g, r = cv.split(img)                                     # 3 grayscale channels
cv.imshow('Blue (gray)', b)
cv.imshow('Green (gray)', g)
cv.imshow('Red (gray)', r)

# show a channel in ITS color: merge it with two blank channels
zero = np.zeros(img.shape[:2], dtype='uint8')
cv.imshow('Blue (color)', cv.merge([b, zero, zero]))       # B, G=0, R=0
cv.imshow('Red (color)', cv.merge([zero, zero, r]))

merged = cv.merge([b, g, r])                                # rebuild the original
cv.imshow('Merged back', merged)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 10. BITWISE -- and / or / xor / not  (inputs must be the SAME size)
# ============================================================================
rect = np.zeros((400, 400), dtype='uint8')
cv.rectangle(rect, (30, 30), (370, 370), 255, thickness=-1)    # filled white box

circle = np.zeros((400, 400), dtype='uint8')
cv.circle(circle, (200, 200), 200, 255, thickness=-1)          # filled white circle

cv.imshow('AND (overlap)', cv.bitwise_and(rect, circle))       # where BOTH white
cv.imshow('OR (both)', cv.bitwise_or(rect, circle))            # where EITHER white
cv.imshow('XOR (differ)', cv.bitwise_xor(rect, circle))        # non-overlap
cv.imshow('NOT (inverted)', cv.bitwise_not(rect))              # white <-> black

cv.waitKey(0)
cv.destroyAllWindows()
