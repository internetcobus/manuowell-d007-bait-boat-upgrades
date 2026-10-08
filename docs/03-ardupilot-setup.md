# ArduPilot Rover setup

Planned settings for the brushless upgrade. Nothing here has been applied yet.

## Skid steering

| Parameter | Value | Note |
|---|---|---|
| `SERVO1_FUNCTION` | 73 | Throttle left |
| `SERVO3_FUNCTION` | 74 | Throttle right |
| `SERVO1_MIN` / `TRIM` / `MAX` | 1000 / 1500 / 2000 | Same for `SERVO3_*` |
| `MOT_PWM_TYPE` | 0 | Normal PWM |
| `MOT_THR_MAX` | about 90 | A full 6S pack (25.2 V) is slightly over the thrusters' 24 V rating |

Set both ESCs to bidirectional (3D) mode, with neutral at 1500 µs.

## Power module (Holybro PM06)

Values are from [Holybro's PM06 V2 specs](https://www.getfpv.com/electronics/autopilot-systems/pm06-14s-power-module.html). Check them against the version on hand, and calibrate against a multimeter and a known charge.

| Parameter | Value |
|---|---|
| `BATT_MONITOR` | 4 (analog voltage and current) |
| `BATT_VOLT_MULT` | 18.182 |
| `BATT_AMP_PERVLT` | 36.364 |

## Battery failsafe

- Return home (RTL) on low battery. For Li-ion, about **3.3 V per cell, 19.8 V for 6S**.
- Set it above any BMS cut-off, so the boat starts home before the BMS disconnects the pack.
- Log the mAh used per drop to get real drop counts per charge.
