# Handover: current state

_Last updated: 2026-10-14_

## Where things stand

- **Running today (working well):** Pixhawk 2.4.8 + GPS on ArduPilot Rover, stock 390 brushed thrusters on two CL9030 brushed ESCs, stock 7.4 V 10 Ah Li-ion pack. The Pixhawk is powered from an ESC's 5 V output, so it cannot read the battery yet.
- **Brushless upgrade:** 480 Kv ducted thrusters (CW/CCW pair) and two BLHeli 40 A bidirectional ESCs ordered. Duct opening measured at 62 mm, which confirms the thrusters match the specs in [the chat export](docs/sources/2026-10-08-earlier-chat-export.md), not the 1000 KV listing.
- **Decided:** go **6S**. Cap `MOT_THR_MAX` at about 90%, because a full 6S pack (25.2 V) is slightly over the 24 V rating.
- **Power module and battery (2026-10-14):** Holybro **PM06 V1** fitted; Akita **6S2P Li-ion 6,000 mAh, no BMS**. Voltage calibrated (`BATT_VOLT_MULT` 10.930); current not yet. Failsafe RTL at 3.3 V/cell. See [docs/03](docs/03-ardupilot-setup.md).
- **Ground station:** Mission Planner runs on the Ubuntu VM (`~/Applications/MissionPlanner`, Mono) over the SiK radio on `/dev/ttyUSB0` at 57600.

## Next steps

1. Wait for the thrusters; bench test them with the props in water.
2. ~~Decide the pack~~: done, Akita 6S2P 6,000 mAh Li-ion, no BMS (2026-10-14).
3. Weigh the stock battery; do the bath/ballast hull test.
4. **Thruster mounts: v2** ([designs/thruster-mount](designs/thruster-mount/)). A base screwed to the hull's 4 existing posts (ST2.9 × 13) and a dovetail carrier that holds the thruster (3 × M4 into the tapped foot), slides in from the stern and is locked by one M3 × 30 from the outboard side. Left and right versions.
   - **Tested 2026-10-10:** the template's 4 holes line up. The base is now cut away over a 4 mm step on the inboard side (84 mm from the transom). A ~1 mm gap on the curve came from a moulding ridge round the mount area, which Cobus shaved flush. The first dovetail (PLA) was loose because its walls were too steep; it's now 16/24 mm, and the ABS clearance ladder picked **0.10 mm** (no wobble). The wire cover now runs 23 mm past the wire hole to cover the old mounting hole.
   - **Decided:** stay with two parts (one-piece rejected, see the mount README); epoxy bedding optional.
   - **Confirmed 2026-10-10:** ridge shaved and the base now sits well; the reprinted template (with the 23 mm tip) fits; the other tunnel has the same inboard step, so the left part's mirrored cut-out is right.
   - **Screws (2026-10-11):** M4 × 12 countersunk bought for the foot. Post screws stay **ST2.9 × 13** stainless pan head ([Fowkes](https://www.fowkes.co.za/product/self-tap-screw-pan-s-s-a4-pz-2-9x13-pan-head-pozi-4-x-13mm)); the ST3.5 × 13 Cobus bought are too big for the 6.2 mm posts (risk of splitting them). No stainless M3 × 40 to be found in SA, so the lock is redrawn for a stainless **M3 × 30** (Xtrude 3D): with a stainless **Nyloc** nut (no Loctite: it attacks ABS): slot 4 mm wide, 4.5 mm outboard of the carrier's centre, head sunk 4 mm. See `v2/renders/lock_section.png`. The black 12.9 M3 × 40 from Fowkes would rust: bench use only.
   - **Next:** a PLA+ mock-up of the right base and carrier with the thruster fitted, to check the whole assembly. Foot holes measured **10.5 mm** deep (2026-10-11): the M4 × 12 goes ~6 mm in, 4.5 mm short of the bottom, so it can't bottom out. The carrier's aft bottom edge is now rounded 2.5 mm like the base (2026-10-12, `v2/renders/carrier_aft_round.png`); the PLA+ mock-up carrier predates it. Then measure the wire hole, buy the screws, print the real parts.
   - Still to design: the taller battery lid.
5. **Hopper servo holes leak (raised 2026-10-11):** in windy conditions water washes over the deck and in through the holes for the hopper servo horns. There is already an O-ring in each hole, but water still gets past it. Cobus is also considering a drain/breather plug to open while the boat is idle. Options discussed: a labyrinth cap (raised ring on the deck + a skirt on the horn, no friction; first choice), a TPU-95 gasket under the servo, an O-ring on the shaft, IP67 servos. **Waiting on** photos from above and below plus the hole, boss and gap sizes; then redraw the horn ([servo parts](designs/servo-parts/)). Picked up after the mount screws arrive.
6. **SketchUp parts added 2026-10-08** (STL only): [cable holders](designs/cable-holders/), [servo parts](designs/servo-parts/), [Pixhawk bed](designs/pixhawk-bed/), [GPS antenna spacer](designs/gps-antenna-spacer/). All printed and in use: eSUN PLA+, except the GPS spacers in solid TPU-95. Purposes recorded 2026-10-09; the receiver antenna tube moved to `cable-holders/`. Still to do: add the `.skp` files beside the STLs.
7. PM06 fitted and battery failsafe set (2026-10-14). Still to do: calibrate `BATT_AMP_PERVLT` from the charger's mAh after a run; the skid-steering parameters ([docs/03](docs/03-ardupilot-setup.md)); the LED indicator ([docs/04](docs/04-battery-led-indicator.md)).

## Open questions

- **5 V supply:** with the PM06 powering the Pixhawk, decide what each ESC's 5 V / 3 A BEC feeds (servos? LED MCU?). Never connect two BECs to the same rail.
- Which Pixhawk outputs drive the relay and the hopper servos (motors: `SERVO1` / `SERVO3`).
- Which RC receiver is paired with the T14SG, and how it connects (SBUS?).
- Which failsafes are configured today.
- Rover is set up as a Rover with twin motors, not the Boat frame (`FRAME_CLASS = 2`). It may be worth trying Boat.
