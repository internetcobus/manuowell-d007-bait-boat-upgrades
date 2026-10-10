# Handover: current state

_Last updated: 2026-10-10_

## Where things stand

- **Running today (working well):** Pixhawk 2.4.8 + GPS on ArduPilot Rover, stock 390 brushed thrusters on two CL9030 brushed ESCs, stock 7.4 V 10 Ah Li-ion pack. The Pixhawk is powered from an ESC's 5 V output, so it cannot read the battery yet.
- **Brushless upgrade:** 480 Kv ducted thrusters (CW/CCW pair) and two BLHeli 40 A bidirectional ESCs ordered. Duct opening measured at 62 mm, which confirms the thrusters match the specs in [the chat export](docs/sources/2026-10-08-earlier-chat-export.md), not the 1000 KV listing.
- **Decided:** go **6S**. Cap `MOT_THR_MAX` at about 90%, because a full 6S pack (25.2 V) is slightly over the 24 V rating.
- **Power module:** Holybro **PM06** on hand, **not fitted yet**.

## Next steps

1. Wait for the thrusters; bench test them with the props in water.
2. Decide the pack: 2× Auline 21700 S70 6S 4500 mAh in parallel (AliExpress), or a no-BMS Molicel P42A 6S2P (Akita or DIY). See [docs/02](docs/02-brushless-upgrade.md).
3. Weigh the stock battery; do the bath/ballast hull test.
4. **Thruster mounts: v2** ([designs/thruster-mount](designs/thruster-mount/)). A base screwed to the hull's 4 existing posts (ST2.9 × 13) and a dovetail carrier that holds the thruster (3 × M4 into the tapped foot), slides in from the stern and is locked by one M3 × 40 from the outboard side. Left and right versions.
   - **Tested 2026-10-10:** the template's 4 holes line up. The base is now cut away over a 4 mm step on the inboard side (84 mm from the transom). A ~1 mm gap on the curve came from a moulding ridge round the mount area, which Cobus shaved flush. The first dovetail (PLA) was loose because its walls were too steep; it's now 16/24 mm, and the ABS clearance ladder picked **0.10 mm** (no wobble). The wire cover now runs 23 mm past the wire hole to cover the old mounting hole.
   - **Decided:** stay with two parts (one-piece rejected, see the mount README); epoxy bedding optional.
   - **Confirmed 2026-10-10:** ridge shaved and the base now sits well; the reprinted template (with the 23 mm tip) fits; the other tunnel has the same inboard step, so the left part's mirrored cut-out is right.
   - **Next:** a PLA+ mock-up of the right base and carrier with the thruster fitted, to check the whole assembly. Then measure the foot holes' depth (M4 length) and the wire hole, buy the screws, print the real parts.
   - Still to design: the taller battery lid.
5. **SketchUp parts added 2026-10-08** (STL only): [cable holders](designs/cable-holders/), [servo parts](designs/servo-parts/), [Pixhawk bed](designs/pixhawk-bed/), [GPS antenna spacer](designs/gps-antenna-spacer/). All printed and in use: eSUN PLA+, except the GPS spacers in solid TPU-95. Purposes recorded 2026-10-09; the receiver antenna tube moved to `cable-holders/`. Still to do: add the `.skp` files beside the STLs.
6. Fit the PM06; configure the Rover parameters and battery failsafe ([docs/03](docs/03-ardupilot-setup.md)); build the LED indicator ([docs/04](docs/04-battery-led-indicator.md)).

## Open questions

- **PM06 connector:** the PM06 ends in a 6-pin JST-GH plug; the Pixhawk 2.4.8 power port is a 6-pin DF13. An adapter cable is needed. Check which PM06 version it is (V1 is 2S-6S, V2 is 2S-14S); either covers 6S.
- **5 V supply:** with the PM06 powering the Pixhawk, decide what each ESC's 5 V / 3 A BEC feeds (servos? LED MCU?). Never connect two BECs to the same rail.
- Which Pixhawk outputs drive the relay and the hopper servos (motors: `SERVO1` / `SERVO3`).
- Which RC receiver is paired with the T14SG, and how it connects (SBUS?).
- Which failsafes are configured today.
- Rover is set up as a Rover with twin motors, not the Boat frame (`FRAME_CLASS = 2`). It may be worth trying Boat.
