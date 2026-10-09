"""Draw the v2 idea as a cross-section, plus a thruster side view for
measurements 17-19. Run: python3 sketch.py  (writes 5_idea_and_thruster_side.png)."""
from PIL import Image, ImageDraw, ImageFont
import math
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
Fn = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f = lambda s, b=True: ImageFont.truetype(F if b else Fn, s)
W, H = 1100, 1400
im = Image.new("RGB", (W, H), (250, 250, 247)); d = ImageDraw.Draw(im)
HULL, SAD, BACK, THR, YEL, RED, INK = (40,40,40), (90,150,220), (240,150,60), (130,200,60), (255,200,0), (220,30,30), (30,30,30)

def badge(xy, n):
    x, y = xy; r = 17
    d.ellipse([x-r, y-r, x+r, y+r], fill=RED); d.text((x, y), str(n), font=f(20), fill="white", anchor="mm")
def dim(a, b):
    d.line([a, b], fill=INK, width=3)
    ang = math.atan2(b[1]-a[1], b[0]-a[0]) + math.pi/2
    for p in (a, b):
        d.line([(p[0]-9*math.cos(ang), p[1]-9*math.sin(ang)), (p[0]+9*math.cos(ang), p[1]+9*math.sin(ang))], fill=INK, width=3)

# ---------------- top: cross-section looking forward from the stern ----------
d.text((40, 30), "The idea (v2), cut across one tunnel, looking forward from the stern", font=f(26), fill=INK)
cx, fy = 550, 330          # tunnel centre, flange level (outside face of hull)
R, t = 130, 10             # tunnel radius, wall
fl0, fl1 = 300, 800        # flange extent
# inside backing plate (orange): flat strips on the inside flanges, bridged over the hump
d.rectangle([fl0+10, fy-t-28, cx-R-t-4, fy-t], fill=BACK)
d.rectangle([cx+R+t+4, fy-t-28, fl1-10, fy-t], fill=BACK)
d.chord([cx-R-t-28, fy-R-t-28, cx+R+t+28, fy+R+t+28], 180, 360, fill=BACK)
# hull wall: flanges + arch (the tunnel)
d.rectangle([150, fy-t, cx-R-t, fy], fill=HULL); d.rectangle([cx+R+t, fy-t, 950, fy], fill=HULL)
d.chord([cx-R-t, fy-R-t, cx+R+t, fy+R+t], 180, 360, fill=HULL)
d.chord([cx-R, fy-R, cx+R, fy+R], 180, 360, fill=(250,250,247))
# saddle (blue): fills the tunnel, flat wings on the outside flanges
d.rectangle([fl0+10, fy, fl1-10, fy+26], fill=SAD)
d.chord([cx-R, fy-R, cx+R, fy+R], 180, 360, fill=SAD)
# pocket for the thruster foot, and the thruster
d.rectangle([cx-20, fy-60, cx+20, fy+26], fill=(250,250,247))
d.rectangle([cx-16, fy-56, cx+16, fy+40], fill=THR)
dr = 120
d.ellipse([cx-dr, fy+40, cx+dr, fy+40+2*dr], outline=THR, width=14)
# bolts through wing + flange + backing plate
for bx in (fl0+45, fl1-45):
    d.rectangle([bx-5, fy-t-40, bx+5, fy+34], fill=(160,160,160))
    d.rectangle([bx-14, fy+26, bx+14, fy+36], fill=(120,120,120))
    d.rectangle([bx-12, fy-t-46, bx+12, fy-t-30], fill=(120,120,120))
# labels
lab = lambda xy, s, c=INK: d.text(xy, s, font=f(20), fill=c)
lab((40, 110), "INSIDE the hull", (120,120,120)); lab((40, 380), "OUTSIDE (in the water)", (120,120,120))
lab((815, 230), "backing plate (inside)", BACK); lab((815, 345), "saddle (outside)", SAD)
lab((815, 290), "hull wall", HULL); lab((690, 520), "thruster", (80,150,30))
lab((255, 268), "bolt", (100,100,100))
# the point about flat faces
for x0, x1 in ((fl0+10, cx-R-t-6), (cx+R+t+6, fl1-10)):
    d.line([(x0, fy+2), (x1, fy+2)], fill=YEL, width=6)
d.text((40, 640), "Yellow = where the saddle presses on the hull: the flat strips beside\n"
                  "the tunnel (the ones with the 4 holes). They look flat in the photos,\n"
                  "so these faces are flat; only the part inside the tunnel is curved.\n"
                  "Measurements 6 and 10 confirm it. Thickened epoxy fills any small gap.",
       font=f(19, False), fill=INK, spacing=6)
d.line([(0, 790), (W, 790)], fill=(200,200,200), width=2)

# ---------------- bottom: thruster side view -----------------------------------
d.text((40, 815), "Thruster from the side (draw on yours, or take a side photo)", font=f(26), fill=INK)
y0 = 980; x0, x1 = 230, 760        # duct top line, duct front/back
d.rectangle([x0, y0, x1, y0+250], outline=THR, width=8)               # duct (side)
d.rectangle([x0+40, y0+90, x1-160, y0+160], fill=(110,110,110))       # motor
d.text((x0+60, y0+110), "motor", font=f(20), fill="white")
fx0, fx1 = 400, 600                                                   # foot
d.rectangle([fx0, y0-50, fx1, y0], fill=THR)
for hx in (fx0+30, (fx0+fx1)//2, fx1-30):
    d.ellipse([hx-7, y0-32, hx+7, y0-18], fill="white", outline=INK)
d.text((x0-200, y0+110), "FRONT\n(wires,\ntowards\nthe bow)", font=f(18, False), fill=INK)
d.text((x1+20, y0+110), "BACK\n(prop,\nthe stern)", font=f(18, False), fill=INK)
dim((fx0, y0-80), (fx1, y0-80)); badge(((fx0+fx1)//2, y0-110), 17)
dim((x0, y0+300), (fx0+30, y0+300)); badge(((x0+fx0)//2+15, y0+272), 18)
d.text((40, 1320), "17  length of the foot along the thruster      18  front edge of the duct to the centre of the first hole\n"
                   "19  do the 3 holes run front-to-back, like this drawing? (yes / no)",
       font=f(19, False), fill=INK, spacing=8)
badge((x1+60, y0-30), 19)
im.save("5_idea_and_thruster_side.png")
