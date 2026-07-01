import cv2 as cv
import numpy as np
import random
import matplotlib.pyplot as plt

blank = np.zeros((1024,1024,3),dtype='uint8')
blank2 = np.full((1024,1024,3),(128,128,128),dtype='uint8')

cv.circle()
cv.rectangle(blank2,(1024*1//4,1024),(1024*3//4,1024//2),(255,255,255),thickness=2) # house
cv.rectangle(blank2,(500*3//5,500),(500*3//4,500*2//3),(255,255,255),thickness=2) # door
cv.ellipse(blank2,(340,370),(25,10),0,0,360,(255,255,255),thickness=2) # door window
cv.circle(blank2,(200,350),40,(255,255,255),thickness=cv.FILLED) # window
cv.circle(blank,(360,400),5,(255,255,255),thickness=cv.FILLED) # door handle
cv.line(blank2,(500*1//4,250),(250,100),(255,255,255),thickness=3)# roof 1
cv.line(blank2,(250,100),(500*3//4,250),(255,255,255),thickness=3) # roof 2
cv.putText(blank2,'my house',(100,50),cv.FONT_HERSHEY_COMPLEX,1.0,(255,255,255), thickness=2)
cv.imshow('rectangle',blank2)
cv.waitKey(0)
cv.destroyAllWindows()


