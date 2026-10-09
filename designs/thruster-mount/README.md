# Thruster mount

## ⭐ Version 2 (current): base + sliding carrier, on the hull's own screw posts

Designed 2026-10-09 from Cobus's measurements ([measure/](measure/)). **Not yet printed.**

| From the stern | From below |
|---|---|
| ![v2 from the stern](v2/renders/assembly_from_stern.png) | ![v2 from below](v2/renders/assembly_from_below.png) |
| ![Base, print side up](v2/renders/base_print.png) | ![Base underside](v2/renders/base_underside.png) |
| **Base**, as it prints: the hump fills the tunnel; corners and bottom edge rounded | **Base underside**: dovetail slot open at the stern, 4 post-screw pockets, wire channel to the wire hole |
| ![Carrier](v2/renders/carrier_print.png) | ![Template](v2/renders/template.png) |
| **Carrier**, as it prints: the foot pocket, 3 M4 holes, lock-screw hole | **Template**: a 1.2 mm plate to check the 4 holes against the hull |

Each motor position has a moulded tunnel in the hull bottom (43 wide, 10 deep, 69 long) and **4 solid posts** inside that the stock motor shield screwed into from outside. The posts are closed, so the hull is already sealed there.

- **Base (blue):** fills the tunnel and screws to the 4 posts from outside, **7 mm** below the hull. Its outline corners (5 mm) and bottom edge (2.5 mm) are rounded; the top edge stays square to bed flat on the hull. The rounded stern end also gives the dovetail slot a lead-in. That gap gives water to the duct's intake. It carries on forward as a cover over the motor wires, up to the wire hole.
- **Carrier (purple):** a dovetail bar. The thruster's foot sinks 7 mm into it and is held by 3 M4 screws from above. It slides into the base from the stern, and forward thrust pushes it against the stop at the front.
- **Lock screw:** one M3 from the **outboard** side, so reverse thrust (the boat turns by reversing one motor) can't pull the carrier out. That's why there's a left and a right version.

**Why two parts:** the duct's oval openings are closed, so the foot screws can only go in from above. The duct also covers the post screws. One single part could never be assembled.

### Fitting it

1. **Pilot holes:** open the hull's 2 mm holes to **2.4 mm**, about **12 mm deep** from outside. Tape round the drill bit marks the depth. Hull and post together are 17.5 mm, so this leaves the post's closed top intact. Do one post first and check it doesn't crack.
2. **Base:** bed it in thickened epoxy or ABS cement (the hull is ABS), and screw it to the 4 posts with **ST2.9 × 13** with the thruster off.
3. **Foot holes:** drill the thruster foot's 3 mm holes out to **3.3 mm** and tap them **M4**, to their existing depth only. **Never drill through.** The foot sits on the duct, and a bolt end would hit the propeller.
4. **Carrier:** bolt the foot into it on the bench, with 3 × **M4 countersunk**. Drop the M3 nut into its slot in the carrier's top.
5. **Assemble:** slide the carrier in from the stern until it stops, then fit the **M3 × 40** lock screw from the outboard side.
6. **Wires:** run them along the channel and up through the wire hole. Seal the hole with a cable gland or potting.

### Parts for both sides

| Qty | Part | For |
|---|---|---|
| 8 (+ spares) | **ST2.9 × 13** stainless pan-head self-tapper | Base to the 4 posts, each side |
| 6 | **M4 countersunk** stainless, about **× 12**. Length to check: 6.1 mm goes through the carrier, the rest into the foot | Foot to carrier |
| 2 | **M3 × 40** stainless machine screw + **2 M3 nuts** | Lock screws |
| 1 each | 2.4 mm and 3.3 mm drill, **M4 tap** | Pilot holes and foot holes |
| 1 | Thickened epoxy or ABS cement | Bedding the bases |
| 2 | Cable gland, or sealant to pot the wire holes | Wire holes |
| — | ABS (or ASA) filament | Bases and carriers |

The v1 shopping list (lamp tube, nuts, rubber washers) is no longer needed.

### Print and check first

| File | Check |
|---|---|
| `v2/v2_template.stl` | Lay it on the hull. Do the 4 holes land on the 2 mm pilot holes, does the window match the tunnel, and does the scribed line sit on the rail? |
| `v2/v2_fit_dovetail_right.stl` | The first 14 mm of a base and a carrier. The carrier should slide in with a light push, not drop out, and its M3 nut should drop into its slot. |
| `v2/v2_base_right.stl`, `v2/v2_carrier_right.stl` | Right-hand thruster: lock screw from the right (outboard) side |
| `v2/v2_base_left.stl`, `v2/v2_carrier_left.stl` | Left-hand thruster |

Print in ABS or ASA (not PLA: sun and water), 4+ walls, 40 %+ infill. Both parts are already laid flat for printing: the base on its underside, the carrier on its top.

### Not yet measured (marked `VERIFY` in the .scad)

- **The rail across the tunnel:** no groove for it (Cobus, 2026-10-09). It's only 0.5 mm high, and the base sits 0.3 mm off the tunnel roof for the epoxy, so the bedding takes it up. If the base rocks on a dry fit, sand the rail down. The groove can be switched back on with `rail_groove = true`; its position (49 mm from the transom) was read off photo 1 by scale, and the template's scribed line checks it.
- **The wire hole:** about 11 mm across.
- **How deep the foot's 3 holes go.** That decides the M4 screw length.

### Files

`thruster_mount_v2.scad` is the source. Set `part` to `base`, `carrier`, `template`, `fit_dovetail` or `all`, and `side` to `right` or `left`. Its `assert`s stop a change that would make the carrier hit the hull or leave too little plastic. I checked with OpenSCAD intersections that the base, carrier, hull and thruster don't overlap anywhere; the only contact is the wings on the hull, the bedding face. Re-export after any change, e.g.
`openscad -D 'part="base"' -D 'side="left"' -o v2/v2_base_left.stl thruster_mount_v2.scad`

---

## Version 1 (shelved 2026-10-09)

Shelved because the hull turned out to have its own tunnel and screw posts, and the lamp tube only came in 15 mm locally. Kept for the record.

A printed pylon that hangs each 62 mm brushless thruster from the **stock motor-post hole**, on a **steel hollow M10 × 1 lamp tube** that also carries the wires. The hull gets no new holes. The part is symmetric, so print two.

![Pylon on a dummy thruster](renders/assembly.png)

| Render | |
|---|---|
| ![Hull face](renders/mount_iso.png) | Hull face: tube bore in the middle, screw-head pockets at each end |
| ![Underside](renders/mount_top.png) | Looking down through it: the screw clearance holes under the head pockets |

## Status (2026-10-08)

**Version 1, not yet printed.** It is designed from the stock pod's dimensions and the thruster specs; nothing has been measured on the boat yet. Print the two fit tests first.

## How it goes together

```
 inside hull     inner nut + steel washer + rubber washer
 ════════════════╪═══════════════  hull, existing 11 mm hole
                 │  ring of marine sealant on the pylon's top face
             ┌───┴───┐
             │ pylon │  the tube threads into a nut captured in the pylon's base
             └─┬───┬─┘  the wires leave through the side slot
          ╭────┴───┴────╮
          │  thruster   │  2 screws, 40 mm apart, heads inside the pylon
          ╰─────────────╯
```

1. Press an M10 × 1 lamp nut into the hex pocket in the pylon's base.
2. Bolt the pylon to the thruster: two screws down through the head pockets into the thruster's **outer** two holes. The middle hole sits under the tube and stays empty.
3. Thread the tube into the captured nut, flush with the nut's underside. Feed the thruster's three wires in through the side slot and up the tube.
4. Run a ring of marine sealant (e.g. Sikaflex) round the tube on the pylon's top face. Keep it **inside** the head pockets: less than 7 mm from the tube's centre.
5. Push the tube up through the stock hole. Inside the hull, fit a rubber washer, a steel washer and the inner nut, then tighten it so the pylon clamps the hull. **Line the thruster up with the boat's centreline before the sealant sets.** The sealant is also what stops the pylon twisting.
6. Seal the wires where they leave the top of the tube, e.g. with silicone or adhesive-lined heat-shrink.

## Parts per side

| Part | Note |
|---|---|
| Printed pylon | ASA, 4+ walls, 40 %+ infill, thruster face down on the bed (as modelled) |
| M10 × 1 hollow steel lamp tube | Cut to **27 mm** (the `.scad` prints the length for the current settings) |
| 2× M10 × 1 lamp nuts | One captured in the pylon, one inside the hull |
| M10 steel washer + rubber washer | Inside the hull |
| 2× M3 socket-head screws, stainless | **Length to be decided** once the thruster's holes are checked. The pylon gives 4 mm of grip. |
| Marine sealant | Sikaflex or similar |

## Check these before printing the full pylon

Every value marked `VERIFY` in `thruster_mount.scad` is an assumption:

- **The thruster's holes:** three 3 mm holes in a line along the top, 20 mm apart (Cobus, 2026-10-08). The pylon uses the outer pair, 40 mm apart. Still to check: are they threaded? A tapped M3 hole measures about 2.5 mm, so 3 mm may mean plain holes for self-tappers.
- **50 mm of flat hull at each post hole.** The pylon is 50 mm long to reach the outer holes; the stock pod's saddle was only 35 mm.
- **The lamp nut:** 13 mm across the flats and 3 mm thick is assumed. Measure the ones you buy and set `nut_af` and `nut_h`.
- **The hull wall at the post hole:** 3 mm assumed. It only changes the tube length.
- **The duct's outside diameter:** 68 mm assumed (62 mm opening plus about 3 mm walls). With the 15 mm `drop`, the thruster's axis sits about 49 mm below the hull. Check that against how shallow the water is where you launch.
- **Is the hull flat where the pylon sits?** If not, the top face needs to follow the curve.

## Fit tests (a few grams each)

| File | What to check |
|---|---|
| `thruster_mount_fit_bottom.stl` | The two screw holes line up with the thruster's outer holes; the lamp nut presses in and doesn't spin; the tube threads in |
| `thruster_mount_fit_top.stl` | The hull face sits flat against the hull at the post hole |

## Files

- `thruster_mount.scad`: the source. Set `part` to `mount`, `fit_bottom`, `fit_top`, or `all` (an assembly preview, not for printing). Its `assert`s stop a parameter change that would break a wall.
- `thruster_mount_*.stl`: exported from the current settings. Re-export after any change:
  `openscad -D 'part="mount"' -o thruster_mount_mount.stl thruster_mount.scad`
- `renders/`: preview images. OpenSCAD is a snap here and can't write to `/tmp`, so render into the repo.

## Design notes

- **Why a steel tube:** about 1.7 kg of thrust per side bends the post where it meets the hull. A printed 11 mm post would see roughly 7 MPa there, close to where printed layers separate, and the load repeats on every run.
- **Why the outer pair of holes:** the thruster's middle hole is directly under the tube. Using the outer two, 40 mm apart, keeps the tube centred and resists the thrust better than a 20 mm pair.
- **Why sealant, not an O-ring:** the sealant also stops the pylon twisting, and it copes with a hull that isn't perfectly flat. Sealant on the face plus the rubber washer inside the hull do the sealing.
- **Footprint:** 50 × 18 mm, long enough for the outer screw pair, with rounded ends to keep it streamlined.
- **If a pylon still twists:** set `pin_d` (e.g. 3.2) to add a locating pin. That needs one small new hole in the hull.
