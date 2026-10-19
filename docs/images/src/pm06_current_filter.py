# Draws pm06-current-filter.png: a 10k + 100 nF low-pass in the CURRENT wire
# (pin 3) of the PM06 -> Pixhawk adapter, at the Pixhawk end, to stop the
# 433 MHz SiK radio showing up as false current.
#   python3 pm06_current_filter.py docs/images/pm06-current-filter.png
from PIL import Image, ImageDraw, ImageFont
import sys
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
B = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
W, H = 1400, 790
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
d.text((20, 14), 'PM06 current filter: 10k + 100 nF in the adapter cable, at the Pixhawk end', fill='black', font=B(24))
names = ['1 VCC', '2 VCC', '3 CURRENT', '4 VOLTAGE', '5 GND', '6 GND']
cols = ['#e03030', '#e03030', '#f0a000', '#2a6fe0', '#222', '#222']   # drawing colours, not the cable's
y0, dy = 140, 70
# PM06-end plug and Pixhawk-end plug
d.rounded_rectangle((60, y0 - 40, 230, y0 + 5 * dy + 40), 8, fill='#eee', outline='#333', width=2)
d.text((70, y0 - 75), 'PM06 end (JST-GH)', fill='black', font=B(16))
d.rounded_rectangle((1150, y0 - 40, 1340, y0 + 5 * dy + 40), 8, fill='#eee', outline='#333', width=2)
d.text((1130, y0 - 75), 'Pixhawk end (DF13)\nPOWER port', fill='black', font=B(16))
for i, (n, c) in enumerate(zip(names, cols)):
    y = y0 + i * dy
    d.text((80, y - 10), n, fill='black', font=B(15)); d.text((1165, y - 10), n, fill='black', font=B(15))
    if i != 2:
        d.line((230, y, 1150, y), fill=c, width=6)
# pin 3 with the resistor and capacitor
y3, yg = y0 + 2 * dy, y0 + 4 * dy
d.line((230, y3, 780, y3), fill='#f0a000', width=6)
d.rectangle((780, y3 - 16, 900, y3 + 16), fill='#e8d3a9', outline='#333', width=2)
d.text((805, y3 - 11), '10k', fill='black', font=B(18))
d.line((900, y3, 1150, y3), fill='#f0a000', width=6)
xc = 1040
d.ellipse((xc - 7, y3 - 7, xc + 7, y3 + 7), fill='black')
y4 = y0 + 3 * dy                     # hop over the voltage wire: NOT joined
d.line((xc, y3, xc, y4 - 14), fill='#555', width=4)
d.arc((xc - 14, y4 - 14, xc + 14, y4 + 14), 270, 90, fill='#555', width=4)
d.line((xc, y4 + 14, xc, y4 + 26), fill='#555', width=4)
d.rectangle((xc - 28, y4 + 26, xc + 28, y4 + 32), fill='#333'); d.rectangle((xc - 28, y4 + 40, xc + 28, y4 + 46), fill='#333')
d.text((xc - 115, y4 + 24), '100 nF\nceramic', fill='black', font=B(15))
d.line((xc, y4 + 46, xc, yg), fill='#555', width=4)
d.text((xc - 175, y4 - 34), 'hops over: not joined', fill='#555', font=F(13))
d.ellipse((xc - 7, yg - 7, xc + 7, yg + 7), fill='black')
# dimension: close to the plug
d.line((xc, y0 + 5 * dy + 60, 1150, y0 + 5 * dy + 60), fill='#c00000', width=2)
d.text((xc - 10, y0 + 5 * dy + 66), 'within ~3 cm of the plug', fill='#c00000', font=B(14))
notes = ['1. Cut ONLY the CURRENT wire (pin 3, third from the end; check its colour at both plugs), about 4 cm from the Pixhawk plug.',
         '2. Solder the 10k in line (PM06 side to one leg, Pixhawk side to the other). Heat-shrink it.',
         '3. On the Pixhawk side of the 10k: one leg of the 100 nF. Other leg to a GND wire (pin 5 or 6):',
         '   strip a few mm of that wire\'s insulation, solder, heat-shrink. Keep the capacitor legs SHORT.',
         '4. Beeper check, unplugged: pin 3 end to end must NOT beep now (10k). Pin 3 to GND must not beep.',
         'The voltage wire (pin 4) is untouched. The 10k + 100 nF smooths over ~1 ms: real current changes are far slower.']
for i, t in enumerate(notes):
    d.text((60, 560 + i * 30 + 20), t, fill='#222', font=F(17))
im.save(sys.argv[1])
