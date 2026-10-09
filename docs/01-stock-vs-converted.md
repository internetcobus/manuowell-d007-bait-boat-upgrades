# Stock vs converted

Conversion done before 2026-10-08: the stock electronics were removed and replaced with a Pixhawk.

| Item | Stock D007 | Converted |
|---|---|---|
| Control electronics | Stock board | Removed; **Pixhawk 2.4.8** and the RC receiver on a printed [bed](../designs/pixhawk-bed/) with a Velcro strap |
| Firmware | Stock | **ArduPilot Rover**, twin drive motors (skid steering) |
| Navigation | Built-in GPS + compass, limited: 3 stored fishing spots, auto-pilot to a spot, auto-return | **GPS** on the Pixhawk; full missions and waypoints. Antenna on the bow, on the centreline, on printed [curved spacers](../designs/gps-antenna-spacer/) |
| Failsafes | Low-power alarm, low-power auto-return, lost-signal auto-return | Rover failsafes (what is configured is not yet recorded) |
| RC | Stock remote, about 500 m range; the shop page also lists "4G mobile" | **Futaba T14SG** |
| Telemetry | None | **SiK 433 MHz** on **TELEM1**, to a phone (QGroundControl or Mission Planner) |
| Motor drive | Stock board | Two **CL9030** brushed ESCs, one per motor |
| Motors | Two 390 brushed thrusters (see below) | Unchanged |
| Lights | Two LEDs, front and rear | Switched by a **relay** from the Pixhawk |
| Battery | 7.4 V 10 Ah Li-ion | Unchanged |
| Battery indicator | 4 LEDs (3 blue + 1 red), 2S only | Planned rebuild, see [04](04-battery-led-indicator.md) |
| Pixhawk power | n/a | From an ESC's 5 V output; no battery reading |
| Wiring | Stock | Signal and power cables kept apart by printed [cable holders](../designs/cable-holders/); the receiver antenna held at 90 degrees |
| Bait hoppers | Two side-release hoppers, 2 kg total, on **continuous-rotation** servos | **Normal (positional) metal-geared servos** on Pixhawk outputs, with a printed horn ([servo parts](../designs/servo-parts/)) |
| Fish finder | Not supported | — |

## Stock specs

Source: [Carpe Diem Online, D007 Classic Series](https://carpediemonline.co.za/online-store/d007-classic-series/). The page's heading reads **D008**, although the URL says D007, so a figure may belong to the D008.

- **Hull:** 53 × 33 × 22 cm overall, hull 50 × 30 × 18 cm, virgin ABS, carbon-fibre finish, 3 kg, stainless steel folding handle.
- **Battery:** D008/V017 pack, 7.4 V, 10 Ah, Li-ion, 10 × 5 × 4 cm, listed at 0.5 kg (the export estimates about 400 g; to be weighed). R1,127 as a spare from [Carpe Diem Online](https://carpediemonline.co.za/online-store/d008-v017-battery-10ah/).
- **Battery bay:** about 98 × 73 × 82 mm. A taller lid can be printed.
- **Motors:** a pair of SkyArea 390-size brushed underwater thrusters ([AliExpress](https://www.aliexpress.com/item/1005006050172879.html), R340 a pair): 30 W, rated 5-12 V, about 10,000 rpm, 26 mm 3-blade prop, ABS shell, silicone seal. About 130 mm long overall (87 mm body), mounted on an 11 mm threaded post (37 mm tall, 28 mm threaded). No current rating listed; about 4 A each running, by estimate from 30 W at 7.4 V.
- **Performance today:** about 0.7 m/s loaded.
