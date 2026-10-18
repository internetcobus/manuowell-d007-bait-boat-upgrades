from PIL import Image, ImageDraw, ImageFont
import sys
OUTDIR = sys.argv[1]
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
B = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
P = 44

class Board:
    def __init__(self, d, ox, oy, rows, mirror=False):
        self.d, self.ox, self.oy, self.rows, self.mirror = d, ox, oy, rows, mirror
    def xy(self, h):                      # h like 'C4'
        r = ord(h[0]) - 64; c = int(h[1:]) - 1
        if self.mirror: c = 5 - c
        return self.ox + c * P + P // 2, self.oy + (r - 0.5) * P
    def draw(self, title, sub):
        d, ox, oy = self.d, self.ox, self.oy
        d.rectangle((ox - 6, oy - 4, ox + 6 * P + 6, oy + self.rows * P + 4), fill='#d9c08a', outline='#7a6236', width=2)
        d.text((ox - 6, oy - 88), title, fill='black', font=B(20))
        d.text((ox - 6, oy - 60), sub, fill='#444', font=F(15))
        for c in range(1, 7):
            x, _ = self.xy('A%d' % c); d.text((x - 5, oy - 30), str(c), fill='#555', font=B(16))
        for r in range(1, self.rows + 1):
            L = chr(64 + r); _, y = self.xy(L + '1')
            d.text((ox - 30 if not self.mirror else ox + 6 * P + 14, y - 10), L, fill='#555', font=B(16))
            for c in range(1, 7):
                x, y = self.xy('%s%d' % (L, c))
                d.ellipse((x - 8, y - 8, x + 8, y + 8), fill='#c8a050', outline='#8a6a2a')
                d.ellipse((x - 3, y - 3, x + 3, y + 3), fill='white')
    def pad(self, h, color, rad=10, label=None, lc='white'):
        x, y = self.xy(h); self.d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=color)
        if label: self.d.text((x - 5, y - 8), label, fill=lc, font=B(13))
    def bridge(self, a, b, color='#9a9a9a', w=11):
        x1, y1 = self.xy(a); x2, y2 = self.xy(b); self.d.line((x1, y1, x2, y2), fill=color, width=w)
    def resistor(self, a, b, label, fill='#e8d3a9'):
        d = self.d; x1, y1 = self.xy(a); x2, y2 = self.xy(b)
        d.line((x1, y1, x2, y2), fill='#555', width=3)
        for x, y in ((x1, y1), (x2, y2)): d.ellipse((x - 5, y - 5, x + 5, y + 5), fill='#555')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2; L = abs(x2 - x1) * 0.55 if y1 == y2 else 30
        d.rounded_rectangle((mx - L / 2, my - 10, mx + L / 2, my + 10), 5, fill=fill, outline='#333')
        d.text((mx - 14, my - 8), label, fill='#222', font=B(13))
    def transistor(self, e, b, c):       # legs e-b-c, flat side towards row A
        d = self.d; xe, y = self.xy(e); xc, _ = self.xy(c)
        lo, hi = min(xe, xc), max(xe, xc)
        d.chord((lo - 18, y - 34, hi + 18, y + 20), 0, 180, fill='#222')
        d.rectangle((lo - 18, y - 8, hi + 18, y - 5), fill='#222')
        for h, t in ((e, 'e'), (b, 'b'), (c, 'c')): self.pad(h, '#888', 9, t)
    def notes(self, x, items, y0=None, step=24):
        y0 = self.oy + 4 if y0 is None else y0
        for i, (t, c) in enumerate(items): self.d.text((x, y0 + i * step), t, fill=c, font=F(15))

WC = {1: '#d22', 2: '#2a6fe0', 3: '#1a9a3a', 4: '#9a3ad0'}

# =============================== LED strip ===================================
# Same 16 x 6 footprint as the driver board: it sits UNDER it, row A edges together.
PINS = ['B6', 'E6', 'H6', 'K6', 'P4']
JUMP = [('A3', 'B5'), ('C3', 'E5'), ('E3', 'H5'), ('G3', 'K5')]
im = Image.new('RGB', (1480, 1010), 'white'); d = ImageDraw.Draw(im)
d.text((20, 12), 'LED strip: 16 rows (A-P) x 6 holes, same size as the driver board, which sits on top of it', fill='black', font=B(22))
h = Board(d, 80, 160, 16, mirror=True)
h.draw('Hull face: LEDs + 4 jumper wires', 'Mirror image: hole 1 on the RIGHT. Row A against the GPS LED mount')
for k, (a, b) in enumerate(JUMP, 1):
    (x1, y1), (x2, y2) = h.xy(a), h.xy(b)
    d.line((x1, y1, x1, (y1 + y2) / 2, x2, (y1 + y2) / 2, x2, y2), fill=WC[k], width=6, joint='curve')
    h.pad(a, WC[k], 9); h.pad(b, WC[k], 9)
for i2, r in enumerate('ACEG'):
    x3, y = h.xy(r + '1'); x4, _ = h.xy(r + '2'); cx = (x3 + x4) / 2
    col = '#e02020' if i2 == 0 else '#2a6fe0'
    d.ellipse((cx - 30, y - 30, cx + 30, y + 30), fill=col, outline='black', width=2)
    d.text((cx - 20, y - 9), 'red' if i2 == 0 else 'blue', fill='white', font=B(14))
for pn in PINS: h.pad(pn, '#f2d23c', 11)
h.notes(80 + 6 * P + 50, [
    ('LEDs in rows A, C, E, G:', 'black'),
    ('  long leg (+) in hole 1', '#333'),
    ('  short leg (−) in hole 2', '#333'),
    ('  RED in row A', '#d22'),
    ('  stand them off so the', '#c00000'),
    ('  lenses sit in the holes', '#c00000'),
    ('', 'black'),
    ('Insulated jumpers, lying', 'black'),
    ('on this face, ends soldered', 'black'),
    ('on the back face:', 'black'),
    ('  A3 -> B5   (LED 1)', WC[1]),
    ('  C3 -> E5   (LED 2)', WC[2]),
    ('  E3 -> H5   (LED 3)', WC[3]),
    ('  G3 -> K5   (LED 4)', WC[4]),
    ('', 'black'),
    ('Yellow = the 5 pins', '#b08a00'),
], step=25)
b = Board(d, 820, 160, 16)
b.draw('Back face: bridges, 5 V wire, pins', 'Faces the driver board. Hole 1 on the LEFT')
for a2, b2 in (('A1', 'C1'), ('C1', 'E1'), ('E1', 'G1')): b.bridge(a2, b2, '#e03030', 7)
(gx, gy), (px, py) = b.xy('G1'), b.xy('P4')
d.line((gx, gy, gx, py - 22, px, py - 22, px, py), fill='#e03030', width=7, joint='curve')
for k, (a, c) in enumerate(JUMP, 1):
    r = a[0]; b.bridge(r + '2', r + '3')
    pr = c[0]; b.bridge(pr + '5', pr + '6')
    b.pad(a, WC[k], 10); b.pad(c, WC[k], 10)
for r in 'ACEG':
    b.pad(r + '2', '#555', 10, '−'); b.pad(r + '1', '#555', 10, '+')
for pn in PINS: b.pad(pn, '#f2d23c', 11)
b.notes(820 + 6 * P + 50, [
    ('Bridges (grey):', 'black'),
    ('  2-3 in rows A, C, E, G', '#333'),
    ('  (LED short leg -> jumper)', '#333'),
    ('  5-6 in rows B, E, H, K', '#333'),
    ('  (jumper -> pin)', '#333'),
    ('', 'black'),
    ('5 V: INSULATED wire, stripped', 'black'),
    ('only where soldered:', 'black'),
    ('  A1-C1-E1-G1 (the + legs),', '#e03030'),
    ('  then on to the P4 pin', '#e03030'),
    ('Not bare: the driver GND wire', '#c00000'),
    ('runs right above hole 1', '#c00000'),
    ('', 'black'),
    ('Pins (yellow) through BOTH', 'black'),
    ('boards at the same holes:', 'black'),
    ('  B6 LED 1   E6 LED 2', '#333'),
    ('  H6 LED 3   K6 LED 4', '#333'),
    ('  P4 5 V', '#e03030'),
], step=25)
im.save(OUTDIR + '/gauge-led-strip.png')

# ============================== driver board =================================
im = Image.new('RGB', (1480, 1010), 'white'); d = ImageDraw.Draw(im)
d.text((20, 12), 'Driver board: 16 rows (A-P) x 6 holes, about 15 x 41 mm. Stacked on top of the LED strip.', fill='black', font=B(22))
CH = [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I'), ('J', 'K', 'L')]
p = Board(d, 80, 160, 16)
p.draw('Parts side (faces into the boat)', 'Resistors lie flat, legs 3 holes apart')
for k, (r0, r1, r2) in enumerate(CH, 1):
    p.resistor(r0 + '2', r0 + '5', '10k')
    p.transistor(r1 + '1', r1 + '2', r1 + '3')
    p.resistor(r2 + '3', r2 + '6', '330')
    x, y = p.xy(r1 + '4'); d.text((x - 4, y - 9), 'LED %d' % k, fill=WC[k], font=B(15))
p.resistor('N1', 'N4', '10k')
p.resistor('O1', 'O3', '100n', fill='#e8a33a')
p.notes(80 + 6 * P + 46, [
    ('Each LED uses 3 rows', 'black'),
    ('(A-C, D-F, G-I, J-L):', 'black'),
    ('  row 1: 10k in holes 2-5', '#333'),
    ('  row 2: BC547 legs e-b-c', '#333'),
    ('    in 1-2-3, FLAT side', '#c00000'),
    ('    towards row A', '#c00000'),
    ('  row 3: 330 in holes 3-6', '#333'),
    ('', 'black'),
    ('Row M: empty gap', 'black'),
    ('Row N: 10k in 1-4', '#333'),
    ('Row O: 100n in 1-3', '#333'),
    ('  (battery divider)', '#333'),
    ('Row P: wires in/out', 'black'),
], step=25)

q = Board(d, 820, 160, 16, mirror=True)
q.draw('Solder side (faces the LED strip)', 'Mirror image: hole 1 on the RIGHT')
q.bridge('A1', 'P1', '#222', 9)                    # GND rail
for k, (r0, r1, r2) in enumerate(CH, 1):
    q.bridge(r0 + '5', r0 + '6')                   # 10k -> GPIO wire
    q.bridge(r0 + '2', r1 + '2')                   # 10k -> base
    q.bridge(r1 + '3', r2 + '3')                   # collector -> 330
    q.bridge(r1 + '6', r2 + '6')                   # LED wire -> 330
    q.pad(r0 + '6', WC[k], 11); q.pad(r1 + '6', WC[k], 11)
for a, b in (('N4', 'N5'), ('O3', 'O4'), ('O4', 'N4'), ('O4', 'O5'), ('P1', 'P2'), ('P4', 'P5'), ('P5', 'P6')):
    q.bridge(a, b)
for h, c in (('N5', '#b06000'), ('O5', '#f0a000'), ('P1', '#222'), ('P2', '#777'), ('P4', '#ff7a00'), ('P5', '#ff7a00'), ('P6', '#e03030')):
    q.pad(h, c, 11)
q.notes(820 + 6 * P + 56, [
    ('Bridges (grey), each LED:', 'black'),
    ('  row 1: 5-6;  rows 1-2: hole 2', '#333'),
    ('  rows 2-3: holes 3 and 6', '#333'),
    ('  e.g. A5-A6, A2-B2, B3-C3, B6-C6', '#333'),
    ('Divider: N4-N5, N4-O4, O3-O4-O5', '#333'),
    ('Power: P1-P2, P4-P5-P6', '#333'),
    ('GND: bare wire along hole 1, A-P', '#222'),
    ('', 'black'),
    ('IN from the boat:', 'black'),
    ('  BEC 5 V red   -> P6', '#e03030'),
    ('  BEC GND black -> P1', '#222'),
    ('  sense (from the 330k) -> N5', '#b06000'),
    ('', 'black'),
    ('To the C3 Zero:', 'black'),
    ('  P5 -> 5V        P2 -> GND', '#ff7a00'),
    ('  O5 -> GP3 (battery sense)', '#f0a000'),
    ('  A6 -> GP4   D6 -> GP5', '#333'),
    ('  G6 -> GP6   J6 -> GP7', '#333'),
    ('', 'black'),
    ('Pins from the LED strip below:', 'black'),
    ('  B6 LED 1 (red)   E6 LED 2', '#333'),
    ('  H6 LED 3         K6 LED 4', '#333'),
    ('  P4 5 V to the LEDs', '#ff7a00'),
], step=25)
for pn in ['B6', 'E6', 'H6', 'K6', 'P4']:
    p.pad(pn, '#f2d23c', 11); q.pad(pn, '#f2d23c', 11)
im.save(OUTDIR + '/gauge-driver-board.png')
