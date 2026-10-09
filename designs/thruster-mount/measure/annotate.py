"""Draw numbered measurement lines on copies of the thruster-mount photos.
Re-run: python3 annotate.py. It only writes pictures that do not exist yet,
because Cobus adds his own marks to them; delete one first to redraw it."""
from PIL import Image, ImageDraw, ImageFont
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, "..", "photos")
F  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
YEL, RED, WHITE, BLACK = (255, 214, 0), (220, 30, 30), (255, 255, 255), (0, 0, 0)

def font(sz): return ImageFont.truetype(F, sz)

def badge(d, xy, n, col=RED):
    x, y = xy; r = 17
    d.ellipse([x-r-2, y-r-2, x+r+2, y+r+2], fill=WHITE)
    d.ellipse([x-r, y-r, x+r, y+r], fill=col)
    d.text((x, y), str(n), font=font(20), fill=WHITE, anchor="mm")

def line(d, a, b, w=4, ticks=True):
    for col, ww in ((BLACK, w+4), (YEL, w)):
        d.line([a, b], fill=col, width=ww)
    if ticks:   # end ticks, perpendicular
        ang = math.atan2(b[1]-a[1], b[0]-a[0]) + math.pi/2
        dx, dy = 11*math.cos(ang), 11*math.sin(ang)
        for p in (a, b):
            for col, ww in ((BLACK, w+4), (YEL, w)):
                d.line([(p[0]-dx, p[1]-dy), (p[0]+dx, p[1]+dy)], fill=col, width=ww)

def ring(d, c, r, w=4):
    for col, ww in ((BLACK, w+4), (YEL, w)):
        d.ellipse([c[0]-r, c[1]-r, c[0]+r, c[1]+r], outline=col, width=ww)

def note(d, xy, text, sz=20, anchor="la"):
    x, y = xy
    bb = d.textbbox((x, y), text, font=font(sz), anchor=anchor)
    d.rectangle([bb[0]-6, bb[1]-4, bb[2]+6, bb[3]+4], fill=(0, 0, 0, 200))
    d.text((x, y), text, font=font(sz), fill=WHITE, anchor=anchor)

def title(d, w, text):
    d.rectangle([0, 0, w, 44], fill=BLACK)
    d.text((12, 22), text, font=font(22), fill=WHITE, anchor="lm")

def make(src, out, ttl, draw):
    # Cobus marks up these pictures himself (6 has his blue circle), so never
    # overwrite one that exists. Delete the file first to regenerate it.
    if os.path.exists(os.path.join(HERE, out)):
        print("kept (exists):", out); return
    im = Image.open(os.path.join(PH, src)).convert("RGB")
    d = ImageDraw.Draw(im, "RGBA")
    draw(d)
    title(d, im.width, ttl)
    im.save(os.path.join(HERE, out), quality=92)

# --- 1: outside, looking down on one tunnel --------------------------------
def outside(d):
    ring(d, (203, 127), 16); badge(d, (150, 160), 1)                 # hole diameter
    line(d, (203, 127), (555, 122)); badge(d, (380, 95), 2)          # holes across
    line(d, (585, 122), (585, 492)); badge(d, (625, 300), 3)         # holes along
    line(d, (250, 250), (512, 250)); badge(d, (380, 220), 4)         # tunnel width
    line(d, (300, 62), (300, 462)); badge(d, (300, 410), 5)          # tunnel length
    line(d, (165, 400), (245, 400)); badge(d, (205, 365), 6)         # flange strip width
    line(d, (460, 62), (460, 690)); badge(d, (460, 600), 7)          # transom to wire hole
    ring(d, (380, 690), 34)
    # the line across the tunnel: check, not measure
    for col, ww in ((BLACK, 8), ((255, 80, 80), 4)):
        d.line([(255, 345), (505, 340)], fill=col, width=ww)
    badge(d, (530, 345), "A", col=(30, 120, 220))
make("20261009_101526.jpg", "1_outside_measure.jpg", "1  Outside: one tunnel, looking down", outside)

# --- 2: the transom notch ----------------------------------------------------
def transom(d):
    line(d, (192, 440), (470, 440)); badge(d, (330, 405), 8)         # notch width
    line(d, (330, 440), (330, 498)); badge(d, (372, 470), 9)         # notch depth
    note(d, (40, 560), "8  width of the notch at the top edge", 21)
    note(d, (40, 595), "9  depth: straight edge across, measure down", 21)
make("20261009_101559.jpg", "2_transom_measure.jpg", "2  Transom: where the tunnel comes out", transom)

# --- 3: inside the hull --------------------------------------------------------
def inside(d):
    line(d, (462, 420), (522, 420)); badge(d, (492, 385), 10)        # inside strip width
    line(d, (545, 248), (545, 648)); badge(d, (585, 450), 11)        # inside strip length
    ring(d, (493, 268), 22); badge(d, (548, 238), 12)                # pin
    ring(d, (350, 850), 75); badge(d, (455, 800), 13)                # wall thickness at hole
    for col, ww in ((BLACK, 8), ((255, 80, 80), 4)):
        d.line([(232, 485), (462, 495)], fill=col, width=ww)
    badge(d, (210, 470), "A", col=(30, 120, 220))
make("20261009_101828.jpg", "3_inside_measure.jpg", "3  Inside the hull, same tunnel", inside)

# --- 4: the thruster from the front ---------------------------------------------
def thruster(d):
    line(d, (64, 228), (546, 228)); badge(d, (305, 195), 14)         # duct outside dia
    line(d, (372, 447), (372, 505)); badge(d, (412, 476), 15)        # foot height
    line(d, (290, 530), (346, 530)); badge(d, (318, 565), 16)        # foot width
make("20261009_101755.jpg", "4_thruster_measure.jpg", "4  Thruster from the front", thruster)
print("written to", HERE)

# --- 6: follow-up questions (2026-10-09) -----------------------------------------
def followup_inside(d):
    ring(d, (493, 268), 22); badge(d, (548, 238), 21)    # boss diameter
    line(d, (515, 255), (515, 300)); badge(d, (600, 285), 22)   # boss height
    ring(d, (186, 598), 18); badge(d, (130, 600), 23)    # the screw
    note(d, (30, 700), "21  diameter of the post", 21)
    note(d, (30, 735), "22  height of the post above the flat strip", 21)
    note(d, (30, 770), "Is the TOP of the post closed (solid)?", 21)
    note(d, (30, 805), "23  this screw: what size, and what does it hold?", 21)
make("20261009_101828.jpg", "6_followup_inside.jpg", "6  Follow-up: the posts inside", followup_inside)

def followup_outside(d):
    line(d, (612, 62), (612, 127)); badge(d, (655, 95), 20)    # transom to first holes
    ring(d, (555, 122), 16)
    note(d, (60, 860), "20  transom edge to the centre of the first two holes", 21)
make("20261009_101526.jpg", "7_followup_outside.jpg", "7  Follow-up: where the holes start", followup_outside)
