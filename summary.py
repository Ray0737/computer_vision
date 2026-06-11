"""
============================================================================
 OpenCV (cv2) SUMMARY / CHEAT SHEET
============================================================================
Reorganized + heavily commented version of cv.py.

Grouping in this version:
  1. Setup & Paths
  2. Reading & Displaying Images
  3. Reading & Displaying Video
  4. Resizing / Rescaling Frames (for video / live use)
  5. Changing Capture Resolution
  6. Drawing Shapes & Text
  7. SIMPLE CONTROLS  -- resize, crop, translate, rotate, flip
                         (basic one-shot transforms on a single image)
  8. EDGE DETECTION + CONTOURS -- the full "vision pipeline":
                         grayscale -> blur -> canny/threshold -> dilate/erode
                         -> findContours -> drawContours

This file is meant to be READ section by section, not run top to bottom --
several sections call cv.imshow() + cv.waitKey(0), which BLOCKS until you
press a key / close the window. Every cv.imshow() title below has been
renamed to describe WHAT THAT STEP DID, so the popup windows are
self-explanatory.
============================================================================
"""

import cv2 as cv
import numpy as np

# Paths used throughout this file (this script lives in "Code - Computer Vision")
IMG_PATH = 'img.jpg'
VIDEO_PATH = 'Sequence 01.mp4'


# ============================================================================
# SECTION 2: READING & DISPLAYING IMAGES
# ============================================================================
#~ cv.imread(path, flag)
#   path : string path to the image file (relative to wherever you RUN the
#          script from)
#   flag : controls HOW the file is loaded into the array
#       1  -> cv.IMREAD_COLOR     : load as 3-channel color, in BGR order
#                                    (NOT RGB! red and blue channels are swapped)
#       0  -> cv.IMREAD_GRAYSCALE : load as a single-channel grayscale image
#       -1 -> cv.IMREAD_UNCHANGED : load exactly as stored, including the
#                                    alpha (transparency) channel if present
#
#~ cv.imshow(window_name, img)
#   window_name : string title shown on the popup window's title bar.
#                  Re-using the same name updates that window in place.
#   img         : the NumPy array (image) to display
#
#~ cv.waitKey(delay)
#   delay = 0   -> wait FOREVER until any key is pressed (returns key code)
#   delay = N   -> wait up to N milliseconds, then continue automatically
#   The return value is an int; mask with `& 0xFF` before comparing to
#   `ord('x')` because some platforms return extra bits in higher positions.
#
#~ cv.destroyAllWindows()
#   Closes every OpenCV window. MUST be called with parentheses `()` to
#   actually execute -- writing `cv.destroyAllWindows` (no parens) just
#   references the function and does nothing.

img = cv.imread(IMG_PATH, 1)        # 1 = color (BGR)
cv.imshow('Original Image', img)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# SECTION 3: READING & DISPLAYING VIDEO
# ============================================================================
#~ cv.VideoCapture(source)
#   source : EITHER a string path to a video file, OR an integer camera
#            index (0 = default webcam, 1 = next camera, etc.)
#
#~ capture.read()
#   Grabs the next frame. Returns a tuple (isTrue, frame):
#       isTrue -> bool, True if a frame was successfully grabbed,
#                 False once the video ends (or the source is invalid)
#       frame  -> the frame as a NumPy array, same shape/format as an image
#
#~ capture.release()
#   Frees the file/camera handle. Always call this when you're done so
#   other programs (or a later cv.VideoCapture call) can use the device.
#
# COMMON ERROR: "error -215:Assertion failed ... !_src.empty()"
#   Almost always means the path passed to VideoCapture()/imread() does
#   NOT exist, so OpenCV got an empty/None frame and choked on it.

capture = cv.VideoCapture(VIDEO_PATH)

while True:
    isTrue, frame = capture.read()         # grab next frame
    if not isTrue:                         # video ended / read failed -> stop
        break

    cv.imshow('Video Playback', frame)

    # cv.waitKey(20)              -> wait 20ms between frames (~50 fps)
    # & 0xFF                      -> mask to the lowest 8 bits (cross-platform safety)
    # == ord('d')                 -> ord() converts 'd' to its ASCII code (100)
    if cv.waitKey(20) & 0xFF == ord('d'):  # press 'd' to quit early
        break

capture.release()
cv.destroyAllWindows()


# ============================================================================
# SECTION 4: RESIZING / RESCALING FRAMES (images AND video)
# ============================================================================
# IMPORTANT -- AXIS ORDER GOTCHA:
#   img.shape  -> (height, width, channels)   <- rows first, then columns
#   cv.resize(src, dsize, ...) wants dsize = (width, height)  <- REVERSED!
# Mixing these two orders up is one of THE most common OpenCV bugs.
#
# There are two common ways to resize:
#
#   METHOD 1 -- SCALE FACTOR
#     Multiply the current width/height by a ratio (e.g. 0.5 = half size,
#     2.0 = double size). Aspect ratio is preserved automatically. Great
#     for shrinking video frames so they fit on screen / process faster.
#
#   METHOD 2 -- HARDCODED TARGET DIMENSIONS
#     Tell cv.resize() the exact (width, height) you want. Simple, but the
#     image will look stretched/squashed if that ratio doesn't match the
#     original. (Used in Section 7, "Simple Controls".)

# --- METHOD 1: scale factor ---
def rescaleFrame(frame, scale):
    """
    Return a copy of `frame` resized by `scale`.
    scale = 0.5 -> half size, scale = 2.0 -> double size.
    Works for images AND individual video frames (both are just arrays).
    """
    # NEW SYNTAX: frame.shape returns a tuple (height, width, channels).
    # frame.shape[1] -> index 1 of that tuple -> WIDTH
    # frame.shape[0] -> index 0 of that tuple -> HEIGHT
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)          # cv.resize wants (width, height)

    #~ cv.resize(src, dsize, interpolation)
    #   src           : the image/frame to resize
    #   dsize         : target size as (width, height)
    #   interpolation : algorithm used to fill in / drop pixels (Section 9 cheat sheet)
    #                    INTER_AREA is the recommended choice for SHRINKING
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


# --- Example: apply Method 1 to a video ---
capture = cv.VideoCapture(VIDEO_PATH)
while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break
    frame_resized = rescaleFrame(frame, scale=0.5)
    cv.imshow('Video Playback (Original)', frame)
    cv.imshow('Video Playback (Rescaled 0.5x)', frame_resized)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
capture.release()
cv.destroyAllWindows()

# --- Example: apply Method 1 to a still image ---
img = cv.imread(IMG_PATH, 1)
resized_img = rescaleFrame(img, scale=0.5)
cv.imshow('Image Rescaled 0.5x', resized_img)
cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# SECTION 5: CHANGING CAPTURE RESOLUTION (live video / webcam)
# ============================================================================
# rescaleFrame() resizes a frame AFTER it has been captured.
# capture.set(...) instead changes the resolution the CAMERA captures at.
# Works reliably on live webcams; video FILES often ignore it.
#
#~ capture.set(propId, value) / capture.get(propId)
#   propId : an integer ID (or the equivalent cv.CAP_PROP_* constant --
#            they are interchangeable, the constant is just a friendly name)
#   value  : the value to set that property to
#
# --- Capture property cheat sheet (most useful ones) ---
#   ID | Constant                     | What it controls
#   ---|------------------------------|----------------------------------
#   3  | cv.CAP_PROP_FRAME_WIDTH      | Frame width
#   4  | cv.CAP_PROP_FRAME_HEIGHT     | Frame height
#   5  | cv.CAP_PROP_FPS              | Frame rate (frames per second)
#   7  | cv.CAP_PROP_FRAME_COUNT      | Total frame count (video files only)
#   10 | cv.CAP_PROP_BRIGHTNESS       | Camera brightness
#   11 | cv.CAP_PROP_CONTRAST         | Camera contrast
#   12 | cv.CAP_PROP_SATURATION       | Camera saturation
#   15 | cv.CAP_PROP_EXPOSURE         | Camera exposure (often negative)
#   39 | cv.CAP_PROP_FOCUS            | Camera hardware focus
#   40 | cv.CAP_PROP_AUTO_EXPOSURE    | Auto exposure (0 = manual, 1 = auto)

def changeRes(capture, width, height):
    """Set a LIVE VideoCapture's resolution (id 3 = width, id 4 = height)."""
    capture.set(cv.CAP_PROP_FRAME_WIDTH, width)    # same as capture.set(3, width)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)  # same as capture.set(4, height)

# Example (uncomment if a webcam is connected):
# capture = cv.VideoCapture(0)
# changeRes(capture, 1280, 720)


# ============================================================================
# SECTION 6: DRAWING SHAPES & WRITING TEXT
# ============================================================================
# np.zeros(shape, dtype) -- creates a blank canvas filled with 0s (black).
#
# NEW SYNTAX -- shape vs shape[:2]:
#   img.shape     -> (height, width, channels)  e.g. (500, 500, 3)
#   img.shape[:2] -> SLICE of the tuple, keeping only index 0 and 1
#                    -> (height, width)  e.g. (500, 500)   (channels dropped)
#   `[:2]` means "everything from the start UP TO (not including) index 2".
#
# QUICK SUMMARY (when to use which):
#   np.zeros(img.shape,      dtype='uint8') -> 3-channel BLACK image
#                                               (for color drawing/painting)
#   np.zeros(img.shape[:2],  dtype='uint8') -> 1-channel BLACK image
#                                               (for masks / stencils / contours)
#   np.zeros((500, 500, 3),  dtype='uint8') -> manual 500x500 3-channel canvas
blank = np.zeros((500, 500, 3), dtype='uint8')   # 500x500 black BGR canvas
cv.imshow('Blank Canvas', blank)

# blank[:] = (B, G, R)  -- slice-assign paints EVERY pixel that color.
# Remember: OpenCV channel order is BLUE, GREEN, RED (not RGB!)
blank[:] = 0, 255, 0   # pure green
cv.imshow('Canvas Painted Green', blank)

#~ cv.rectangle(img, pt1, pt2, color, thickness)
#   pt1       : (x, y) of the TOP-LEFT corner
#   pt2       : (x, y) of the BOTTOM-RIGHT corner
#   color     : (B, G, R) tuple
#   thickness : outline width in pixels, OR cv.FILLED (== -1) to fill solid
cv.rectangle(blank, (0, 0), (250, 250), (0, 250, 0), thickness=2)              # 2px outline
cv.rectangle(blank, (0, 0), (250, 250), (0, 250, 0), thickness=cv.FILLED)      # filled
# Fill just the top-left quadrant of the canvas using its own dimensions:
cv.rectangle(blank, (0, 0), (blank.shape[1] // 2, blank.shape[0] // 2), (0, 250, 0), thickness=cv.FILLED)
cv.imshow('Rectangle Drawn', blank)

#~ cv.circle(img, center, radius, color, thickness)
#   center    : (x, y) of the circle's center point
#   radius    : radius in pixels (a single int)
#   thickness : outline width, or -1 / cv.FILLED to fill
cv.circle(blank, (250, 250), 40, (0, 250, 0), thickness=-1)
cv.imshow('Circle Drawn', blank)

#~ cv.line(img, pt1, pt2, color, thickness)
#   pt1, pt2 : (x, y) endpoints of the line
cv.line(blank, (0, 0), (blank.shape[1] // 2, blank.shape[0] // 2), (255, 250, 255), thickness=3)
cv.line(blank, (0, 0), (300, 400), (255, 250, 255), thickness=3)
cv.imshow('Line Drawn', blank)

#~ cv.putText(img, text, org, fontFace, fontScale, color, thickness)
#   text      : the string to draw
#   org       : (x, y) of the BOTTOM-LEFT corner of the text
#   fontFace  : a font constant, e.g. cv.FONT_HERSHEY_COMPLEX
#   fontScale : size multiplier (1.0 = default size)
cv.putText(blank, 'hello', (255, 255), cv.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 0), thickness=2)
cv.imshow('Text Drawn', blank)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# SECTION 7: SIMPLE CONTROLS -- Resize, Crop, Translate, Rotate, Flip
# ============================================================================
# These are the basic "one-shot" transforms you apply to a single image --
# as opposed to Section 4 (rescaling, mainly for video/live frames).

img = cv.imread(IMG_PATH, 1)

# --- Resize (hardcoded target dimensions) ---
#~ cv.resize(src, dsize, interpolation)
#   dsize         : (width, height) -- REMEMBER: opposite order from .shape!
#   interpolation : algorithm used when the size changes (cheat sheet below)
#
#   Goal                      | Flag                | Notes
#   --------------------------|---------------------|----------------------------
#   Shrinking                 | cv.INTER_AREA       | Avoids jagged edges/moire
#   Enlarging (best quality)  | cv.INTER_CUBIC      | Sharp & smooth, slower
#   Enlarging (fast)          | cv.INTER_LINEAR     | Default, good speed/quality
#   Pixel art / AI masks      | cv.INTER_NEAREST    | No blur, crisp blocky pixels
#   Max quality zoom          | cv.INTER_LANCZOS4   | 8x8 neighborhood, slowest
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)
cv.imshow('Resized (500x500, INTER_AREA)', resized)

# --- Crop ---
# Images are just NumPy arrays, so cropping is plain ARRAY SLICING:
#
#   cropped = img[y1:y2, x1:x2]
#       - 1st range (y1:y2) -> ROWS    -> the VERTICAL   (y) range
#       - 2nd range (x1:x2) -> COLUMNS -> the HORIZONTAL (x) range
#       - (0, 0) is the TOP-LEFT corner of the image
#
# img[50:200, 200:400] keeps rows 50-200 and columns 200-400
# -> a region that is 150px tall and 200px wide.
cropped = img[50:200, 200:400]
cv.imshow('Cropped Region', cropped)

# --- Translate (shift) ---
#~ cv.warpAffine(src, M, dsize)
# Applies a 2x3 "affine transformation matrix" M to every pixel coordinate.
#   src   : input image
#   M     : 2x3 transformation matrix (np.float32)
#   dsize : output size as (width, height)
def translate(img, x, y):
    """
    Shift `img` by (x, y) pixels.
    x > 0 -> right, x < 0 -> left
    y > 0 -> down,  y < 0 -> up
    """
    # [[1, 0, x],    -> new_x = 1*old_x + 0*old_y + x
    #  [0, 1, y]]    -> new_y = 0*old_x + 1*old_y + y
    # i.e. just adds (x, y) to every coordinate -- a pure shift.
    transMat = np.float32([[1, 0, x], [0, 1, y]])  # warpAffine needs float32
    dimensions = (img.shape[1], img.shape[0])      # (width, height)
    return cv.warpAffine(img, transMat, dimensions)

translated = translate(img, 100, 100)  # right 100px, down 100px
cv.imshow('Translated Image', translated)

# --- Rotate ---
def rotate(img, angle, rotPoint=None):
    """
    Rotate `img` by `angle` degrees (counter-clockwise for positive values)
    around `rotPoint`. If rotPoint is None, rotates around the image center.
    """
    # NEW SYNTAX: img.shape[:2] -> slice of the shape tuple -> (height, width)
    # (drops the channel count, since we don't need it for rotation math)
    (height, width) = img.shape[:2]

    if rotPoint is None:              # default arg -> caller can omit it
        rotPoint = (width // 2, height // 2)  # center of the image

    #~ cv.getRotationMatrix2D(center, angle, scale)
    #   center : (x, y) pivot point to rotate around
    #   angle  : degrees, counter-clockwise for positive values
    #   scale  : 1.0 = no extra resizing, 0.5 = also shrink to half, etc.
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)
    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, 45)  # rotate 45 degrees around the center
cv.imshow('Rotated 45 Degrees', rotated)

# --- Flip ---
#~ cv.flip(src, flipCode)
#   flipCode = 0  -> flip VERTICALLY   (upside down)
#   flipCode = 1  -> flip HORIZONTALLY (mirror left-right)
#   flipCode = -1 -> flip BOTH axes    (180 degree mirror)
flip = cv.flip(img, 0)
cv.imshow('Flipped Vertically', flip)

cv.waitKey(0)
cv.destroyAllWindows()


# ============================================================================
# SECTION 8: EDGE DETECTION + CONTOURS -- the "Vision Pipeline"
# ============================================================================
# === THE VISION PIPELINE LAYER ===
# 1. Grayscale + Blur  -> clean, single-channel input (less noise)
# 2. cv.threshold()    -> BINARIZES: converts to clean, solid black & white blocks
#    cv.Canny()        -> PLOTS EDGES: scans and highlights individual boundary pixels
# 3. cv.dilate/erode   -> thicken/thin those edges
# 4. cv.findContours() -> CONNECTS THE DOTS: links edge/boundary pixels into an
#                         organized list of shapes (contours)
# 5. cv.drawContours() -> draw the result

img = cv.imread(IMG_PATH, 1)

# --- Step 1: Grayscale ---
#~ cv.cvtColor(src, code)
#   code : a cv.COLOR_<FROM>2<TO> constant describing the conversion
#       cv.COLOR_BGR2GRAY -> BGR color  -> single-channel grayscale
#       cv.COLOR_BGR2RGB  -> BGR color  -> RGB (needed before matplotlib)
#       cv.COLOR_BGR2HSV  -> BGR color  -> Hue/Saturation/Value
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale', gray)

# --- Step 1b: Blur ---
#~ cv.GaussianBlur(src, ksize, sigmaX)
#   ksize  : kernel ("window") size as (width, height). BOTH numbers must
#            be POSITIVE and ODD, e.g. (3,3), (5,5), (7,7). Bigger = blurrier.
#   sigmaX : standard deviation of the gaussian curve in the X direction.
#            cv.BORDER_DEFAULT here is just a numeric placeholder that lets
#            OpenCV auto-compute sigma from ksize.
# Blurring removes small noise that would otherwise create lots of tiny,
# useless edges/contours.
blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)
cv.imshow('Gaussian Blur', blur)

# --- Step 2a: Canny edge detection ---
#~ cv.Canny(src, threshold1, threshold2)
#   threshold1, threshold2 : the LOW and HIGH gradient-strength thresholds.
#       - A pixel with edge-strength ABOVE threshold2 is DEFINITELY an edge.
#       - A pixel BELOW threshold1 is DEFINITELY NOT an edge.
#       - Anything in between is kept ONLY if connected to a strong edge.
#       Lower the thresholds to detect MORE (fainter) edges; raise them to
#       detect FEWER, only-strong edges.
#   Returns a binary (black/white) image: white = edge pixel.
canny = cv.Canny(blur, 125, 175)
cv.imshow('Canny Edge Detection', canny)

# --- Step 2b: Threshold (alternative / complementary to Canny) ---
#~ cv.threshold(src, thresh, maxval, type)
#   src    : a SINGLE-CHANNEL (grayscale) image
#   thresh : the cutoff value (0-255) -- "what to put here" depends on how
#            bright/dark your subject is vs. the background. Common starting
#            point: 125-150, then tweak.
#   maxval : the value given to pixels that PASS the test (almost always 255)
#   type   : the comparison rule applied to each pixel:
#       cv.THRESH_BINARY      -> pixel > thresh ? maxval : 0
#       cv.THRESH_BINARY_INV  -> pixel > thresh ? 0 : maxval        (inverted)
#       cv.THRESH_TRUNC       -> pixel > thresh ? thresh : pixel    (clip/cap)
#       cv.THRESH_TOZERO      -> pixel > thresh ? pixel : 0
#       cv.THRESH_TOZERO_INV  -> pixel > thresh ? 0 : pixel
#   Returns a TUPLE: (retval, dst)
#       retval -> the threshold value that was actually used
#       dst    -> the resulting binary image
ret, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
cv.imshow('Threshold (Binary)', thresh)

# --- Step 3: Dilate / Erode (sharpen up the Canny edges) ---
#~ cv.dilate(src, kernel, iterations)
#   kernel     : shape/size of the neighborhood used to grow white regions,
#                e.g. (3,3) -- a 3x3 block
#   iterations : how many times to repeat the operation (more = thicker)
dilated = cv.dilate(canny, (3, 3), iterations=1)
cv.imshow('Dilated Edges', dilated)

#~ cv.erode(src, kernel, iterations)
#   The opposite of dilate -- shrinks white regions. Running erode after
#   dilate with the SAME kernel can "undo" some of the thickening, giving
#   thinner, more precise edge lines than the raw Canny output.
eroded = cv.erode(dilated, (3, 3), iterations=1)
cv.imshow('Eroded Edges', eroded)

# --- Step 4: Find contours ---
# A "contour" is the OUTLINE / boundary curve of a shape -- a list of (x, y)
# points tracing where a region of similar color/intensity meets a
# different one. Contours are NOT the same as edges: edges (Canny) are
# individual lines; contours are CLOSED SHAPES built by connecting those
# edges/boundaries. (its a list btw)
#
#~ cv.findContours(image, mode, method)
#   image  : a binary/edge image (single channel) -- here, canny or thresh
#   mode   : how contours are organized / which ones are returned
#       cv.RETR_LIST     -> ALL contours, no parent/child relationships
#       cv.RETR_EXTERNAL -> only the OUTERMOST contour of each shape
#       cv.RETR_TREE     -> ALL contours, with full nesting hierarchy
#       cv.RETR_CCOMP    -> all contours organized into a 2-level hierarchy
#   method : how much detail to keep PER contour
#       cv.CHAIN_APPROX_NONE   -> store EVERY point along the boundary
#                                 (most accurate, most memory)
#       cv.CHAIN_APPROX_SIMPLE -> compress straight line segments down to
#                                 just their START and END points (saves
#                                 memory, usually good enough)
#   Returns: (contours, hierarchy)
#       contours  : a tuple of arrays; each array is the (x, y) points for
#                   ONE contour (one shape found)
#       hierarchy : describes how contours are nested inside each other
#                   (only meaningful with RETR_TREE / RETR_CCOMP)
#
# You can find contours from EITHER `canny` or `thresh` -- canny is more
# common for general edge-based shapes.
contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} contour(s) found')

# --- Step 5: Draw contours ---
#~ cv.drawContours(image, contours, contourIdx, color, thickness)
#   image      : image to draw ON, modified IN PLACE -- usually a blank
#                canvas (np.zeros) or a copy of the original (img.copy())
#   contours   : the list returned by cv.findContours
#   contourIdx : which contour to draw -- an index into `contours`,
#                or -1 to draw ALL of them
#   color      : (B, G, R)
#   thickness  : outline thickness in pixels, or cv.FILLED to fill the shape
#
# NOTE: arguments must be separated by commas: (-1, (0, 0, 255), 2)
#       writing -1(0, 0, 255) -- with no comma -- is a syntax error, since
#       Python would try to "call" the int -1 like a function.
#
# Drawing in COLOR (0, 0, 255) needs a 3-CHANNEL canvas, so use
# np.zeros(img.shape, ...) here -- NOT img.shape[:2] (that's the 1-channel
# "mask/stencil" version from the Quick Summary above, which can only hold
# a single intensity value per pixel, not a B/G/R color).
blank = np.zeros(img.shape, dtype='uint8')   # 3-channel canvas (for color drawing)
cv.drawContours(blank, contours, -1, (0, 0, 255), 2)
cv.imshow('Contours Drawn', blank)

cv.waitKey(0)
cv.destroyAllWindows()
