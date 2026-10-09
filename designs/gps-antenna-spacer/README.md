# GPS antenna spacer

Drawn by Cobus in SketchUp during the upgrade. Added 2026-10-08 from `GPS antenna spacer.stl`.

![GPS antenna spacer](renders/gps-antenna-spacer.png)

## What it's for

The GPS antenna is mounted on the **front of the hull, on the centreline**. The hull isn't flat there, so these curved spacers sit between the antenna bracket and the hull: the bracket can be tightened firmly and still grip the curve.

Described by Cobus, 2026-10-09. **Printed in solid TPU-95** (100 % infill), so the spacers flex to follow the hull's curve exactly. **In use.**

The original plate also held the receiver antenna tube. That isn't a GPS part, so on 2026-10-09 it moved to the [cable holders](../cable-holders/) as `receiver-antenna-tube.stl`.

## What's in the file

`gps-antenna-spacer.stl` is a print plate with 7 parts, in millimetres:

| Part | Size (mm) |
|---|---|
| Curved square pad | 17.0 × 14.0 × 2.7 |
| Ring | 14.4 × 14.4 × 2.1 |
| Shaped washers with a hole (4) | about 14-17 × 14 × 2.2-4.4 |
| Small washers (2) | 8.0 × 8.0 × 1.2 and 2.2 |

Watertight mesh (no open edges). The plate is now 7.3 mm tall (it was 22 mm with the tube).

**Print in TPU-95, solid.** In PLA+ these spacers wouldn't follow the curve, and the bracket would rock.

## Source

The SketchUp `.skp` file isn't in the repo yet. Add it here as `gps-antenna-spacer.skp` so the original can be reopened and changed.

## Changing it

Without the `.skp`, changes are made on this STL in OpenSCAD: adding or cutting features, or scaling. Redrawing it as a parametric `.scad` is the better route if it will keep changing.
