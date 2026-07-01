import cv2 as cv
import numpy as np

# 1. Load the image and verify it exists
canvas = cv.imread('Code - Computer Vision/test2.png', 1)
t = 'Click to draw'

# 2. Define the callback function
def on_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        global initx, inity, drawing, canvas
        # Left button pressed
        # cv.putText(canvas,f'({x}, {y})',(x,y),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        initx, inity = x, y  # Save the initial click position
        cv.circle(canvas, (x, y), 6, (0, 255, 0), thickness=-1)
        cv.imshow(t, canvas)                    # Redraw with the new dot
        cv.waitKey(1)                           # Force GUI refresh
    elif event == cv.EVENT_MOUSEMOVE:
        currentx, currenty = x, y
        cv.line(canvas, (initx, inity), (currentx, currenty), (0, 255, 0), thickness=2)
        initx, inity = currentx, currenty
        cv.imshow(t, canvas)                    # Redraw with the new line
    elif event == cv.EVENT_LBUTTONUP:
        # Left button released
        cv.line(canvas, (initx, inity), (x, y), (0, 255, 0), thickness=2)
        cv.imshow(t, canvas)                    # Redraw with the final line
# 3. Setup the window and event listener
cv.namedWindow(t)                               # Explicitly create named window
cv.imshow(t, canvas)                      
cv.setMouseCallback(t, on_mouse)             
cv.waitKey(0)                                   
cv.destroyAllWindows()