"""Thruster mount v2 drawn TO SCALE from Cobus's measurements (2026-10-09).
Run: python3 sketch_v2.py  (writes 8_v2_to_scale.png). All numbers in mm."""
from PIL import Image, ImageDraw, ImageFont
import math
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; Fn = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f = lambda s, b=True: ImageFont.truetype(F if b else Fn, s)
K = 5.0                                  # px per mm
W, H = 1200, 1500
im = Image.new("RGB", (W, H), (250, 250, 247)); d = ImageDraw.Draw(im)
HULL, SAD, THR, SCR, INK, GREY = (40,40,40), (90,150,220), (130,200,60), (150,150,150), (30,30,30), (120,120,120)

# measurements
TUN_W, TUN_D, TUN_L = 43, 10, 69          # 4, 9, 5
STRIP, HOLE_X, HOLE_PITCH = 9, 59, 62     # 6, 2, 3
WALL = 3                                  # 13
DUCT_MAX, DUCT_EDGE, DUCT_L = 74, 67, 75  # 14, spec
FOOT_W, FOOT_L, FOOT_H = 10, 50, 8.5      # 16, 17, 15
HOLE1 = 14.5                              # 18
WIRE = 111                                # 7
DROP = 5                                  # proposal: saddle face this far below the hull

def T(x, y, ox, oy): return (ox + x*K, oy + y*K)   # mm -> px, y down = deeper

# ------------- A: side view, bow left, stern (transom) right --------------------
d.text((30, 20), "A  Side view, cut down the middle of one tunnel (to scale)", font=f(24), fill=INK)
ox, oy = 1080, 260                     # transom at x=0, hull bottom plane at y=0; x negative = forward
# hull: bottom plane forward of the tunnel, tunnel roof, transom
d.polygon([T(-150,0,ox,oy), T(-TUN_L,0,ox,oy), T(-TUN_L,-TUN_D,ox,oy), T(0,-TUN_D,ox,oy), T(0,-TUN_D-WALL,ox,oy),
           T(-TUN_L-WALL,-TUN_D-WALL,ox,oy), T(-TUN_L-WALL,-WALL,ox,oy), T(-150,-WALL,ox,oy)], fill=HULL)
d.rectangle([*T(0,-TUN_D-WALL-40,ox,oy), *T(WALL,-TUN_D,ox,oy)], fill=HULL)     # transom
# wire hole
wx = -WIRE
d.rectangle([*T(wx-5.5,-WALL,ox,oy), *T(wx+5.5,0,ox,oy)], fill=(250,250,247))
# saddle: fills the tunnel, DROP below the hull
d.rectangle([*T(-TUN_L,-TUN_D,ox,oy), *T(0,DROP,ox,oy)], fill=SAD)
d.polygon([T(-TUN_L,0,ox,oy), T(-TUN_L-12,0,ox,oy), T(-TUN_L,DROP,ox,oy)], fill=SAD)   # sloped nose
# thruster: duct top at DROP, foot sunk into the saddle
dx0 = -DUCT_L + 4                    # duct ends 4 mm past... flush-ish with the transom
fx0 = dx0 + HOLE1 - 5
d.rectangle([*T(fx0, DROP-FOOT_H, ox, oy), *T(fx0+FOOT_L, DROP, ox, oy)], fill=THR)
d.rectangle([*T(dx0, DROP, ox, oy), *T(dx0+DUCT_L, DROP+DUCT_MAX, ox, oy)], outline=THR, width=6)
d.rectangle([*T(dx0+8, DROP+DUCT_MAX/2-9, ox, oy), *T(dx0+50, DROP+DUCT_MAX/2+9, ox, oy)], fill=(110,110,110))
# foot screws: from inside the duct, up through the foot into the saddle
for i in range(3):
    hx = dx0 + HOLE1 + 20*i
    d.rectangle([*T(hx-1.5, DROP-FOOT_H-5, ox, oy), *T(hx+1.5, DROP+1, ox, oy)], fill=SCR)
# wires: motor front -> wire hole
d.line([T(dx0+8, DROP+DUCT_MAX/2, ox, oy), T(wx, DROP+DUCT_MAX/2, ox, oy), T(wx, -WALL-8, ox, oy)], fill=(200,60,60), width=4)
lab = lambda xy, s, c=INK, z=19: d.text(xy, s, font=f(z), fill=c)
lab(T(-150,-WALL-14,ox,oy), "INSIDE", GREY); lab(T(-150,12,ox,oy), "OUTSIDE (water)", GREY)
lab((ox-110, oy-200), "transom", HULL); lab(T(-TUN_L+5,-TUN_D-14,ox,oy), "tunnel, 69 long x 10 deep", HULL)
lab(T(-60, DROP+DUCT_MAX+3, ox, oy), "duct, 75 long, 74 across the middle", (80,150,30))
lab(T(-145, DROP+DUCT_MAX/2-14, ox, oy), "wires to the\nwire hole (111\nfrom transom)", (200,60,60), 17)
lab((40, 700), "Blue = the saddle. It fills the tunnel and sits 5 mm below the hull, so the duct's top is 5 mm\n"
               "clear of the hull for water to reach the intake. The foot (green) sinks 8.5 mm into the saddle.\n"
               "Grey = the 3 foot screws, put in from inside the duct through its two oval openings.\n"
               "The thruster's position fore and aft is a first guess until I have measurement 20.",
    INK, 18)
d.line([(0, 800), (W, 800)], fill=(200,200,200), width=2)

# ------------- B: section across the tunnel, looking forward -------------------
d.text((30, 820), "B  Cut across the tunnel, looking forward (to scale)", font=f(24), fill=INK)
cx, cy = 600, 1010
R = TUN_W**2/(8*TUN_D) + TUN_D/2                       # 28.1
half = TUN_W/2
pts = [T(-80,0,cx,cy), T(-half,0,cx,cy)]
for a in range(0, 101):
    x = -half + TUN_W*a/100; y = -(math.sqrt(R*R - x*x) - (R - TUN_D))
    pts.append(T(x, y, cx, cy))
pts += [T(80,0,cx,cy), T(80,-WALL,cx,cy)]
inner = []
for a in range(100, -1, -1):
    x = -half - WALL + (TUN_W + 2*WALL)*a/100; Ri = R + WALL
    inner.append(T(x, -(math.sqrt(max(Ri*Ri - x*x,0)) - (R - TUN_D)), cx, cy))
d.polygon(pts + [T(half+WALL,-WALL,cx,cy)] + inner + [T(-half-WALL,-WALL,cx,cy), T(-80,-WALL,cx,cy)], fill=HULL)
# saddle: tunnel fill + wings to the holes, DROP below
sad = [T(-HOLE_X/2-5, 0, cx, cy)] + pts[2:-2] + [T(HOLE_X/2+5, 0, cx, cy), T(HOLE_X/2+5, DROP, cx, cy), T(-HOLE_X/2-5, DROP, cx, cy)]
d.polygon(sad, fill=SAD)
# foot pocket + foot, duct
d.rectangle([*T(-FOOT_W/2, DROP-FOOT_H, cx, cy), *T(FOOT_W/2, DROP, cx, cy)], fill=THR)
d.ellipse([*T(-DUCT_MAX/2, DROP, cx, cy), *T(DUCT_MAX/2, DROP+DUCT_MAX, cx, cy)], outline=THR, width=6)
# screws into the posts
for sx in (-HOLE_X/2, HOLE_X/2):
    d.rectangle([*T(sx-1.2, -11, cx, cy), *T(sx+1.2, DROP, cx, cy)], fill=SCR)
    d.rectangle([*T(sx-2.5, -11-WALL-3, cx, cy), *T(sx+2.5, -WALL, cx, cy)], fill=GREY)   # the post
lab(T(-80,-WALL-10,cx,cy), "INSIDE", GREY); lab(T(-80,10,cx,cy), "OUTSIDE", GREY)
lab(T(HOLE_X/2+8,-24,cx,cy), "post inside the hull\n(its screw goes up\ninto it from outside)", GREY, 17)
lab(T(-HOLE_X/2-48, 18, cx, cy), "saddle", SAD)
lab((40, 1410), "The tunnel is a SHALLOW arc (43 wide, 10 deep, radius about 28), not a half-circle. The saddle's\n"
                "top follows it; its wings sit on the flat 9 mm strips and screw into the 4 posts from outside.",
    INK, 18)
im.save("8_v2_to_scale.png")
