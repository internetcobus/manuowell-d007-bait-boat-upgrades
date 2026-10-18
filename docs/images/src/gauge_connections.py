# Draws gauge-connections.png: the LED strip, the driver board and the C3 Zero
# side by side, with every wire drawn between its holes.
#   python3 gauge_connections.py docs/images/gauge-connections.png
from PIL import Image, ImageDraw, ImageFont
import sys
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
B = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
P = 34
W, H = 1600, 1080
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
d.text((20, 12), 'How it all connects (everything seen from inside the boat)', fill='black', font=B(24))

def board(ox, oy, rows, title, sub):
    d.rectangle((ox - 5, oy - 4, ox + 6 * P + 5, oy + rows * P + 4), fill='#d9c08a', outline='#7a6236', width=2)
    d.text((ox - 5, oy - 64), title, fill='black', font=B(20))
    d.text((ox - 5, oy - 40), sub, fill='#444', font=F(14))
    for c in range(1, 7): d.text((ox + (c - 1) * P + P // 2 - 5, oy - 22), str(c), fill='#555', font=B(13))
    for r in range(rows):
        d.text((ox - 22, oy + r * P + P // 2 - 9), chr(65 + r), fill='#555', font=B(14))
        for c in range(6):
            x, y = ox + c * P + P // 2, oy + r * P + P // 2
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill='#c8a050', outline='#8a6a2a')
    return lambda h: (ox + (int(h[1:]) - 1) * P + P // 2, oy + (ord(h[0]) - 65) * P + P // 2)

def dot(p, col, r=9): d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=col, outline='black')
def wire(a, b, col, via=None, w=5):
    pts = [a] + (via or []) + [b]; d.line(pts, fill=col, width=w, joint='curve'); dot(a, col); dot(b, col)

# LED strip (back face), 16 rows: it sits UNDER the driver board
L = board(110, 150, 16, 'LED strip (under the driver)', 'back face, as seen from inside the boat')
for i, r in enumerate('ACEG'):
    x3, y = L(r + '1'); x4, _ = L(r + '2')
    col = '#e02020' if i == 0 else '#2a6fe0'
    d.ellipse(((x3 + x4) / 2 - 26, y - 26, (x3 + x4) / 2 + 26, y + 26), outline=col, width=3)
    d.line((L(r + '2'), L(r + '3')), fill='#9a9a9a', width=9)
d.line((L('A1'), L('G1')), fill='#e03030', width=7)
(gx, gy), (px, py) = L('G1'), L('P4')
d.line((gx, gy, gx, py - 18, px, py - 18, px, py), fill='#e03030', width=7)
JCOL = {1: '#e02020', 2: '#2a6fe0', 3: '#1a9a3a', 4: '#9a3ad0'}
for k, (a, b) in enumerate((('A3', 'B5'), ('C3', 'E5'), ('E3', 'H5'), ('G3', 'K5')), 1):
    (x1, y1), (x2, y2) = L(a), L(b)
    d.line((x1, y1, x1, (y1 + y2) / 2, x2, (y1 + y2) / 2, x2, y2), fill=JCOL[k], width=4)
    d.line((L(b), L(b[0] + '6')), fill='#9a9a9a', width=9)
    d.text((L('A1')[0] - 100, y1 - 9), 'LED %d' % k, fill=JCOL[k], font=B(13))
# driver board (parts side)
D = board(560, 150, 16, 'Driver board (on top)', 'parts side, as seen from inside the boat')
for k, (r0, r1, r2) in enumerate((('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I'), ('J', 'K', 'L')), 1):
    for a, b, t in ((r0 + '2', r0 + '5', '10k'), (r2 + '3', r2 + '6', '330')):
        (x1, y1), (x2, y2) = D(a), D(b)
        d.line((x1, y1, x2, y2), fill='#555', width=3)
        d.rounded_rectangle(((x1 + x2) / 2 - 26, y1 - 9, (x1 + x2) / 2 + 26, y1 + 9), 4, fill='#e8d3a9', outline='#333')
        d.text(((x1 + x2) / 2 - 14, y1 - 8), t, fill='#222', font=B(12))
    xe, y = D(r1 + '1'); xc, _ = D(r1 + '3')
    d.chord((xe - 14, y - 26, xc + 14, y + 16), 0, 180, fill='#222')
for a, b, t, f in (('N1', 'N4', '10k', '#e8d3a9'), ('O1', 'O3', '100n', '#e8a33a')):
    (x1, y1), (x2, y2) = D(a), D(b)
    d.line((x1, y1, x2, y2), fill='#555', width=3)
    d.rounded_rectangle(((x1 + x2) / 2 - 22, y1 - 9, (x1 + x2) / 2 + 22, y1 + 9), 4, fill=f, outline='#333')
    d.text(((x1 + x2) / 2 - 16, y1 - 8), t, fill='#222', font=B(12))

# C3 Zero (face-down: the printed labels face you)
cx, cy = 1180, 190
d.rounded_rectangle((cx, cy, cx + 230, cy + 400), 10, fill='#2a5fb0', outline='#123')
d.rectangle((cx + 85, cy - 26, cx + 145, cy), fill='#bbb', outline='#555'); d.text((cx + 92, cy - 22), 'USB-C', fill='black', font=F(12))
d.text((cx + 52, cy + 175), 'ESP32-C3\n   Zero\n(face-down)', fill='white', font=B(17))
right = ['5V', 'GND', '3V3', 'GP0', 'GP1', 'GP2', 'GP3', 'GP4', 'GP5']
left = ['GP21', 'GP20', 'GP19', 'GP18', 'GP10', 'GP9', 'GP8', 'GP7', 'GP6']
C3 = {}
for i, (l, r) in enumerate(zip(left, right)):
    y = cy + 30 + i * 43
    for x, n in ((cx + 18, l), (cx + 212, r)):
        d.rectangle((x - 9, y - 9, x + 9, y + 9), fill='#f2d23c', outline='#333'); C3[n] = (x, y)
    d.text((cx + 32, y - 8), l, fill='white', font=B(12)); d.text((cx + 198 - d.textlength(r, font=B(12)), y - 8), r, fill='white', font=B(12))
d.text((cx, cy + 410), 'labels as printed on its back', fill='#555', font=F(13))

# ---- pins: LED strip <-> driver board (same holes, boards stacked) ----
LEDC = {1: '#e02020', 2: '#2a6fe0', 3: '#1a9a3a', 4: '#9a3ad0'}
for h in ('B6', 'E6', 'H6', 'K6', 'P4'):
    a, b = L(h), D(h)
    for x in range(int(a[0]), int(b[0]), 16): d.line((x, a[1], x + 8, a[1]), fill='#b08a00', width=3)
    dot(a, '#f2d23c', 10); dot(b, '#f2d23c', 10)
    d.text((a[0] + 30, a[1] - 22), 'pin ' + h, fill='#8a6a00', font=B(12))
# ---- wires: driver board <-> C3 ----
for k, (s, n) in enumerate((('A6', 'GP4'), ('D6', 'GP5'), ('G6', 'GP6'), ('J6', 'GP7')), 1):
    a, b = D(s), C3[n]; xm = 820 + k * 26
    if n in ('GP6', 'GP7'):                       # left edge of the C3
        wire(a, b, LEDC[k], [(xm, a[1]), (xm, b[1])])
    else:                                         # right edge: round underneath
        yb = cy + 450 + k * 14; xr = cx + 250 + k * 14
        wire(a, b, LEDC[k], [(xm, a[1]), (xm, yb), (xr, yb), (xr, b[1])])
for k, (s, n, col) in enumerate((('O5', 'GP3', '#f0a000'), ('P5', '5V', '#ff7a00'), ('P2', 'GND', '#555')), 1):
    a, b = D(s), C3[n]; xm = 820 + (4 + k) * 26; xr = cx + 250 + (4 + k) * 14
    yb = cy + 450 + (4 + k) * 14
    wire(a, b, col, [(a[0], a[1] + 12 * k), (xm, a[1] + 12 * k), (xm, yb), (xr, yb), (xr, b[1])])
# ---- wires in from the boat ----
for s, t, col, dy in (('P6', 'BEC 5 V red', '#e03030', 70), ('P1', 'BEC GND black', '#222', 100), ('N5', 'battery sense\n(330k at the battery end)', '#b06000', 130)):
    a = D(s); y = D('P1')[1] + dy
    d.line((a, (a[0], y), (560 + 6 * P + 40, y)), fill=col, width=5); dot(a, col)
    d.text((560 + 6 * P + 48, y - 10), t + '  (from the boat)', fill=col, font=B(14))

# ---- explanation ----
ex = ['HOW ONE LED WORKS (LED 1, red). The two boards are stacked; the dashed lines are the 5 pins, not wires:',
      '1. 5 V comes from the BEC into driver P6, across to P4, down the P4 pin to the LED strip,',
      '   and along its insulated 5 V wire to the long (+) leg of every LED (hole 1).',
      '2. Current goes through the LED, out of its short (-) leg in A2, across to A3, along the red jumper to B5,',
      '   across to B6 and up the B6 pin into the driver board.',
      '3. On the driver board it goes through the 330 (row C) and the BC547 (row B) to GND (hole 1).',
      '4. The BC547 only lets it through when the C3 drives GP4 HIGH (red wire, C3 GP4 -> driver A6 -> 10k).',
      'LEDs 2, 3 and 4 are the same with their own jumpers and pins. Wires may cross over a board: they are insulated.']
for i, t in enumerate(ex):
    d.text((60, 850 + i * 25), t, fill='black' if i == 0 else '#333', font=B(16) if i == 0 else F(16))
im.save(sys.argv[1])
