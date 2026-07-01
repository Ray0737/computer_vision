import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt

# Fixed path syntax (using r'' for raw string to avoid escape character issues)
img = cv.imread(r'Code - Computer Vision\Screenshot 2026-06-24 124535.png', 0)

# cv.threshold returns two values: retval and dst. 
# We use '_' to discard the threshold value and keep the image.
_, result = cv.threshold(img, 150, 255, cv.THRESH_BINARY)

cv.imshow("hehe", result) 
cv.waitKey(0)
cv.destroyAllWindows()