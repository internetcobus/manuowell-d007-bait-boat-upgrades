"""Plan view of thruster mount v2, TO SCALE, looking up at the hull bottom with
the transom at the top (same way round as photo 1). From measurements 1-22.
Run: python3 plan_v2.py  (writes 9_v2_plan.png). Units mm."""
from PIL import Image, ImageDraw, ImageFont
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Fn = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f = lambda s, b=True: ImageFont.truetype(F if b else Fn, s)
K = 5.0; W, H = 1000, 1000; ox, oy = 500, 130          # x=0 centreline, y=0 transom edge
im = Image.new("RGB", (W, H), (250, 250, 247)); d = ImageDraw.Draw(im, "RGBA")
P = lambda x, y: (ox + x*K, oy + y*K)
INK, HULL, SAD, THR, POST, RED = (30,30,30), (60,60,60), (90,150,220,150), (130,200,60), (120,120,120), (220,30,30)
TUN_W, TUN_L, STRIP = 43, 69, 9; HX, HY1, HPITCH = 59/2, 12, 62
DUCT_R, DUCT_L, FOOT_W, FOOT_L, HOLE1 = 37, 75, 10, 50, 14.5
WIRE_Y, WIRE_D = 111, 11
# hull features (outline)
d.line([P(-90, 0), P(90, 0)], fill=HULL, width=4); d.text(P(-90, -9), "transom edge", font=f(18), fill=HULL)
d.rectangle([*P(-TUN_W/2, 0), *P(TUN_W/2, TUN_L)], outline=HULL, width=3)
for s in (-1, 1):
    x0, x1 = sorted((s*TUN_W/2, s*(TUN_W/2+STRIP)))
    d.rectangle([*P(x0, 0), *P(x1, TUN_L+8)], outline=HULL, width=2)
d.ellipse([*P(-WIRE_D/2, WIRE_Y-WIRE_D/2), *P(WIRE_D/2, WIRE_Y+WIRE_D/2)], outline=HULL, width=3)
# saddle (blue, translucent) incl. the optional wire fairing forward to the hole
d.polygon([P(-35, 0), P(35, 0), P(35, HY1+HPITCH+7), P(10, WIRE_Y+9), P(-10, WIRE_Y+9), P(-35, HY1+HPITCH+7)], fill=SAD)
# thruster: duct footprint, aft edge at the transom; foot + its 3 holes
d.rectangle([*P(-DUCT_R, 0), *P(DUCT_R, DUCT_L)], outline=THR, width=5)
fy0 = DUCT_L - HOLE1 - 5
d.rectangle([*P(-FOOT_W/2, fy0 - FOOT_L + 10), *P(FOOT_W/2, fy0 + 10)], fill=THR)
for i in range(3):
    y = DUCT_L - HOLE1 - 20*i
    d.ellipse([*P(-1.5, y-1.5), *P(1.5, y+1.5)], fill="white", outline=INK)
# the 4 posts (screw holes)
for s in (-1, 1):
    for y in (HY1, HY1 + HPITCH):
        d.ellipse([*P(s*HX-3.1, y-3.1), *P(s*HX+3.1, y+3.1)], fill=POST, outline=INK, width=2)
# dimensions / labels
lab = lambda xy, t, c=INK, z=17: d.text(xy, t, font=f(z), fill=c)
lab(P(40, 10), "post + screw, 12 from\nthe transom (#20)")
lab(P(40, 70), "post + screw, 74 from\nthe transom (12 + 62)")
lab(P(-88, 30), "tunnel\n43 x 69", HULL)
lab(P(40, 35), "duct, 74 across,\naft edge at\nthe transom", (80,150,30))
lab(P(-88, 105), "wire hole\n111 from\nthe transom", HULL)
lab(P(14, 95), "saddle carries on\nforward over the wires\n(optional)", (40,90,170))
lab((30, 800), "Blue = the saddle. Grey = the 4 existing posts (screws go up into them from outside).\n"
               "Green = the thruster seen from below: the duct outline, and its foot with the 3 holes.\n"
               "The duct covers the post screws, so: screw the saddle to the hull FIRST, then fit\n"
               "the thruster to the saddle through the duct's oval openings.", INK, 17)
d.text((30, 30), "C  Plan view, looking up at the hull bottom (to scale)", font=f(24), fill=INK)
im.save("9_v2_plan.png")
