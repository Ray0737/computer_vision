import cv2
import numpy as np

# 1. Create a blank white canvas (1024 x 1024, 3 channels)
canvas = np.ones((1024, 1024, 3), dtype=np.uint8) * 255

# 2. Define colors (BGR format)
BLACK = (0, 0, 0)
RED = (0, 0, 255)       # For the river markers if needed, or we use BLUE for water
BLUE = (235, 130, 0)    # A nice river blue
LINE_THICKNESS = 4

# --- COORDINATES & DRAWING ---

# A. Mountains (Background - drawn first)
# Mountain 1 (Left)
mtn1_pts = np.array([[105, 470], [270, 75], [370, 550]], dtype=np.int32)
cv2.polylines(canvas, [mtn1_pts], isClosed=False, color=BLACK, thickness=LINE_THICKNESS)

# Mountain 2 (Right)
mtn2_pts = np.array([[320, 435], [635, 140], [750, 700]], dtype=np.int32)
cv2.polylines(canvas, [mtn2_pts], isClosed=False, color=BLACK, thickness=LINE_THICKNESS)


# B. Diagonal River (Midground - Polylines/fillPoly where you highlighted red)
# Defining the top and bottom banks to fill the river with blue
river_pts = np.array([
    [600, 570],   # Top bank start
    [980, 800],   # Top bank end
    [1024, 825],  # Corner transition
    [1024, 960],  # Edge transition
    [870, 960],   # Bottom bank end
    [515, 620]    # Bottom bank start
], dtype=np.int32)

# Fill the river area with blue, then draw the red border lines as requested
cv2.fillPoly(canvas, [river_pts], color=BLUE)
cv2.polylines(canvas, [np.array([[600, 570], [1024, 825]], dtype=np.int32)], isClosed=False, color=RED, thickness=LINE_THICKNESS)
cv2.polylines(canvas, [np.array([[515, 620], [870, 960]], dtype=np.int32)], isClosed=False, color=RED, thickness=LINE_THICKNESS)


# C. Floating Box / Cloud (Top Right)
# cv2.rectangle format: (image, (x1, y1), (x2, y2), color, thickness)
cv2.rectangle(canvas, (720, 100), (820, 180), BLACK, thickness=LINE_THICKNESS)


# D. House Structure (Foreground - drawn over background)
# 1. House Roof
roof_pts = np.array([[180, 650], [390, 430], [730, 650]], dtype=np.int32)
cv2.fillPoly(canvas, [roof_pts], color=(240, 240, 240)) # Light fill so background lines don't bleed through
cv2.polylines(canvas, [roof_pts], isClosed=True, color=BLACK, thickness=LINE_THICKNESS)

# 2. Main House Body Box
cv2.rectangle(canvas, (180, 650), (730, 910), BLACK, thickness=LINE_THICKNESS)

# 3. Doors (Left and Right)
cv2.rectangle(canvas, (215, 700), (255, 870), BLACK, thickness=LINE_THICKNESS) # Door 1
cv2.rectangle(canvas, (655, 700), (695, 870), BLACK, thickness=LINE_THICKNESS) # Door 2

# 4. Windows (3 Middle Windows)
cv2.rectangle(canvas, (315, 740), (385, 790), BLACK, thickness=LINE_THICKNESS) # Window 1
cv2.rectangle(canvas, (425, 740), (485, 790), BLACK, thickness=LINE_THICKNESS) # Window 2
cv2.rectangle(canvas, (525, 740), (595, 790), BLACK, thickness=LINE_THICKNESS) # Window 3


# 3. Save and display the final image
cv2.imwrite('generated_scene.png', canvas)
cv2.imshow('Canvas Map', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()