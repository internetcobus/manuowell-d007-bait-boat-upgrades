// ===========================================================================
// thruster_mount_v2.scad — BASE + CARRIER that hang a 62 mm ducted thruster in
// the D007's moulded motor tunnel, using the hull's 4 EXISTING screw posts
// ---------------------------------------------------------------------------
// WHY v2 (2026-10-09): with the stock pods off, each motor position turned out
// to have a moulded tunnel in the hull bottom (43 wide, 10 deep, 69 long),
// flat 9 mm strips either side, and 4 SOLID posts inside (6.2 dia, 14.5 tall)
// that the stock motor shield screwed into from outside (2 mm pilot holes,
// ST2 x 7). The posts are closed, so the hull is already sealed there: no new
// holes, no through-bolts, no backing plate. v1 (a pylon on a lamp tube
// through the old post hole) is shelved.
//
// TWO PARTS, because the thruster's oval openings are closed: nothing can
// reach the foot screws from below, and the duct covers the post screws.
//
//   inside hull    posts (existing)
//   ═══════╪═══════╭─────╮═══════╪═══════  hull, tunnel in the middle
//      ST2.9 x 13  │BASE │  ST2.9 x 13     BASE: fills the tunnel, screws to
//   ───────┴───────┤╲   ╱├───────┴───────  the 4 posts, DROP below the hull
//                  │CARRIER               CARRIER: dovetail bar, slides in
//                  └──┬──┘                 from the stern, foot bolted in
//                  ╭──┴───────╮            with 3 x M4 from its top
//                  │ thruster │
//
//   1  Screw the BASE to the 4 posts, from outside, thruster OFF.
//   2  On the bench, bolt the thruster's foot into the CARRIER: 3 x M4
//      countersunk, down through the carrier's top. Tap the foot's 3 mm holes
//      M4 (3.3 mm drill), to their EXISTING depth. Never drill through: the
//      foot sits on the duct and a bolt end would hit the propeller.
//   3  Slide the carrier into the base from the stern until it stops (forward
//      thrust pushes it into the stop). Fit the side LOCK screw, M3 x 40, from
//      the outboard side; its nut sits in a slot in the carrier.
//
// LOADS: about 1.7 kg thrust per side. With the thrust line ~45 mm below the
// hull and the posts 62 mm apart, each post screw sees only ~6 N. The screws
// are there for KNOCKS (rocks, landing it on the bank), which is why they are
// 2.9 x 13, not the shield's 2 x 7: grip depth in the post is what counts.
// Bed the base in thickened epoxy (or ABS cement, the hull is ABS) to take a
// knock off the screws.
//
// 🚨 VALUES MARKED "VERIFY" ARE NOT MEASURED. Print part = "template" first
// (lay it on the hull: do the 4 holes land on the 4 pilot holes?) and
// "fit_dovetail" (does the carrier slide in with a light push?).
//
//   part = "base" | "carrier" | "template" | "fit_dovetail" | "all" | "none"
//          ("none" draws nothing: for check scripts that include this file)
//   side = "right" | "left"  the lock screw goes in from the OUTBOARD side, so
//          print one base + one carrier of each. "right" = screw at +X.
//
// Print: ABS or ASA (not PLA: sun + water), 4+ walls, 40 %+ infill. Both parts
// are already laid out for printing: the base on its flat underside, the
// carrier on its flat top. Units: mm.
// Model axes (part = "all"): X across the boat (0 = tunnel centreline),
// Y forward from the transom (0 = transom edge), Z up (0 = hull bottom).
// ===========================================================================

part = "all";
side = "right";

/* [Hull: Cobus's measurements, 2026-10-09 (designs/thruster-mount/measure)] */
tun_w   = 43;      // #4 / #8 tunnel width
tun_d   = 10;      // #9 tunnel depth at the transom
tun_l   = 69;      // #5 transom edge to where the tunnel steps up
strip_w = 9;       // #6 flat strip beside the tunnel
post_x  = 59 / 2;  // #2 posts 59 apart across
post_y1 = 12;      // #20 transom edge to the first pair
post_pitch = 62;   // #3 first pair to second pair
hull_t  = 3;       // #13
wire_y  = 111;     // #7 transom edge to the wire hole's centre
wire_d  = 11;      // VERIFY: the old post hole, ~11 mm
// The small rail across the tunnel (2 wide, 0.5 high, check "A"). Position is
// read off photo 1 by scale, so the groove is cut generously wide.
// Cobus, 2026-10-09: no groove needed. The rail is 0.5 high and the epoxy
// bed (bed_gap) takes it up; sand it down if the base rocks on a dry fit.
rail_groove = false;
rail_y  = 49;      // VERIFY: transom edge to the rail
rail_gw = 5;       // groove width (rail 2 + slack for the estimate)
rail_gd = 1.0;     // groove depth (rail 0.5 + slack)
// The strips are shallow POCKETS. On the INBOARD side of the tunnel (away
// from the hull's edge) the hull steps 4 mm proud at the strip's forward end;
// the template's corner caught on it (Cobus, 2026-10-10, measure/ #24-26).
// The outboard strip runs to the hull edge: no step there.
step_y     = 84;   // #25 transom edge to the step
step_h     = 4;    // #24 how far the hull forward of it stands proud
step_x0    = 18;   // VERIFY: where the raised area starts across. It begins at
                   // the tunnel's frame line (~21.5); 18 leaves a margin
step_clear = 0.5;  // (unused since the cut-out; kept for a relief variant)

/* [Thruster: measured] */
duct_l    = 75;    // spec
duct_od   = 74;    // #14 in the middle (67 at the edges)
foot_w    = 10;    // #16
foot_l    = 50;    // #17
hole1     = 14.5;  // #18 duct's front edge to the first foot hole
hole_pitch = 20;   // the three foot holes, front to back
// #15: the foot stands 8.5 above the duct at its ends but only 7 in the
// middle, because the duct bulges (67 -> 74). So the foot can only sink 7 mm
// before the duct's bulge touches the carrier; its ends stay 1.5 mm proud.
foot_sink = 7.0;
duct_aft  = 0;     // the duct's back edge, from the transom (0 = flush)

/* [Mount] */
drop     = 7;      // base underside below the hull = duct top below the hull.
                   // Clearance for water to reach the intake, and the depth
                   // the side lock screw and post-screw heads need.
wing     = 36;     // base half-width: posts at 29.5 + head pocket + wall
bed_gap  = 0.3;    // base top this far off the tunnel roof, for the epoxy
corner_r = 5;      // outline corners, seen from below
edge_r   = 2.5;    // round on the base's bottom edge, all the way round (the
                   // top edge stays square: it beds flat on the hull)

/* [Post screws: ST2.9 x 13 stainless pan head] */
ps_clear = 3.2;
ps_head  = 6.2;    // pan head ~5.6
ps_sink  = 2.0;    // head sunk this far into the base underside
// pilot: open the hull's 2 mm holes to 2.4 mm, ~12 mm deep (hull + post =
// 17.5, so 12 leaves the post's closed top intact). Try one post first.

/* [Carrier: dovetail bar] */
// The walls' slope sets how far the carrier SINKS for a given side gap:
// drop = clearance / ((car_tw - car_bw) / 2 / car_h). The first test print
// (18 / 22, 0.3 clearance) had walls only ~9 deg off vertical, so 0.3 a side
// let it sink ~2 mm: "play all round" (Cobus, 2026-10-10, PLA). 16 / 24
// doubles the slope; with 0.15 clearance the drop is ~0.5 mm.
car_bw   = 16;     // width at the bottom (open face); foot pocket 10.4 + 2.8 walls
car_tw   = 24;     // width at the top: wider, so it cannot drop out
min_skin = 1.2;    // least base plastic left above the carrier, under the roof
dv_clear = 0.15;   // slide clearance each side. VERIFY with the fit_dovetail
                   // ladder (0.10 / 0.15 / 0.20) printed in ABS
foot_clear = 0.2;
// M4 countersunk into the foot
m4_clear = 4.4;
m4_csk_d = 8.4;
m4_csk_h = 2.4;

/* [Side lock screw: M3 x 40 + nut] */
lock_y   = 6;      // in the 15 mm at the aft end where the carrier has no foot
lock_z   = -drop / 2;
lock_d   = 3.4;
lock_head = 6.2;
lock_cb  = 3.0;    // head counterbore into the base's side face
nut_af   = 5.5;  nut_t = 2.4;  nut_x = -4;   // nut slot, past the centreline

/* [Wire cover] */
cover_end_w = 10;  // half-width where the cover ends, just past the wire hole
groove_w = 6;      // wire channel in the base underside, carrier -> wire hole
groove_d = 4;

$fn = 64;

// --- derived ----------------------------------------------------------------
R       = tun_w * tun_w / (8 * tun_d) + tun_d / 2;     // tunnel arc radius ~28.1
function roof(x) = sqrt(max(R * R - x * x, 0)) - (R - tun_d);
car_h   = roof(car_tw / 2 + dv_clear) - min_skin - bed_gap + drop;   // to fit under the arc
car_top = -drop + car_h;
foot_y1 = duct_aft + duct_l - hole1 + 5;            // foot's front end
foot_y0 = foot_y1 - foot_l;
holes_y = [for (i = [0:2]) duct_aft + duct_l - hole1 - i * hole_pitch];
car_len = foot_y1 + foot_clear + 2.2;               // front wall 2.2 past the foot
base_len = post_y1 + post_pitch + 6;                // full width to past the 2nd posts
cover_y  = wire_y + wire_d / 2 + 4;
sx = (side == "right") ? 1 : -1;   // the outboard side (lock screw)
inb = -sx;                          // the inboard side (the step)
lock_len = wing - lock_cb + abs(nut_x) + 2;

// --- checks -----------------------------------------------------------------
assert(car_len < tun_l - 0.5, "carrier runs past the tunnel: it would hit the hull step");
above_foot = car_top - (-drop + foot_sink);
assert(above_foot >= 4, str("only ", above_foot, " mm of carrier above the foot for the M4 heads"));
assert(car_h > foot_sink + 4, "carrier too shallow for the foot + screw heads");
assert(foot_y0 - foot_clear > lock_y + lock_d / 2 + 2, "lock screw runs into the foot pocket");
assert(norm([post_x, post_y1] - [post_x, lock_y]) > ps_head / 2 + lock_d / 2 + 0.8,
       "lock screw too close to the first post screw");
assert(car_bw / 2 + dv_clear < tun_w / 2 - 2, "dovetail slot too close to the tunnel edge");
assert(wing - post_x - ps_head / 2 >= 2, "less than 2 mm of wing outside the post-screw heads");
assert(wing - edge_r >= post_x + ps_head / 2, "the bottom-edge round cuts into the post-screw head pockets");
assert(edge_r < drop / 2, "edge round too big for the base's thickness");
assert(post_y1 + post_pitch + ps_head / 2 + 2 < step_y - 1, "step relief runs into the forward post screws");
assert(lock_z - lock_d / 2 > -drop + 1 && lock_z + lock_d / 2 < -1,
       "lock screw too close to the base's faces: increase drop");

echo(str("Tunnel arc radius ", R, "; carrier ", car_bw, "-", car_tw, " wide x ", car_h,
         " tall x ", car_len, " long; ", above_foot, " mm above the foot."));
echo(str("Foot holes (M4) at ", holes_y, " mm from the transom. Duct top ", drop,
         " mm below the hull; thruster axis ", drop + duct_od / 2, " mm below."));
echo(str("Lock screw: M3 x ", ceil(lock_len / 5) * 5, " (needs ", lock_len, ")."));

// --- 2D helpers ---------------------------------------------------------------
// Tunnel fill across X (as X, Z), lowered by `down` (0 = bedded on the roof).
module fill_profile(down = 0) {
    n = 60;  hw = tun_w / 2 - bed_gap;
    polygon(concat([[-hw, 0]],
                   [for (i = [0:n]) let(x = -hw + 2 * hw * i / n) [x, max(roof(x) - bed_gap - down, 0)]],
                   [[hw, 0]]));
}
module dovetail_profile(c = 0, ext = 0) {   // as X, Z; c = clearance, ext = extend down
    polygon([[-(car_bw / 2 + c), -drop - ext], [car_bw / 2 + c, -drop - ext],
             [car_tw / 2 + c, car_top + c], [-(car_tw / 2 + c), car_top + c]]);
}
// Extrude an (X, Z) profile along +Y from y0 to y1.
module along_y(y0, y1) { translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0) children(); }

// Base outline seen from below (X, Y). The area over the inboard step is cut
// away altogether (Cobus, 2026-10-10): a cover there only trapped water and
// added drag, and it carries no load. Outer corners rounded corner_r, the
// inside corner of the cut-out rounded too.
module footprint() {
    offset(r = corner_r) offset(delta = -corner_r)
    offset(r = -corner_r) offset(delta = corner_r)
    difference() {
        footprint_sharp();
        step_zone_2d();
    }
}
module step_zone_2d() {
    x0 = (inb > 0) ? step_x0 : -(wing + 2);
    translate([x0, step_y - 1]) square([wing + 2 - step_x0, 200]);
}
module footprint_sharp() {
    polygon([[-wing, 0], [wing, 0], [wing, base_len], [cover_end_w, cover_y],
             [-cover_end_w, cover_y], [-wing, base_len]]);
}

// The part of the base below the hull: the outline, with its bottom edge
// rounded by a sphere and its top (hull) face left flat. The outline is
// convex, so this minkowski is quick.
module plate() {
    intersection() {
        minkowski() {
            translate([0, 0, -drop + edge_r]) linear_extrude(2 * drop) offset(delta = -edge_r) footprint();
            sphere(r = edge_r, $fn = 24);
        }
        translate([-wing - 1, -1, -drop]) cube([2 * wing + 2, cover_y + 2, drop]);   // keep the top flat
    }
}

// --- parts, in boat axes ---------------------------------------------------------
module base(c = dv_clear) {
    difference() {
        union() {
            plate();
            along_y(0, tun_l - 0.5) fill_profile();
        }
        // dovetail slot, open at the stern and underneath
        along_y(-1, car_len + c) dovetail_profile(c, 1);
        // 4 post screws: clearance + head pockets from below
        for (s = [-1, 1], y = [post_y1, post_y1 + post_pitch]) translate([s * post_x, y, 0]) {
            translate([0, 0, -drop - 1]) cylinder(d = ps_clear, h = drop + 2);
            translate([0, 0, -drop - 1]) cylinder(d = ps_head, h = ps_sink + 1);
        }
        // wire channel underneath, carrier front -> wire hole, then up through
        translate([-groove_w / 2, car_len + dv_clear - 0.01, -drop - 1]) cube([groove_w, wire_y - car_len, groove_d + 1]);
        translate([0, wire_y, -drop - 1]) cylinder(d = wire_d + 1, h = drop + 2);
        // groove over the rail across the tunnel roof
        // (the cut reaches above the part and stops 0.3 above Z = 0, so no faces
        // coincide: shared faces leave a paper-thin sliver in the print)
        if (rail_groove) along_y(rail_y - rail_gw / 2, rail_y + rail_gw / 2)
            intersection() {
                difference() { fill_profile(-2); fill_profile(rail_gd); }
                translate([-tun_w, 0.3]) square([2 * tun_w, tun_d + 5]);
            }
        // side lock screw from the outboard face, with a head counterbore
        translate([0, lock_y, lock_z]) rotate([0, sx * 90, 0]) {
            cylinder(d = lock_d, h = wing + 1);
            translate([0, 0, wing - lock_cb]) cylinder(d = lock_head, h = lock_cb + 1);
        }
    }
}

module carrier() {
    difference() {
        along_y(0, car_len) dovetail_profile();
        // foot pocket, open underneath
        translate([-(foot_w / 2 + foot_clear), foot_y0 - foot_clear, -drop - 1])
            cube([foot_w + 2 * foot_clear, foot_l + 2 * foot_clear, foot_sink + 1]);
        // 3 x M4 countersunk from the top into the foot
        for (y = holes_y) translate([0, y, -drop - 1]) {
            cylinder(d = m4_clear, h = car_h + 2);
            translate([0, 0, car_h + 1 - m4_csk_h]) cylinder(d1 = m4_clear, d2 = m4_csk_d, h = m4_csk_h + 0.01);
        }
        // lock screw through, and a slot from the top for its nut
        translate([0, lock_y, lock_z]) rotate([0, 90, 0]) cylinder(d = lock_d, h = 2 * car_tw, center = true);
        translate([sx * nut_x - nut_t / 2 - 0.15, lock_y - nut_af / 2 - 0.15, lock_z - nut_af / 2 - 0.15])
            cube([nut_t + 0.3, nut_af + 0.3, car_top - lock_z + nut_af / 2 + 1]);
    }
}

// The area forward of the inboard strip's end, where the hull stands proud.
module step_zone(z0, h) { translate([0, 0, z0]) linear_extrude(h) step_zone_2d(); }

// --- print layouts ----------------------------------------------------------------
module base_print(c = dv_clear) { translate([0, 0, drop]) base(c); }                       // underside on the bed
module carrier_print() { translate([0, 0, car_top]) rotate([0, 180, 0]) carrier(); }   // top on the bed

module template() {    // 1.2 mm flat plate: lay it on the hull, check the 4 holes
    difference() {
        linear_extrude(1.2) footprint();
        for (s = [-1, 1], y = [post_y1, post_y1 + post_pitch]) translate([s * post_x, y, -1]) cylinder(d = 2.2, h = 3);
        translate([-tun_w / 2, 0, -1]) cube([tun_w, tun_l, 3]);                   // window: the tunnel
        translate([0, wire_y, -1]) cylinder(d = wire_d, h = 3);                  // the wire hole
        translate([-wing + 3, rail_y - 0.5, 0.6]) cube([2 * wing - 6, 1, 1]);   // scribe line: the rail
        step_zone(-1, 3);                                                      // clear the inboard step
    }
}

// Clearance ladder: one 14 mm carrier slice and three 14 mm base slices
// (the middle 40 mm, around the slot), cut at 0.10 / 0.15 / 0.20 a side.
// The slices are marked with 1, 2 and 3 notches. Pick the one that slides with
// a light push and doesn't wobble, then set dv_clear to it.
fit_clears = [0.10, 0.15, 0.20];
module fit_dovetail() {
    for (i = [0:2]) translate([i * 46, 0, 0]) difference() {
        intersection() { base_print(fit_clears[i]); translate([-20, -1, -1]) cube([40, 15, 40]); }
        for (n = [0:i]) translate([-20 + 3 + n * 3.5, -0.01, -1]) cube([1.5, 2, 40]);   // notches = which clearance
    }
    translate([3 * 46, 0, 0]) intersection() { carrier_print(); translate([-50, -1, -1]) cube([100, 15, 40]); }
}

module dummy_hull() {
    color("DimGray", 0.6) difference() {
        translate([-60, -2, 0]) cube([120, 140, hull_t]);
        translate([-tun_w / 2, -3, -0.01]) cube([tun_w, tun_l + 3, hull_t + 1]);
    }
    // the raised area forward of the inboard strip (starts at the tunnel's frame line)
    color("DimGray", 0.6) intersection() {
        translate([(inb > 0) ? tun_w / 2 : -60, step_y, -step_h]) cube([60 - tun_w / 2, 138 - step_y, step_h]);
        translate([-60, -2, -step_h]) cube([120, 140, step_h]);
    }
    color("DimGray", 0.6) along_y(-2, tun_l) difference() {
        intersection() { offset(delta = hull_t) fill_profile(-bed_gap); translate([-60, 0]) square([120, 40]); }
        fill_profile(-bed_gap);
    }
}
module dummy_thruster() {
    color("YellowGreen", 0.7) {
        translate([0, duct_aft, -drop - duct_od / 2]) rotate([-90, 0, 0]) difference() {
            cylinder(d = duct_od, h = duct_l);
            translate([0, 0, -1]) cylinder(d = duct_od - 6, h = duct_l + 2);
        }
        translate([-foot_w / 2, foot_y0, -drop]) cube([foot_w, foot_l, foot_sink]);
    }
}

if      (part == "base")         base_print();
else if (part == "carrier")      carrier_print();
else if (part == "template")     template();
else if (part == "fit_dovetail") fit_dovetail();
else if (part == "all") {
    color("SteelBlue") base();
    color("MediumPurple") carrier();
    dummy_hull();
    dummy_thruster();
}
