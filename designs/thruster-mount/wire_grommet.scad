// ===========================================================================
// wire_grommet.scad — TPU plug for the motor-wire hole, fitted from INSIDE
// the hull. Print 2 (one per motor) in TPU-95.
// ---------------------------------------------------------------------------
// Cobus, 2026-10-16: the hole on the inside is about 11 mm and not perfectly
// round; each motor wire is 2 mm, but the bullet connectors are just over
// 5 mm, so the wires can't be threaded through 2 mm holes. Each wire hole has
// a SLIT to the edge: press the wires in sideways, then push the plug into the
// hole. The oversize body squeezes the slits shut. The grommet holds the wires
// and the sealant; the SEAL is a bead of marine sealant (Sikaflex 291i or
// another MS polymer, never vinegar-smelling silicone) over the flange inside,
// plus the base's wire pocket filled from outside.
//
//        wire  wire  wire
//   ╭────┼─────┼─────┼────╮   flange, inside the hull (print side down)
//   ╰──╮ │     │     │ ╭──╯
//      │ │     │     │ │      body in the hull hole, 0.6 over the hole
//       ╲│     │     │╱       lead-in taper
//
//   openscad -D 'part="plate"' -o v2/wire_grommet.stl wire_grommet.scad
// ===========================================================================

part = "plate";   // "plate" (2 grommets) | "one" | "ladder" (3 wire-hole sizes, v2/wire_grommet_ladder.stl)

hole_d   = 11.0;   // Cobus, 2026-10-16: inside of the hull hole, about 11
squeeze  = 1.0;    // body over the hole, so TPU fills an out-of-round hole.
                   // Cobus, 2026-10-16: of the first ladder (11.2 / 11.6 / 12.0,
                   // no wires in) the 12.0 fitted best
body_l   = 4.0;    // VERIFY: hull thickness at the hole (about 3); spare
                   // length goes into the base's 12 mm wire pocket below
taper_l  = 1.2;    // lead-in at the tip
taper_in = 0.8;    // tip is this much smaller in diameter
flange_d = 16;
flange_t = 1.2;    // thin, so it bends to the hull's inside face

wire_d   = 2.5;    // wires are 2.0. Was 1.8: Cobus, 2026-10-16, far too tight;
                   // after one wire the others would not go in (small holes
                   // print undersize in TPU). The sealant seals, not the hole.
                   // Second ladder (2.2 / 2.5 / 2.8): 2.5 fits perfectly (Cobus)
wire_r   = 2.6;    // wire-hole centres from the middle (holes 4.5 apart)
slit_w   = 0.5;    // pushed shut once the body is in the hole

$fn = 72;

body_d = hole_d + squeeze;

// --- checks -----------------------------------------------------------------
assert(2 * wire_r * sin(60) - wire_d >= 1.5, "wall between the wire holes too thin");
assert(body_d / 2 - taper_in / 2 - wire_r - wire_d / 2 >= 1.2,
       "wall outside the wire holes too thin at the tip");
assert(flange_d >= body_d + 3, "flange too small to stop the plug");

module grommet(wd = wire_d, marks = 0, bd = body_d) {
    difference() {
        union() {
            cylinder(d = flange_d, h = flange_t);
            cylinder(d = bd, h = flange_t + body_l - taper_l);
            translate([0, 0, flange_t + body_l - taper_l])
                cylinder(d1 = bd, d2 = bd - taper_in, h = taper_l);
        }
        for (a = [90, 210, 330]) rotate(a) {
            translate([wire_r, 0, -1]) cylinder(d = wd, h = flange_t + body_l + 2, $fn = 24);
            // slit from the wire hole out through the side
            translate([wire_r, -slit_w / 2, -1]) cube([flange_d, slit_w, flange_t + body_l + 2]);
        }
        // ladder marks: 1, 2 or 3 notches in the flange edge
        if (marks > 0) for (k = [0:marks - 1]) rotate(150 + k * 12)
            translate([flange_d / 2, 0, -1]) cylinder(d = 1.6, h = flange_t + 2, $fn = 16);
    }
}

if (part == "one") grommet();
if (part == "plate") for (x = [0, flange_d + 4]) translate([x, 0, 0]) grommet();
if (part == "ladder")   // wire holes 2.2 (1 notch), 2.5 (2), 2.8 (3), body 12.0
    for (i = [0:2]) translate([i * (flange_d + 4), 0, 0]) grommet(2.2 + i * 0.3, i + 1);
