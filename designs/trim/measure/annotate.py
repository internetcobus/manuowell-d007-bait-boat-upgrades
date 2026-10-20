# Labels copies of Cobus's 2026-10-20 stern photos (boat upside down on its
# stand) for the nose-down work. Never overwrites an existing output.
#   python3 annotate.py
import os
from PIL import Image, ImageDraw, ImageFont
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
B = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
YEL, RED, BLU, GRN, WHITE, BLACK = (255, 214, 0), (230, 40, 40), (40, 120, 230), (30, 170, 70), (255, 255, 255), (0, 0, 0)

def label(d, xy, text, col=WHITE, bg=BLACK, size=18):
    x, y = xy; b = d.multiline_textbbox((x, y), text, font=B(size), spacing=3)
    d.rounded_rectangle((b[0] - 6, b[1] - 4, b[2] + 6, b[3] + 4), 5, fill=bg)
    d.multiline_text((x, y), text, fill=col, font=B(size), spacing=3)

def badge(d, xy, n, col=YEL):
    x, y = xy; d.ellipse((x - 15, y - 15, x + 15, y + 15), fill=col, outline=BLACK, width=2)
    d.text((x, y), str(n), fill=BLACK, font=B(18), anchor='mm')

def arrow(d, a, b, col, w=5):
    d.line((a, b), fill=col, width=w)
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (-0.5, 0.5):
        d.line((b, (b[0] - 18 * math.cos(ang + s), b[1] - 18 * math.sin(ang + s))), fill=col, width=w)

def side(out):
    im = Image.open('photo_side_cobus.jpg').convert('RGB')
    W, H = im.size; im = im.resize((W, H + 230)); im.paste(Image.open('photo_side_cobus.jpg'), (0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, H, W, H + 230), fill=WHITE)
    label(d, (20, 20), 'UPSIDE DOWN: hull bottom on top', YEL)
    label(d, (110, 330), 'BOW', YEL); label(d, (860, 330), 'STERN', YEL)
    # thrust line (below the hull in the water = above it in this photo)
    arrow(d, (930, 235), (700, 235), RED)
    label(d, (520, 150), 'thrust line: low, well "below"\nthe boat\'s centre of gravity', RED, size=15)
    # bow-up moment
    d.arc((380, 260, 640, 520), 200, 330, fill=RED, width=5)
    label(d, (330, 450), 'thrust below the centre of\ngravity tips the NOSE UP', RED, size=15)
    badge(d, (950, 290), 1)
    d.text((20, H + 12), 'Idea A  thruster tilt: rear end of each duct a few degrees DEEPER than its front (in the water).', fill=BLACK, font=B(17))
    d.text((20, H + 40), '        The jet then pushes back AND down: the stern lifts, the nose drops. Built into a new carrier', fill=BLACK, font=F(16))
    d.text((20, H + 62), '        (ours, designs/thruster-mount), printed as a ladder: 0°, 3°, 6°.', fill=BLACK, font=F(16))
    d.text((20, H + 96), 'Idea B  trim tabs at the transom edge (badge 1): plates sticking out behind the hull bottom,', fill=BLACK, font=B(17))
    d.text((20, H + 124), '        trailing edge angled down. Water pressure under them lifts the stern.', fill=BLACK, font=F(16))
    d.text((20, H + 160), 'Both are modest at ~1 m/s (lift grows with speed squared), so we test them the same way in the pool', fill=(90, 90, 90), font=F(15))
    d.text((20, H + 182), 'and keep what measurably lowers the nose at MOT_THR_MAX 50.', fill=(90, 90, 90), font=F(15))
    im.save(out)

def stern(out):
    src = Image.open('photo_stern_cobus.jpg').convert('RGB'); W, H = src.size
    im = Image.new('RGB', (W, H + 230), WHITE); im.paste(src, (0, 0)); d = ImageDraw.Draw(im)
    label(d, (20, 20), 'UPSIDE DOWN, from behind', YEL)
    # transom bottom edge: where the grey mount bases meet the black transom face
    d.line((85, 470, 800, 470), fill=YEL, width=4); badge(d, (60, 470), 2)
    # centre gap between the two bases
    d.line((330, 420, 560, 420), fill=BLU, width=4); badge(d, (445, 395), 3, (120, 180, 255))
    # duct depth below the base
    d.line((40, 440, 40, 175), fill=GRN, width=4); badge(d, (40, 150), 4, (120, 230, 140))
    label(d, (600, 20), 'grey = our v2 mount bases\n(flat, reach the transom)', WHITE, size=15)
    d.text((20, H + 10), 'Please measure (mm):', fill=BLACK, font=B(18))
    rows = ['1  side photo: how far the duct\'s rear end sits ahead of (or past) the transom',
            '2  width of the transom along its bottom edge (yellow), side to side',
            '3  width of the centre part between the two grey bases (blue)',
            '4  how far the duct hangs below the grey base (green), top of duct to base',
            '5  what the wooden strip along the keel is (photos 4 and 5): keel guard, or a marker?']
    for i, t in enumerate(rows): d.text((30, H + 44 + i * 34), t, fill=BLACK, font=F(17))
    im.save(out)

for fn, out in ((side, 'side_annotated.jpg'), (stern, 'stern_annotated.jpg')):
    if os.path.exists(out): print('exists, skipped:', out)
    else: fn(out); print('wrote', out)
