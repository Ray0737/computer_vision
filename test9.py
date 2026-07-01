import cv2 as cv
import numpy as np

W = H = 1024

# ── Cloudy gray sky (gradient: slightly darker at top) ──
canvas = np.full((H, W, 3), (118, 118, 118), dtype='uint8')
for y in range(720):
    b = int(108 + (y / 720) * 20)
    canvas[y] = (b, b, b)

# ── Mountains (drawn first, behind everything) ──
M_COL  = (65, 65, 65)
M_EDGE = (45, 45, 45)
SNOW   = (185, 185, 185)

lm = np.array([[-50, 730], [205, 175], [540, 730]], np.int32)
cv.fillPoly(canvas, [lm], M_COL)
cv.polylines(canvas, [lm], True, M_EDGE, 2)


rm = np.array([[500, 730], [835, 155], [1100, 730]], np.int32)
cv.fillPoly(canvas, [rm], M_COL)
cv.polylines(canvas, [rm], True, M_EDGE, 2)
rs = np.array([[790, 213], [835, 155], [880, 213]], np.int32)


# ── Ground ──
cv.rectangle(canvas, (0, 720), (W, H), (50, 70, 40), cv.FILLED)


# ── River (full-width rectangle at the bottom) ──
cv.rectangle(canvas, (0, 740), (W, 870), (145, 118, 88), cv.FILLED)   # river body (steel blue-gray)
cv.rectangle(canvas, (0, 740), (W, 870), (100, 80, 60), 3)             # river border/banks
cv.line(canvas, (0, 768), (W, 768), (168, 142, 112), 2)                # ripple 1
cv.line(canvas, (0, 796), (W, 796), (168, 142, 112), 2)                # ripple 2
cv.line(canvas, (0, 824), (W, 824), (155, 130, 100), 1)                # ripple 3

# ── House body (pink, wide: 100–924) ──
HX1, HY1, HX2, HY2 = 100, 445, 924, 720
PINK = (170, 98, 228)
cv.rectangle(canvas, (HX1, HY1), (HX2, HY2), PINK, cv.FILLED)
cv.rectangle(canvas, (HX1, HY1), (HX2, HY2), (102, 48, 155), 3)

# ── Roof (purple triangle) ──
PURPLE = (155, 20, 138)
roof = np.array([[62, 452], [512, 185], [962, 452]], np.int32)
cv.fillPoly(canvas, [roof], PURPLE)
cv.polylines(canvas, [roof], True, (102, 8, 98), 3)


# ── 2 Doors (bottom section, y 590–720) ──
DOOR_C   = (115, 60, 170)
DOOR_OUT = (70, 30, 115)
HANDLE_C = (28, 172, 200)

for dx1, dx2 in [(292, 407), (617, 732)]:
    cv.rectangle(canvas, (dx1, 590), (dx2, 720), DOOR_C, cv.FILLED)
    cv.rectangle(canvas, (dx1, 590), (dx2, 720), DOOR_OUT, 2)
    mid_x = (dx1 + dx2) // 2
    cv.ellipse(canvas, (mid_x, 622), (40, 14), 0, 0, 360, (188, 215, 232), 2)
    hx = dx2 - 22 if dx1 < 512 else dx1 + 22
    cv.circle(canvas, (hx, 668), 8, HANDLE_C, cv.FILLED)

# ── 3 Windows (upper house, y 462–552) ──
WIN_G = (255, 255, 255)  # Changed glass color to pure white
WIN_F = (78, 40, 120)

for wx1, wx2 in [(132, 248), (462, 578), (792, 908)]:
    wy1, wy2 = 462, 552
    cv.rectangle(canvas, (wx1, wy1), (wx2, wy2), WIN_G, cv.FILLED)
    cv.rectangle(canvas, (wx1, wy1), (wx2, wy2), WIN_F, 3)
    # Simple setup: internal cross lines removed for a clean look

# ── Dark gray clouds ──
CLOUD_D = (46, 46, 46)
CLOUD_M = (68, 68, 68)

def draw_cloud(img, cx, cy, s=1.0, col=(46, 46, 46)):
    blobs = [(0, 0, 58, 33), (-48, -12, 44, 27), (48, -8, 50, 31),
             (-24, -30, 40, 24), (24, -23, 42, 26), (72, 7, 33, 22), (-72, 7, 34, 21)]
    for dx, dy, rx, ry in blobs:
        cv.ellipse(img, (int(cx + dx*s), int(cy + dy*s)),
                   (int(rx*s), int(ry*s)), 0, 0, 360, col, cv.FILLED)

draw_cloud(canvas,  130,  90, 1.3, CLOUD_D)
draw_cloud(canvas,  378,  68, 1.1, CLOUD_D)
draw_cloud(canvas,  630,  88, 1.2, CLOUD_M)
draw_cloud(canvas,  880, 110, 1.0, CLOUD_D)
draw_cloud(canvas,  248, 148, 0.85, CLOUD_M)
draw_cloud(canvas,  512, 125, 0.95, CLOUD_D)

np.random.seed()
for _ in range(1500):
    x = np.random.randint(-200, 1200)
    y = np.random.randint(-100, 1024)
    length = np.random.randint(15, 50)
    cv.line(canvas, (x, y), (x - int(length * 0.4), y + length), (180, 180, 180), 1)

cv.imshow('my house', canvas)
cv.waitKey(0)
cv.destroyAllWindows()