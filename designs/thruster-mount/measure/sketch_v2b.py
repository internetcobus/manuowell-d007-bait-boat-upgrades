"""v2 with a two-part saddle: a BASE screwed to the 4 hull posts, and a
CARRIER bolted to the thruster's foot that slides into the base from the stern.
To scale (mm). Run: python3 sketch_v2b.py  (writes 10_v2_two_part.png)."""
from PIL import Image, ImageDraw, ImageFont
import math
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Fn = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f = lambda s, b=True: ImageFont.truetype(F if b else Fn, s)
K = 5.0; W, H = 1200, 1480
im = Image.new("RGB", (W, H), (250, 250, 247)); d = ImageDraw.Draw(im)
INK, GREY, HULL, BASE, CAR, THR, SCR = (30,30,30), (120,120,120), (40,40,40), (90,150,220), (150,90,200), (130,200,60), (150,150,150)
TUN_W, TUN_D, WALL, HX = 43, 10, 3, 59/2
DROP, FOOT_W, FOOT_H, DUCT = 5, 10, 8.5, 74
CAR_W, CAR_H = 20, 13                    # carrier: dovetail bar holding the foot
R = TUN_W**2/(8*TUN_D) + TUN_D/2
lab = lambda xy, t, c=INK, z=19: d.text(xy, t, font=f(z), fill=c)

# ---------- A: cut across, looking forward ----------
d.text((30, 20), "A  Cut across the tunnel, looking forward (to scale)", font=f(24), fill=INK)
cx, cy = 600, 250
T = lambda x, y: (cx + x*K, cy + y*K)
arc = lambda x, r: -(math.sqrt(max(r*r - x*x, 0)) - (R - TUN_D))
# hull
top = [T(-75, -WALL), T(-TUN_W/2-WALL, -WALL)] + [T(x/10, arc(x/10, R+WALL)) for x in range(int(-(TUN_W/2+WALL)*10), int((TUN_W/2+WALL)*10)+1)] + [T(TUN_W/2+WALL, -WALL), T(75, -WALL)]
bot = [T(75, 0), T(TUN_W/2, 0)] + [T(x/10, arc(x/10, R)) for x in range(int(TUN_W/2*10), int(-TUN_W/2*10)-1, -1)] + [T(-TUN_W/2, 0), T(-75, 0)]
d.polygon(top + bot, fill=HULL)
# base: tunnel fill + wings, DROP below the hull, with a dovetail slot from below
base = [T(-HX-6, 0), T(-TUN_W/2, 0)] + [T(x/10, arc(x/10, R)) for x in range(int(-TUN_W/2*10), int(TUN_W/2*10)+1)] + [T(TUN_W/2, 0), T(HX+6, 0), T(HX+6, DROP), T(-HX-6, DROP)]
d.polygon(base, fill=BASE)
top_w, bot_w = CAR_W + 4, CAR_W        # dovetail: wider at the top
dv = [T(-bot_w/2, DROP), T(-top_w/2, DROP-CAR_H), T(top_w/2, DROP-CAR_H), T(bot_w/2, DROP)]
d.polygon(dv, fill=CAR)
# foot in the carrier, screws from the carrier's top into the foot
d.rectangle([*T(-FOOT_W/2, DROP-FOOT_H), *T(FOOT_W/2, DROP)], fill=THR)
d.rectangle([*T(-1.6, DROP-CAR_H+0.5), *T(1.6, DROP-FOOT_H+5)], fill=SCR)
d.rectangle([*T(-3, DROP-CAR_H+0.5), *T(3, DROP-CAR_H+3)], fill=SCR)
d.ellipse([*T(-DUCT/2, DROP), *T(DUCT/2, DROP+DUCT)], outline=THR, width=6)
# base screws into the posts, and the side locking screw
for sx in (-HX, HX):
    d.rectangle([*T(sx-3.1, -WALL-14.5), *T(sx+3.1, -WALL)], fill=GREY)
    d.rectangle([*T(sx-1.3, -12), *T(sx+1.3, DROP)], fill=SCR)
d.rectangle([*T(2, DROP-3.2), *T(HX+6, DROP-1.8)], fill=(220,60,60))
lab(T(HX+9, DROP-2), "locking screw from the side,\nbetween the posts (not in line\nwith them), under the hull", (200,40,40), 17)
lab(T(-75, -WALL-12), "INSIDE", GREY); lab(T(-75, 10), "OUTSIDE", GREY)
lab(T(-HX-2, DROP+3), "BASE (blue)", BASE, 22); lab(T(-55, -22), "CARRIER (purple)", CAR, 22)
lab(T(HX-2, -WALL-24), "post", GREY, 17)

# ---------- B: side view, how it goes together ----------
d.line([(0, 680), (W, 680)], fill=(200,200,200), width=2)
d.text((30, 700), "B  Side view: how it goes together", font=f(24), fill=INK)
K2 = 5.0; sx0, sy0 = 1050, 860
S = lambda x, y: (sx0 + x*K2, sy0 + y*K2)
d.rectangle([*S(-150, -WALL), *S(-69, 0)], fill=HULL)
d.rectangle([*S(-69-WALL, -10-WALL), *S(0, -10)], fill=HULL); d.rectangle([*S(-69-WALL, -10-WALL), *S(-69, 0)], fill=HULL)
d.rectangle([*S(0, -10-WALL-25), *S(WALL, -10)], fill=HULL)
d.rectangle([*S(-80, -10), *S(0, DROP)], fill=BASE)                      # base
d.rectangle([*S(-72, DROP-13), *S(0, DROP)], fill=CAR)                   # carrier
d.rectangle([*S(-65.5, DROP-8.5), *S(-15.5, DROP)], fill=THR)            # foot
d.rectangle([*S(-75, DROP), *S(0, DROP+DUCT)], outline=THR, width=5)     # duct
d.polygon([S(-72, DROP-13), S(-76, DROP-13), S(-72, DROP-9)], fill=BASE)
for y in (20.5, 40.5, 60.5):
    d.rectangle([*S(-y-1.5, DROP-12.5), *S(-y+1.5, DROP-4)], fill=SCR)
d.line([S(6, DROP+30), S(30, DROP+30)], fill=CAR, width=6)
d.polygon([S(6, DROP+30), S(14, DROP+25), S(14, DROP+35)], fill=CAR)
lab(S(-150, -WALL-12), "INSIDE", GREY); lab(S(-150, 8), "OUTSIDE", GREY)
lab(S(-30, DROP+40), "slides in from\nthe stern", CAR, 17)
lab(S(-140, DROP+25), "stop at the front:\nforward thrust pushes\nthe carrier into it", INK, 17)
lab((30, 1300),
    "1  Screw the BASE (blue) to the 4 hull posts, from outside, with the thruster off.\n"
    "2  Bolt the thruster's foot into the CARRIER (purple): 3 screws down through its top into\n"
    "   the foot's holes. Tap those holes M4 (drill 3.3 mm first). Do NOT drill through: a bolt\n"
    "   poking out of the foot would hit the propeller.\n"
    "3  Slide the carrier into the base from the stern, then fit the locking screw from the side.",
    INK, 18)
im.save("10_v2_two_part.png")
