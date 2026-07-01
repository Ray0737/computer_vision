import cv2 as cv
import numpy as np

# 1. Load the image and verify it exists
# Note: Fixed path string to use forward slashes to avoid escape character bugs
canvas = cv.imread('Code - Computer Vision/img.jpg', 1)

if canvas is None:
    print("Error: Could not open or find the image. Check the file path!")
    exit()

t = 'Click and Drag to Draw'

# State variables to track mouse holding and previous coordinates
drawing = False 
ix, iy = -1, -1

# 2. Define the callback function
def on_mouse(event, x, y, flags, param):
    global ix, iy, drawing, canvas

    # Check condition: Did the user press the left mouse button down?
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y  # Save the starting point of the line
        
        # Optional: draw a small dot where they first clicked
        cv.circle(canvas, (x, y), 2, (0, 255, 0), -1)
        cv.imshow(t, canvas)

    # Check condition: Is the mouse moving while the button is held down?
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            # Draw a line from the last saved position to the current mouse position
            cv.line(canvas, (ix, iy), (x, y), (0, 255, 0), thickness=3)
            ix, iy = x, y  # Update the "last position" to the current position
            cv.imshow(t, canvas)

    # Check condition: Did the user release the left mouse button?
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        # Draw the final line segment to the release point
        cv.line(canvas, (ix, iy), (x, y), (0, 255, 0), thickness=3)
        cv.imshow(t, canvas)

# 3. Setup the window and event listener
cv.namedWindow(t)                               
cv.imshow(t, canvas)                      
cv.setMouseCallback(t, on_mouse)             

print("Click and drag to sketch. Press any key to close.")
cv.waitKey(0)                                   
cv.destroyAllWindows()