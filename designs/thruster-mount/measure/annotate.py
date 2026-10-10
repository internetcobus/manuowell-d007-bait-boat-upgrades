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

# --- 11: the corner the template catches on (Cobus, 2026-10-10) ------------------
# Drawn on Cobus's own photo (his red circle stays). 658 x 909 px.
def corner(d):
    line(d, (110, 497), (110, 520)); badge(d, (70, 505), 24)        # step height
    line(d, (612, 52), (612, 497)); badge(d, (640, 280), 25)        # transom to the step
    ring(d, (470, 498), 14); badge(d, (520, 470), 26)               # the other side
    note(d, (20, 660), "24  how high is the step at the end of the strip?", 18)
    note(d, (20, 692), "25  transom edge to that step", 18)
    note(d, (20, 724), "26  same step on this side? (yes / no)", 18)
make("20261010_catches_corner_cobus.png", "11_corner_step.jpg", "11  The step the template catches on", corner)

# --- 12: the dovetail test piece in the transom notch (Cobus, 2026-10-10) ---------
# His photo is 4000 x 3000; drawn at full size, marks scaled up.
def gap(d):
    def big_ring(c, r, n, off):
        for col, ww in ((BLACK, 14), (YEL, 8)):
            d.ellipse([c[0]-r, c[1]-r, c[0]+r, c[1]+r], outline=col, width=ww)
        x, y = c[0]+off[0], c[1]+off[1]; R = 42
        d.ellipse([x-R-4, y-R-4, x+R+4, y+R+4], fill=WHITE); d.ellipse([x-R, y-R, x+R, y+R], fill=(30,120,220))
        d.text((x, y), n, font=font(46), fill=WHITE, anchor="mm")
    big_ring((2700, 1010), 170, "G1", (230, -120))      # right slope: the clearest gap
    big_ring((2000, 1235), 140, "G2", (0, 210))         # bottom of the curve
    big_ring((1100, 960), 150, "G3", (-230, 60))        # left slope
    big_ring((3150, 850), 120, "G4", (170, 150))        # under the right wing
    for i, t in enumerate(["G1  right slope: the clearest gap I can see",
                           "G2  the bottom of the curve",
                           "G3  left slope: reflections, hard to read",
                           "G4  under the right wing: a light line. Gap, or the rounded edge?"]):
        note(d, (80, 1700 + i*80), t, 48)
make("20261010_dovetail_gap.jpg", "12_dovetail_gap.jpg", "12  Where I see the gap", gap)
