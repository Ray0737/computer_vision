import cv2 as cv
import numpy as np

blank = np.zeros((500,500),dtype='uint8') #blank canvas | 1 channel | 500x500 dimension
cv.imshow('blank',blank)

def get_triangle_points(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    length = np.hypot(dx, dy)
    if length < 5:
        return None

    # จุดกึ่งกลางของฐาน
    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2

    # เวกเตอร์ตั้งฉาก (หน่วย)
    px = -dy / length
    py = dx / length

    # ความสูงของสามเหลี่ยม (ปรับอัตราส่วนให้สวย)

    height = length * 0.65
    # จุดยอดที่ 3
    p3_x = int(mid_x + px * height)
    p3_y = int(mid_y + py * height)

    return np.array([p1, p2, (p3_x, p3_y)], dtype=np.int32)

cv.namedWindow('whatever')                               # Explicitly create named window                 
cv.setMouseCallback('whatever', get_triangle_points)             
cv.waitKey(0)                                   
cv.destroyAllWindows()