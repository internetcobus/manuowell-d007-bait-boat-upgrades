# Draws gauge-stack.png: side view of the LED strip + driver board stack.
#   python3 gauge_stack.py docs/images/gauge-stack.png
from PIL import Image, ImageDraw, ImageFont
import sys
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
B = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
S = 14                                    # px per mm
W, H = 1500, 760
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
d.text((20, 12), 'The stack, side view (not to scale along the board; heights roughly to scale)', fill='black', font=B(22))
x0, x1 = 160, 1000                        # board length (row A at the left)
y = 120
# hull wall
d.rectangle((60, y, x1 + 160, y + 3 * S), fill='#555'); d.text((x1 + 175, y + 8), 'hull wall (3 mm)', fill='#333', font=B(16))
yl = y + 3 * S
for i, xc in enumerate((220, 300, 380, 460)):
    d.rectangle((xc - 1.5 * S, y, xc + 1.5 * S, yl), fill='white')
    col = '#e02020' if i == 0 else '#2a6fe0'
    d.rounded_rectangle((xc - 1.5 * S, y + 4, xc + 1.5 * S, yl + 5.3 * S), 18, fill=col, outline='black')
    d.rectangle((xc - 1.9 * S, yl + 4.3 * S, xc + 1.9 * S, yl + 5.3 * S), fill=col, outline='black')
    for dx in (-0.6 * S, 0.6 * S): d.line((xc + dx, yl + 5.3 * S, xc + dx, yl + 9 * S), fill='#888', width=3)
d.text((500, yl + 20), 'LEDs: lenses in the hull holes,\nstood off the strip on their legs', fill='#333', font=F(15))
d.ellipse((140, y - 10, 180, y + 3 * S + 10), outline='#c00000', width=3)
d.text((30, y + 3 * S + 30), 'GPS LED\nmount here', fill='#c00000', font=B(14))
# LED strip
ys = yl + 7 * S
d.rectangle((x0, ys, x1, ys + 1.6 * S), fill='#d9c08a', outline='#7a6236'); d.text((x1 + 20, ys - 2), 'LED strip (1.6 mm)', fill='#333', font=B(16))
d.text((x0, ys - 26), 'row A', fill='#555', font=B(13)); d.text((x1 - 50, ys - 26), 'row P', fill='#555', font=B(13))
# jumpers on hull face
d.line((240, ys - 4, 330, ys - 4), fill='#d22', width=4); d.line((320, ys - 8, 520, ys - 8), fill='#2a6fe0', width=4)
d.text((560, ys - 34), 'jumpers on this face, under the raised LEDs', fill='#333', font=F(14))
# spacer + tape
yt = ys + 1.6 * S
d.rectangle((x0, yt, x1, yt + 0.4 * S), fill='#222')
d.text((x1 + 20, yt + 0.2 * S), 'insulating tape on the LED strip back face', fill='#222', font=B(15))
# driver board
yd = yt + 2.5 * S
d.rectangle((x0, yd, x1, yd + 1.6 * S), fill='#d9c08a', outline='#7a6236'); d.text((x1 + 20, yd + 2), 'driver board (1.6 mm)', fill='#333', font=B(16))
# pins with spacers
for xp in (260, 400, 540, 680, 960):
    d.line((xp, ys - 10, xp, yd + 1.6 * S + 14), fill='#b08a00', width=5)
    d.rectangle((xp - 9, yt + 0.4 * S, xp + 9, yd), fill='#333')
d.text((1040, 60), 'pins at B6, E6, H6, K6, P4: header pins with their\nplastic spacer (2.5 mm), through both boards', fill='#b08a00', font=B(15))
# parts on top
yp = yd + 1.6 * S
for xa in (200, 340, 480, 620):
    d.chord((xa, yp, xa + 70, yp + 5 * S * 2), 180, 360, fill='#222')
    d.rounded_rectangle((xa + 80, yp, xa + 130, yp + 2.6 * S), 5, fill='#e8d3a9', outline='#333')
d.rounded_rectangle((780, yp, 840, yp + 2.6 * S), 5, fill='#e8d3a9', outline='#333')
d.rounded_rectangle((860, yp, 900, yp + 2.6 * S), 5, fill='#e8a33a', outline='#333')
d.text((x1 + 20, yp + 20), 'transistors + resistors\n(face into the boat)', fill='#333', font=B(15))
# harness
d.line((940, yp + 10, 1000, yp + 120, 1180, yp + 120), fill='#555', width=6)
d.text((1190, yp + 108), '7-wire harness to the C3 Zero\n(higher up, face-down on foam tape)\n+ 3 wires from the boat', fill='#333', font=B(15))
ins = ['Build order:',
       '1. Build the LED strip (LEDs, bridges, jumpers, 5 V wire).',
       '2. Build the driver board (parts, bridges, GND wire).',
       '3. Put insulating tape over the LED strip back face (after testing the LEDs).',
       '4. Push 5 header pins through the tape at B6, E6, H6, K6, P4, spacers against it; solder them on the hull face.',
       '5. Lower the driver board solder side down onto the pins; solder them on its parts side; trim.',
       '6. Check with a meter: P4 to every LED + leg = 0 ohm, and P4 to driver P1 (GND) is NOT a short.',
       'Stick the stack to the hull with foam tape or glue on its edges: do not let it hang on the LEDs.']
for i, t in enumerate(ins):
    d.text((40, 520 + i * 27), t, fill='black' if i == 0 else '#333', font=B(16) if i == 0 else F(16))
im.save(sys.argv[1])
