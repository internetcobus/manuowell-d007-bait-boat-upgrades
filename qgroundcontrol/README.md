# QGroundControl

Cobus drives the boat from QGroundControl (phone, and since 2026-10-19 the Ubuntu VM: v5.1.5 AppImage in `~/Applications/QGroundControl/`, app-menu entry "QGroundControl").

## Fly View actions: `FlyViewActions.json`

Cobus's buttons for the Fly View (2026-10-19). Install: copy to `Documents/QGroundControl/MavlinkActions/` (on Android, the QGroundControl folder in the phone's storage), then pick it under Application Settings, **Fly View Actions**.

| Button | MAVLink command | Does |
|---|---|---|
| Lights ON / OFF | 181 `DO_SET_RELAY`, relay 0, 1 / 0 | Relay 0 = `RELAY1` (`RELAY1_FUNCTION` 1, `RELAY1_PIN` 55, inverted) |
| L Drop / L Lock (5) | 183 `DO_SET_SERVO`, Main Out 5, 2000 / 1000 µs | Left hopper |
| R Drop / R Lock (6) | 183 `DO_SET_SERVO`, Main Out 6, 2000 / 1000 µs | Right hopper |

- Checked against Rover 4.7.2 (`AP_ServoRelayEvents::do_set_servo`): Main Out 5 and 6 are RC passthrough (`SERVO5_FUNCTION` 58 = RC8, `SERVO6_FUNCTION` 57 = RC7), which `DO_SET_SERVO` is allowed to drive. If the Futaba is on and that RC channel's stick or switch moves, the RC input takes the servo back.
- `DO_SET_SERVO` sends the PWM as given; it is not limited by `SERVOn_MIN`/`MAX` (1000 / 2100 here).
- The repo copy fixes two copied descriptions (the R buttons said "Main Out 5").
