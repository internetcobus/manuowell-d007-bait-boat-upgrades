// ===========================================================================
// thruster_mount.scad — pylon that hangs a 62 mm brushless thruster from the
// D007's STOCK motor-post hole (one per side; the part is symmetric)
// ---------------------------------------------------------------------------
// HOW IT WORKS (2026-10-08): the stock 390 pods hang on an 11 mm threaded post
// through the hull, with their wires inside it. This keeps that hole and that
// idea, but the post is a STEEL hollow M10 x 1 lamp tube, not plastic:
//
//   inside hull    inner nut + washer + rubber washer
//   ═══════════════╪═════════════  hull, existing 11 mm hole
//                  │  sealant ring on this part's top face seals the hole
//              ┌───┴───┐
//              │ pylon │  this part; the tube threads into a CAPTURED nut
//              └─┬───┬─┘  at its bottom, the wires leave through a side slot
//           ╭────┴───┴────╮
//           │  thruster   │  2 screws, 40 mm apart, heads inside the pylon
//           ╰─────────────╯
//
// THE THRUSTER'S HOLES (Cobus, 2026-10-08): THREE 3 mm holes in a straight line
// along the top of the thruster, 20 mm apart. The middle one sits right under
// the tube, so this uses the OUTER PAIR (40 mm apart) and leaves the middle
// one free. The wider pair also resists the thrust better than 20 mm would.
//
// WHY STEEL: about 1.7 kg of thrust per side bends the post where it meets the
// hull. A printed 11 mm tube would sit near 7 MPa there, close to where printed
// layers part, and the load repeats every run. A steel tube shrugs it off.
//
// ANTI-ROTATION: a single post lets the pylon twist, which would swing the
// thrust line and fight the skid steering. Clamping friction plus a bead of
// marine sealant (e.g. Sikaflex) on the top face is the plan. If a pylon still
// turns, add a locating pin (pin_d > 0), which costs one small new hole.
//
// 🚨 VALUES MARKED "VERIFY" ARE ASSUMPTIONS. Nothing here has been measured on
// the boat yet. Print part = "fit_bottom" and "fit_top" (a few grams each)
// and check them before printing a full pylon.
//
//   part = "mount" | "fit_bottom" | "fit_top" | "all"
//   "mount"      one pylon, print orientation (thruster face on the bed)
//   "fit_bottom" bottom slice: the 20 mm screw pair, captured nut, tube thread
//   "fit_top"    top slice: the hull face, to check it sits flat on the hull
//   "all"        pylon on a dummy thruster, for a visual check (not to print)
//
// Print: ASA (PLA softens at 55-60 °C, which a dark hull in the sun reaches),
// 4+ walls, 40 %+ infill. Thruster face DOWN on the bed, as modelled.
// Units: millimetres. Origin: centre of the tube on the thruster face; +X is
// the thrust axis, +Z goes up towards the hull.
// ===========================================================================

part = "mount";

/* [Pylon body] */
// Long enough to reach the outer screw pair (+-20 mm). The stock pod's saddle
// is only 35 mm, so VERIFY there is 50 mm of flat hull at each post hole.
body_len = 50.0;     // along the thrust axis
body_w   = 18.0;     // across; the ends are full radius, so it stays streamlined
// Gap between hull and duct. The stock post shows ~9 mm of post below the hull
// (37 mm tall, 28 mm of it threaded). This needs more to fit the screw heads,
// the captured nut and the wire exit above each other; see the checks below.
drop     = 15.0;

/* [Steel tube — M10 x 1 hollow lamp tube (VERIFY your tube and nut)] */
tube_od    = 10.0;
tube_clear = 0.4;    // bore = 10.4: the tube slides in, the NUT does the holding
nut_af     = 13.0;   // VERIFY: M10 x 1 lamp nuts are commonly 13-14 mm across flats
nut_h      = 3.0;    // VERIFY: lamp nuts are thin, ~3 mm
nut_clear  = 0.3;    // press-fit-ish, so the nut can't spin when the tube is turned

/* [Thruster interface] */
hole_pitch  = 20.0;  // the thruster's three holes, in a line along the thrust axis
screw_xs    = [-hole_pitch, hole_pitch];   // outer pair; the middle hole is under the tube
// VERIFY: the holes measure 3 mm. A tapped M3 hole measures about 2.5 mm
// (3 mm only across the thread crests), so check whether they are threaded
// M3 or plain holes for self-tappers before buying screws.
screw_d     = 3.3;   // M3 clearance through the pylon
head_d      = 6.0;   // M3 socket head 5.5 + clearance
pad_t       = 4.0;   // plastic under the screw heads; the screw's grip length

/* [Wire exit] */
wire_w = 6.0;        // three motor wires leave the tube bore sideways (-Y)
wire_h = 6.0;

/* [Hull face seal] */
// Sealed with a ring of marine sealant on this face around the tube, plus the
// rubber washer under the inner nut. The same sealant stops the pylon
// twisting. (An O-ring groove would now fit; sealant is kept because it also
// does the anti-rotation and copes with a hull that isn't perfectly flat.)
seal_ring_r = hole_pitch - head_d / 2;   // sealant must stay inside this

/* [Optional locating pin, 0 = none] */
pin_d   = 0;         // e.g. 3.2 for an M3 / 3 mm steel pin
pin_x   = 10.0;      // distance from the tube, along the thrust axis
pin_len = 4.0;       // how far it pokes up into the hull

/* [Hull, for the tube-length sum only] */
hull_t     = 3.0;    // VERIFY: hull wall at the post hole
inner_pack = 6.0;    // inner nut 3 + steel washer 1 + rubber washer 2
thread_spare = 3.0;  // thread left showing above the inner nut

/* [Dummy thruster, for "all" only] */
duct_id = 62.0;      // measured 2026-10-08 (duct opening)
duct_od = 68.0;      // VERIFY: assumes ~3 mm walls
duct_len = 75.0;

$fn = 96;

// --- derived ----------------------------------------------------------------
H        = drop;
bore_d   = tube_od + tube_clear;
nut_d    = (nut_af + nut_clear) / cos(30);   // across corners of the pocket
tube_len = H + hull_t + inner_pack + thread_spare;

// --- checks -----------------------------------------------------------------
// The captured nut must not cut into the screw holes.
assert(nut_d / 2 < hole_pitch - screw_d / 2,
       "nut pocket breaks into the screw holes");
// The screw-head pockets must leave a wall against the tube bore.
assert(hole_pitch - head_d / 2 - bore_d / 2 >= 1.5,
       "less than 1.5 mm of wall between the screw heads and the tube bore");
// Screw heads, the nut and the wire exit stack up; they must fit inside drop.
assert(H >= max(pad_t, nut_h) + wire_h + 2,
       "drop too small for the screw pad / captured nut + wire exit");
// The sealant ring needs a usable width between the tube and the head pockets.
assert(seal_ring_r - bore_d / 2 >= 1.5, "no room for a sealant ring around the tube");
// The screws must fall inside the footprint, with wall to spare.
assert(hole_pitch + head_d / 2 < body_len / 2 - 1.5,
       "screw heads too close to the pylon's ends");

echo(str("Cut each steel tube to ", tube_len, " mm (drop ", H, " + hull ", hull_t,
         " + inner nut/washers ", inner_pack, " + spare ", thread_spare, ")."));
echo(str("Thruster axis sits ", H + duct_od / 2, " mm below the hull (VERIFY duct_od)."));

// --- geometry ---------------------------------------------------------------
module footprint(h) {
    hull() for (s = [-1, 1])
        translate([s * (body_len - body_w) / 2, 0, 0]) cylinder(d = body_w, h = h);
}

module mount() {
    difference() {
        union() {
            footprint(H);
            if (pin_d > 0)
                translate([pin_x, 0, H - 0.01]) cylinder(d = pin_d, h = pin_len);
        }
        // tube bore, full height
        translate([0, 0, -1]) cylinder(d = bore_d, h = H + 2);
        // captured nut, opening onto the thruster face
        translate([0, 0, -1]) rotate([0, 0, 30])
            cylinder(d = nut_d, h = nut_h + 1, $fn = 6);
        // outer pair of thruster screws: clearance through the pad, head pockets above
        for (x = screw_xs) translate([x, 0, 0]) {
            translate([0, 0, -1]) cylinder(d = screw_d, h = pad_t + 2);
            translate([0, 0, pad_t]) cylinder(d = head_d, h = H);
        }
        // wire exit: from the bore out of the -Y side, just above the nut
        translate([-wire_w / 2, -body_w, nut_h])
            cube([wire_w, body_w, wire_h]);
    }
}

module dummy_thruster() {
    color("grey", 0.5)
    translate([-duct_len / 2, 0, -duct_od / 2]) rotate([0, 90, 0])
        difference() {
            cylinder(d = duct_od, h = duct_len);
            translate([0, 0, -1]) cylinder(d = duct_id, h = duct_len + 2);
        }
}

fit_bottom_h = max(pad_t, nut_h) + 2;
fit_top_h    = 4.0;

if (part == "mount") mount();
else if (part == "fit_bottom")
    intersection() { mount(); translate([-50, -50, -1]) cube([100, 100, fit_bottom_h + 1]); }
else if (part == "fit_top")
    // the top slice, dropped onto the bed; hull face up
    translate([0, 0, fit_top_h]) intersection() {
        translate([0, 0, -H]) mount();
        translate([-50, -50, -fit_top_h]) cube([100, 100, fit_top_h + pin_len + 1]);
    }
else {
    mount();
    dummy_thruster();
    color("silver") translate([0, 0, 0]) cylinder(d = tube_od, h = tube_len);
}
