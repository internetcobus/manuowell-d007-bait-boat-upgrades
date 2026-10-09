# Handover: current state

_Last updated: 2026-10-09_

## Where things stand

- **Running today (working well):** Pixhawk 2.4.8 + GPS on ArduPilot Rover, stock 390 brushed thrusters on two CL9030 brushed ESCs, stock 7.4 V 10 Ah Li-ion pack. The Pixhawk is powered from an ESC's 5 V output, so it cannot read the battery yet.
- **Brushless upgrade:** 480 Kv ducted thrusters (CW/CCW pair) and two BLHeli 40 A bidirectional ESCs ordered. Duct opening measured at 62 mm, which confirms the thrusters match the specs in [the chat export](docs/sources/2026-10-08-earlier-chat-export.md), not the 1000 KV listing.
- **Decided:** go **6S**. Cap `MOT_THR_MAX` at about 90%, because a full 6S pack (25.2 V) is slightly over the 24 V rating.
- **Power module:** Holybro **PM06** on hand, **not fitted yet**.

## Next steps

1. Wait for the thrusters; bench test them with the props in water.
2. Decide the pack: 2× Auline 21700 S70 6S 4500 mAh in parallel (AliExpress), or a no-BMS Molicel P42A 6S2P (Akita or DIY). See [docs/02](docs/02-brushless-upgrade.md).
3. Weigh the stock battery; do the bath/ballast hull test.
4. **Thruster mounts: v2 designed** (2026-10-09, [designs/thruster-mount](designs/thruster-mount/)), not yet printed. A base screwed to the hull's 4 existing posts (ST2.9 × 13) and a dovetail carrier that holds the thruster (3 × M4 into the tapped foot) and slides in from the stern, locked by one M3 × 40 from the outboard side. Left and right versions. **Next (2026-10-09): Cobus is printing `v2_template` and `v2_fit_dovetail_right`** (the fit test in ABS, the same as the real parts). Then adjust from his results; check the rail position, the wire hole size and the depth of the foot holes; buy the screws. Still to design: the taller battery lid.
5. **SketchUp parts added 2026-10-08** (STL only): [cable holders](designs/cable-holders/), [servo parts](designs/servo-parts/), [Pixhawk bed](designs/pixhawk-bed/), [GPS antenna spacer](designs/gps-antenna-spacer/). All printed and in use: eSUN PLA+, except the GPS spacers in solid TPU-95. Purposes recorded 2026-10-09; the receiver antenna tube moved to `cable-holders/`. Still to do: add the `.skp` files beside the STLs.
6. Fit the PM06; configure the Rover parameters and battery failsafe ([docs/03](docs/03-ardupilot-setup.md)); build the LED indicator ([docs/04](docs/04-battery-led-indicator.md)).

## Open questions

- **PM06 connector:** the PM06 ends in a 6-pin JST-GH plug; the Pixhawk 2.4.8 power port is a 6-pin DF13. An adapter cable is needed. Check which PM06 version it is (V1 is 2S-6S, V2 is 2S-14S); either covers 6S.
- **5 V supply:** with the PM06 powering the Pixhawk, decide what each ESC's 5 V / 3 A BEC feeds (servos? LED MCU?). Never connect two BECs to the same rail.
- Which Pixhawk outputs drive the relay and the hopper servos (motors: `SERVO1` / `SERVO3`).
- Which RC receiver is paired with the T14SG, and how it connects (SBUS?).
- Which failsafes are configured today.
- Rover is set up as a Rover with twin motors, not the Boat frame (`FRAME_CLASS = 2`). It may be worth trying Boat.
