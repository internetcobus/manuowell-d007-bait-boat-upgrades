// ===========================================================================
// thruster_tilt_carrier.scad — v2 CARRIER that holds the thruster TILTED:
// the duct's rear end sits deeper than its front, so the jet pushes back AND
// slightly down. That lifts the stern and lowers the nose.
// ---------------------------------------------------------------------------
// WHY (2026-10-20 pool runs, docs/03): past ~1 m/s the hull climbs its bow
// wave. Loaded with ~1 kg in the hoppers the nose reached 31° at 70-79 %
// throttle, 15° at the 50 % limit. The thrust line hangs ~45 mm below the hull,
// well under the centre of gravity, which tips the nose up the harder it
// drives. A few degrees of tilt counters part of that. Cost: thrust forward x
// cos(tilt), 99.5 % at 6°.
//
// Drop-in for the v2 carrier: same dovetail, lock screw and nut slot, same 3 x
// M4 countersunk into the foot. Only the foot pocket and its 3 holes are
// rotated about the foot's FRONT end, so the foot keeps its full 7 mm grip.
// Behind that pivot the foot sits lower than the base's underside, so a SHOE
// (a wedge under the carrier, 0 at the pivot, deepest at the stern end) holds
// it: about 3.4 mm deep at 3°, 6.9 mm at 6°. The shoe hangs under the base,
// between it and the duct, where the foot already is.
//
//   side view, stern on the left, water below:
//      base ══════════════════════════════
//      carrier ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔╲   pivot (foot front)
//      shoe     ╲▁▁▁▁▁▁foot▁▁▁▁▁▁▁▁▁▁▁▁▁▁╲
//              duct rear lower ↘  ↗ front
//
// CHOSEN: 8° (Cobus, 2026-10-20): one unseal only, so one tilt, not a ladder.
// 8° over 6° for more nose-down push if MOT_THR_MAX goes up later; not 10°, so
// the empty boat does not run bow-down on the way back.
// (Originally a LADDER for the pool test: print tilt 3 and 6, one left
// and one right of each. The existing v2 carriers are the 0° pair. Swap a
// pair, run the same 50 % pool runs loaded and empty, compare the nose angle.
//
//   openscad -D tilt=6 -D side='"right"' -o v2/v2_carrier_tilt6_right.stl thruster_tilt_carrier.scad
//   (tilt_part = "carrier" | "assembly" for a render with the dummy duct)
//
// Print like the v2 carrier: ABS or ASA, flat top on the bed, 4+ walls, 40 %+.
// ===========================================================================

include <thruster_mount_v2.scad>
part = "none";              // the v2 file draws nothing; this file draws below

tilt = 6;                    // degrees, rear end down. Ladder: 3, 6
tilt_part = "carrier";

pivot_y = foot_y1 + foot_clear;         // the foot's front end (with its clearance)
pivot_z = -drop;                        // on the base's underside
shoe_d  = pivot_y * tan(tilt);          // shoe depth at the stern end of the carrier
duct_drop_rear = pivot_y * sin(tilt);   // how much deeper the duct's rear rim sits (it rotates about the foot front)

assert(tilt >= 0 && tilt <= 8, "tilt outside 0-8°: the shoe gets deep and the jet hits the hull bottom less cleanly");
assert(car_len > pivot_y, "carrier must reach past the pivot");
echo(str("Tilt ", tilt, "°: shoe ", shoe_d, " mm deep at the stern end; duct rear about ",
         duct_drop_rear, " mm deeper; forward thrust x ", cos(tilt)));

module tilted() { translate([0, pivot_y, pivot_z]) rotate([tilt, 0, 0]) translate([0, -pivot_y, -pivot_z]) children(); }

// The wedge under the carrier: car_bw wide, from the base's underside down to
// the tilted plane of the carrier's bottom, stern end to the pivot.
module shoe() {
    hull() {
        translate([-car_bw / 2, 0, -drop - 0.01]) cube([car_bw, pivot_y, 0.01]);
        tilted() translate([-car_bw / 2, 0, -drop]) cube([car_bw, pivot_y, 0.01]);
    }
}

module carrier_tilt() {
    difference() {
        union() {
            along_y(0, car_len) dovetail_profile();
            shoe();
        }
        // foot pocket and its 3 M4 holes, tilted about the foot's front end
        tilted() {
            translate([-(foot_w / 2 + foot_clear), foot_y0 - foot_clear, -drop - 10])
                cube([foot_w + 2 * foot_clear, foot_l + 2 * foot_clear, foot_sink + 10]);
            for (y = holes_y) translate([0, y, -drop - 10]) {
                cylinder(d = m4_clear, h = car_h + 20);
                // countersink on the tilted axis, carried up past the flat top so
                // the head always seats fully on the cone
                translate([0, 0, 10 + car_h + 1 - m4_csk_h - 0.6]) cylinder(d1 = m4_clear, d2 = m4_csk_d, h = m4_csk_h);
                translate([0, 0, 10 + car_h + 1 - 0.6 - 0.01]) cylinder(d = m4_csk_d, h = 10);
            }
        }
        // lock screw and nut slot, unchanged from the v2 carrier
        translate([0, lock_y, lock_z]) rotate([0, 90, 0]) cylinder(d = lock_d, h = 2 * car_tw, center = true);
        translate([sx * nut_x - nut_t / 2 - 0.15, lock_y - nut_cw / 2 - 0.15, lock_z - nut_af / 2 - 0.15])
            cube([nut_t + 0.3, nut_cw + 0.3, car_top - lock_z + nut_af / 2 + 1]);
        // round the shoe's stern bottom edge, like the v2 carrier's
        translate([0, 0, -drop - shoe_d]) rotate([90, 0, 90]) linear_extrude(car_tw + 2, center = true)
            difference() {
                translate([-1, -1]) square([edge_r + 1, edge_r + 1]);
                translate([edge_r, edge_r]) circle(r = edge_r, $fn = 24);
            }
    }
}

// thruster held at the tilt, for the assembly render
module dummy_thruster_tilt() { tilted() dummy_thruster(); }

if (tilt_part == "carrier") translate([0, 0, car_top]) rotate([0, 180, 0]) carrier_tilt();   // flat top on the bed
else if (tilt_part == "assembly") {
    color("SteelBlue") base();
    color("MediumPurple") carrier_tilt();
    dummy_hull();
    dummy_thruster_tilt();
}
