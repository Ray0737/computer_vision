"""
============================================================================
 OpenCV (cv2) -- COPY & RUN EXAMPLES
============================================================================
Each numbered section below is a SELF-CONTAINED mini-script for ONE trick.
To use one: copy the "SETUP" block at the top + the ONE section you want
into a new file (or just run this whole file -- each section pops its own
window(s), press any key to close them and move to the next section).

Lines marked `#!` are the values you'll most often want to TWEAK
(file paths, colors, coordinates, thresholds, kernel sizes, etc.).
For full explanations of WHY/HOW each function works, see summary.py.
============================================================================
"""

# ============================================================================
# SETUP -- copy these lines along with whatever section you copy
# ============================================================================
import cv2 as cv
import numpy as np

IMG_PATH = 'img.jpg'              #! path to your image
VIDEO_PATH = 'Sequence 01.mp4'    #! path to your video


# ============================================================================
# 1. Show an image
# ============================================================================
img = cv.imread(IMG_PATH, 1)      #! flag: 1=color, 0=grayscale, -1=unchanged
cv.imshow('Original Image', img)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 2. Play a video file (or webcam)
# ============================================================================
capture = cv.VideoCapture(VIDEO_PATH)   #! path to video, or 0 for default webcam

while True:
    isTrue, frame = capture.read()
    if not isTrue:                      # video ended
        break

    cv.imshow('Video Playback', frame)

    if cv.waitKey(20) & 0xFF == ord('d'):   #! 20 = ms between frames (lower = faster)
        break                                #! 'd' = key to quit early

capture.release()
cv.destroyAllWindows()


# ============================================================================
# 3. Rescale by a SCALE FACTOR (works on an image OR a video frame)
# ============================================================================
def rescaleFrame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

img = cv.imread(IMG_PATH, 1)
resized = rescaleFrame(img, scale=0.5)   #! scale: 0.5 = half size, 2.0 = double size
cv.imshow('Rescaled 0.5x', resized)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 4. Resize to a HARDCODED target size
# ============================================================================
img = cv.imread(IMG_PATH, 1)
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)   #! (width, height) target
cv.imshow('Resized 500x500', resized)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 5. Change webcam capture resolution
# ============================================================================
capture = cv.VideoCapture(0)                  #! 0 = default webcam
capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)    #! target width
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)    #! target height

while True:
    isTrue, frame = capture.read()
    cv.imshow('Webcam', frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()


# ============================================================================
# 6. Draw shapes & text on a blank canvas
# ============================================================================
blank = np.zeros((500, 500, 3), dtype='uint8')   #! canvas size: (height, width, channels)

blank[:] = 0, 255, 0   #! fill color (B, G, R) -- this is pure green
cv.imshow('Painted Canvas', blank)

cv.rectangle(blank, (0, 0), (250, 250), (0, 250, 0), thickness=2)   #! pt1, pt2, color, thickness (-1/cv.FILLED = solid)
cv.imshow('Rectangle', blank)

cv.circle(blank, (250, 250), 40, (0, 250, 0), thickness=-1)   #! center, radius, color, thickness
cv.imshow('Circle', blank)

cv.line(blank, (0, 0), (300, 400), (255, 250, 255), thickness=3)   #! pt1, pt2, color, thickness
cv.imshow('Line', blank)

cv.putText(blank, 'hello', (255, 255), cv.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 0), 2)   #! text, position, fontScale, color, thickness
cv.imshow('Text', blank)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 7. Crop (array slicing)
# ============================================================================
img = cv.imread(IMG_PATH, 1)
cropped = img[50:200, 200:400]   #! [y1:y2, x1:x2] -- the rows/cols range to KEEP
cv.imshow('Cropped', cropped)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 8. Translate (shift up/down/left/right)
# ============================================================================
def translate(img, x, y):
    transMat = np.float32([[1, 0, x], [0, 1, y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

img = cv.imread(IMG_PATH, 1)
translated = translate(img, 100, 100)   #! x, y shift in pixels (+x = right, +y = down)
cv.imshow('Translated', translated)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 9. Rotate
# ============================================================================
def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]
    if rotPoint is None:
        rotPoint = (width // 2, height // 2)   # default: rotate around center
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)
    return cv.warpAffine(img, rotMat, dimensions)

img = cv.imread(IMG_PATH, 1)
rotated = rotate(img, 45)   #! angle in degrees (counter-clockwise)
cv.imshow('Rotated', rotated)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 10. Flip
# ============================================================================
img = cv.imread(IMG_PATH, 1)
flipped = cv.flip(img, 0)   #! flipCode: 0 = vertical, 1 = horizontal, -1 = both
cv.imshow('Flipped', flipped)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 11. Grayscale
# ============================================================================
img = cv.imread(IMG_PATH, 1)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)   #! conversion code: BGR2GRAY, BGR2HSV, BGR2RGB, etc.
cv.imshow('Grayscale', gray)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 12. Blur
# ============================================================================
img = cv.imread(IMG_PATH, 1)
blur = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT)   #! kernel size -- both numbers must be ODD, bigger = blurrier
cv.imshow('Gaussian Blur', blur)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 13. Canny edge detection
# ============================================================================
img = cv.imread(IMG_PATH, 1)
canny = cv.Canny(img, 125, 175)   #! threshold1, threshold2 -- lower = more (fainter) edges detected
cv.imshow('Canny Edges', canny)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 14. Threshold (binarize)
# ============================================================================
img = cv.imread(IMG_PATH, 1)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)   #! thresh cutoff (0-255), type (THRESH_BINARY/_INV/TRUNC/...)
cv.imshow('Threshold', thresh)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 15. Dilate / Erode (thicken / thin edges)
# ============================================================================
img = cv.imread(IMG_PATH, 1)
canny = cv.Canny(img, 125, 175)

dilated = cv.dilate(canny, (3, 3), iterations=1)   #! kernel size, iterations -- more iterations = thicker
cv.imshow('Dilated', dilated)

eroded = cv.erode(dilated, (3, 3), iterations=1)   #! same kernel as dilate -- more iterations = thinner
cv.imshow('Eroded', eroded)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 16. Find & draw contours (full pipeline)
# ============================================================================
img = cv.imread(IMG_PATH, 1)
canny = cv.Canny(img, 125, 175)   #! threshold1, threshold2 -- controls how many shapes get found

contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)   #! mode (RETR_LIST/EXTERNAL/TREE), method (CHAIN_APPROX_NONE/SIMPLE)
print(f'{len(contours)} contour(s) found')

blank = np.zeros(img.shape, dtype='uint8')   # 3-channel canvas (needed for color drawing)
cv.drawContours(blank, contours, -1, (0, 0, 255), 2)   #! contourIdx (-1 = all), color (B,G,R), thickness
cv.imshow('Contours Drawn', blank)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# 17. COMBINED PIPELINE -- resize -> grayscale -> blur -> canny -> contours
# ============================================================================
# This is closer to a "production" flow: every step feeds the next, and each
# stage exists to make the NEXT stage's job easier/cheaper:
#   resize    -> smaller image = every later step runs faster
#   grayscale -> contours/edges don't need color, 1 channel = 1/3 the data
#   blur      -> removes small noise so Canny doesn't pick up tiny fake edges
#   canny     -> turns the cleaned-up image into edge pixels
#   contours  -> groups those edge pixels into shapes you can loop over

img = cv.imread(IMG_PATH, 1)

# Step 1: resize down first -- everything below is now cheaper to compute
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)   #! target (width, height)
cv.imshow('1. Resized', resized)

# Step 2: grayscale -- drop color info we don't need for shape detection
gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
cv.imshow('2. Grayscale', gray)

# Step 3: blur -- smooth out small noise/texture before edge detection
blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)   #! kernel size (odd numbers, bigger = more smoothing)
cv.imshow('3. Blurred', blur)

# Step 4: canny -- find edges in the cleaned-up image
canny = cv.Canny(blur, 125, 175)   #! threshold1, threshold2 -- tune based on Step 3 output
cv.imshow('4. Canny Edges', canny)

# Step 5: contours -- connect those edges into shapes
contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)   #! mode, method
print(f'{len(contours)} contour(s) found')

# Step 6: draw the result back onto a copy of the resized image (in color),
# so you can see the detected shapes overlaid on the real picture
output = resized.copy()
cv.drawContours(output, contours, -1, (0, 255, 0), 2)   #! contourIdx (-1 = all), color (B,G,R), thickness
cv.imshow('5. Contours on Original', output)

cv.waitKey(0)
cv.destroyAllWindows()
