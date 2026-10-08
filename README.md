# Manuowell D007 bait boat upgrades

A stock Manuowell D007 bait boat converted to a Pixhawk 2.4.8 running ArduPilot Rover, now being upgraded to brushless thrusters on 6S.

**Start with [HANDOVER.md](HANDOVER.md)**: the current state, what's next and what's still open.

## Contents

| Path | What it holds |
|---|---|
| [HANDOVER.md](HANDOVER.md) | Current state, next steps, open questions. Keep it current. |
| [docs/01-stock-vs-converted.md](docs/01-stock-vs-converted.md) | The stock boat's specs, and what the conversion changed |
| [docs/02-brushless-upgrade.md](docs/02-brushless-upgrade.md) | Thrusters, ESCs, power module, battery options and sourcing |
| [docs/03-ardupilot-setup.md](docs/03-ardupilot-setup.md) | Rover parameters for skid steering, the power module and the battery failsafe |
| [docs/04-battery-led-indicator.md](docs/04-battery-led-indicator.md) | Reusing the stock 4 LEDs as a 4S/6S battery gauge |
| [docs/sources/](docs/sources/) | Source material kept as-is, e.g. the earlier chat export |
| [designs/](designs/) | Printed parts: thruster mounts, battery lid |

## The boat in one paragraph

Used about 4 times a year to drop bait about 180 m out. The stock electronics are gone; a Pixhawk 2.4.8 with GPS runs ArduPilot Rover with twin-motor (skid) steering, controlled from a Futaba T14SG, with a 433 MHz SiK telemetry radio to a phone (QGroundControl or Mission Planner). The bait hoppers are on servos and the lights on a relay, both driven by the Pixhawk. The goal of the current upgrade is about 1 m/s loaded outbound (now about 0.7 m/s) so the fishing lines sag less.
