// ===========================================================================
// trim_tab.scad — CENTRE TRIM TAB for the D007's transom, bolt-on, no new holes
// in the hull. Print the angle ladder: 0°, 5°, 10° (plus the fit gauge first).
// ---------------------------------------------------------------------------
// WHY (2026-10-20 pool runs, docs/03): near hull speed (~1 m/s) the nose
// climbs: loaded 15° at the MOT_THR_MAX 50 limit. A plate sticking out behind
// the transom with its trailing edge angled down gets pushed UP by the water,
// lifting the stern and lowering the nose. Honest expectation (Claude,
// 2026-10-20): small at 1 m/s, because lift grows with speed squared; roughly
// 10-15 % of the nose-up push at 10°. A cheap bolt-on test, nothing unsealed.
//
// WHERE: the centre section between the two v2 mount bases (90 mm wide). The
// ducts fill the rest of the 230 mm transom, and a plate behind a duct would
// sit in its jet.
//
// SHAPE (Cobus, 2026-10-20; VERIFY with part = "gauge"): the centre section is
// a shallow V. The v2 bases' underside is 4 mm DEEPER than the V's edges (first
// read the other way round from his sketch); the keel line is 12 mm deeper than
// the edges, so 8 mm below the bases' underside.
//
//   seen from behind, water BELOW:
//      hull ═══╗╲_______________╱╔═══ hull        V edges: z = +4
//      base ███║ ╲             ╱ ║███ base        base underside: z = 0
//      ear  ▓▓▓▓  ╲   centre  ╱  ▓▓▓▓ ear  (post screw UP through it)
//                  ╲_________╱  tab hugs the V, 3 mm thick; keel z = -8
//
// FIXING (Cobus, 2026-10-20): two ears reach sideways under the inboard edge of
// each base and sit under that base's EXISTING inboard aft post screw (12 mm
// forward of the transom; holes 99.5 mm apart, found with the fit gauge). Take the
// screw out, fit the tab, put the screw back through the ear. Nothing new goes
// into the hull or the base. The 4 mm ear moves the head 3.5 mm down, so an
// ST2.9 x 13 keeps ~4.5 mm in the post: fine for a pool test; x 16 to keep it on.
//
// Model axes: X across (0 = keel line), Y forward from the transom (0 = transom
// edge, negative = behind the boat), Z up (0 = the bases' underside; the water
// is below). Units mm.
//
//   openscad -D 'part="tab"' -D angle=5 -o stl/trim_tab_05.stl trim_tab.scad
//   part = "tab" | "gauge" | "assembly"
// Print: ASA or ABS, top face (the one that hugs the hull) on the bed, which
// needs a little support under the V; or print the gauge first and check.
// ===========================================================================

part  = "tab";
angle = 5;          // trailing edge down, degrees. Ladder: 0, 5, 10

// --- the hull's centre section at the transom (VERIFY) ------------------------
gap     = 90;       // Cobus #3: between the two bases
edge_z  = 4;        // Cobus 2026-10-20: the V's edges are 4 mm ABOVE (shallower than) the bases' underside
keel_z  = -8;       // keel line: 12 mm below the edges (Cobus's sketch), so 8 below the bases

// --- the tab ------------------------------------------------------------------
t       = 3;        // plate thickness
fwd     = 20;       // under the hull, forward of the transom (seats the V; matches the ears)
aft     = 35;       // sticks out behind the transom
te_r    = 1.0;      // trailing edge round (approx, by chamfer)

// --- ears and screws ----------------------------------------------------------
ear_w   = 10;       // sideways under each base
ear_t   = 4;        // ear thickness under the base
edge_cut = 1;       // Cobus, 2026-10-20 (fit gauge): plate edges 1 mm further in on both
                    // sides, so they clear the base's inboard face (cut above the ears only)
ramp_w  = 10;       // the ramp joining the plate edge (z +1..+4) to the ear (z -4..0) starts this far in
ear_l   = 20;       // forward from the transom (the post screw sits at 12)
screw_x = gap / 2 + 4.75; // screw centre from the keel line. Cobus, 2026-10-20 (fit gauge):
                          // holes 1 mm, then another 0.5 mm, further apart than first
                          // drawn (was + 4): 99.5 mm centre to centre
screw_y = 12;            // forward of the transom. Cobus, 2026-10-20: the ears go on the bases'
                         // EXISTING inboard post screws (no new holes), 12 mm forward
screw_d = 3.2;           // clearance for ST2.9 / M3
head_d  = 6.2;  head_h = 2.5;   // pan head pocket from below, 1.5 mm floor left in the 4 mm ear
// the v2 base: duct right under it (tunnel centre 81 mm out, duct OD 74),
// inboard post screw at 51.5 across, 12 forward (base 72 wide, post_x 29.5)
tun_x   = gap / 2 + 36;
post_xy = [tun_x - 29.5, 12];
duct_r  = 37;

$fn = 48;
half = gap / 2;
function vz(x) = edge_z - (edge_z - keel_z) * (1 - abs(x) / half);   // hull surface

// --- checks -------------------------------------------------------------------
assert(angle >= 0 && angle <= 15, "angle 0-15");
// The ear screw IS the base's inboard aft post screw. Its head moves from 2 mm
// up inside the base to 1.5 mm below the base's underside: 3.5 mm less in the
// post (ST2.9 x 13: ~4.5 mm left; x 16: ~7.5).
duct_top = -duct_r + sqrt(max(duct_r * duct_r - pow(tun_x - (half + ear_w), 2), 0));   // at the ear's outer edge
ear_bottom = -ear_t;
assert(ear_bottom - duct_top >= 2, str("ear too close to the duct: ", ear_bottom - duct_top, " mm"));
echo(str("Tab ", angle, "°: trailing edge ", aft * sin(angle), " mm lower than at the transom; ",
         "ear to duct clearance ", ear_bottom - duct_top, " mm."));

// one half of the V as an (x, z) profile, 3 mm thick below the hull surface
module half_profile(s) {   // s = +1 / -1 side
    polygon([[0, vz(0)], [s * half, vz(half)], [s * half, vz(half) - t], [0, vz(0) - t]]);
}
module slab(y0, y1, s) { translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0) half_profile(s); }
module tilt() { rotate([angle, 0, 0]) children(); }   // about the transom line: aft end goes DOWN

module tab() {
    difference() {
        union() {
            for (s = [-1, 1]) {
                slab(0, fwd, s);                                   // seats on the V under the hull
                hull() { slab(-0.01, 0, s); tilt() slab(-aft, -aft + 0.01, s); }   // the tab itself
                // ear: out under the base, top flat on the base's underside
                translate([s > 0 ? half : -half - ear_w, 0, -ear_t]) cube([ear_w, ear_l, ear_t]);
                // join: the V's edge is 4 mm higher than the base's underside, so the
                // plate and the ear don't touch. A smooth ramp under the plate edge
                // (from ramp_w in, down to the ear) bridges them: no square stub
                // (Cobus, 2026-10-20: the first block showed as a step).
                hull() {
                    translate([s * (half - ramp_w), 0, vz(half - ramp_w) - t]) rotate([-90, 0, 0]) cylinder(d = 0.01, h = ear_l);
                    translate([s > 0 ? half - 0.01 : -half, 0, -ear_t]) cube([0.01, ear_l, edge_z + ear_t]);
                    translate([s * (half - ramp_w), 0, vz(half - ramp_w) - 0.01]) rotate([-90, 0, 0]) cylinder(d = 0.01, h = ear_l);
                }
            }
        }
        // plate edges 1 mm in: cut everything above the ears' top in the last mm
        for (s = [-1, 1]) translate([s > 0 ? half - edge_cut : -half - 5, -aft - 5, 0]) cube([edge_cut + 5, aft + fwd + 10, 20]);
        // ear screws, up into the base, pan head pocket from below
        for (s = [-1, 1]) translate([s * screw_x, screw_y, 0]) {
            translate([0, 0, -20]) cylinder(d = screw_d, h = 25);
            translate([0, 0, -ear_t - 1]) cylinder(d = head_d, h = head_h + 1);
        }
    }
}

// thin V gauge: 2 mm slice of the forward part + ears, to check the hull's V and the
// ear holes before printing the tabs
module gauge() {
    intersection() { tab(); translate([-100, 0, -50]) cube([200, ear_l, 60]); }
}

module dummy() {   // hull centre section, bases, ducts: for the assembly render
    color("DimGray", 0.5) translate([0, 60, 0]) rotate([90, 0, 0])
        linear_extrude(60, center = false) polygon([[-half, vz(half)], [0, vz(0)], [half, vz(half)], [half, 14], [-half, 14]]);
    for (s = [-1, 1]) {
        color("SteelBlue", 0.7) translate([s > 0 ? half : -half - 72, 0, 0]) cube([72, 80, 7]);
        color("YellowGreen", 0.5) translate([s * tun_x, 0, -duct_r]) rotate([-90, 0, 0]) difference() { cylinder(r = duct_r, h = 75); translate([0, 0, -1]) cylinder(r = duct_r - 3, h = 77); }
    }
}

if (part == "tab")           rotate([180, 0, 0]) tab();           // hull face on the bed
else if (part == "gauge")    rotate([180, 0, 0]) gauge();
else if (part == "assembly") { color("DarkOrange") tab(); dummy(); }
