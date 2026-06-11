import cv2 as cv

img = cv.imread('Code - Computer Vision\img.jpg')
height, width, channels = img.shape

for i in range(height):
    for j in range(width):
        # i j Iteration | 0: B first index | 1: G second index | 2: R third index
        gray = 0.114 * img[i,j,0] + 0.587 * img[i,j,1] + 0.299 * img[i,j,2]
        if gray >= 128:
            img[i, j] = [255, 255, 255]
        else:
            img[i, j] = [0, 0, 0]

print(img)
cv.imshow('?', img)
cv.waitKey(0)
cv.destroyAllWindows()

