# ArduPilot Rover setup

Settings for the brushless upgrade. The power module and battery sections were set on 2026-10-14; the skid-steering section is still planned.

## Skid steering

| Parameter | Value | Note |
|---|---|---|
| `SERVO1_FUNCTION` | 73 | Throttle left |
| `SERVO3_FUNCTION` | 74 | Throttle right |
| `SERVO1_MIN` / `TRIM` / `MAX` | 1000 / 1500 / 2000 | Same for `SERVO3_*` |
| `MOT_PWM_TYPE` | 0 | Normal PWM |
| `MOT_THR_MAX` | about 90 | A full 6S pack (25.2 V) is slightly over the thrusters' 24 V rating |

Set both ESCs to bidirectional (3D) mode, with neutral at 1500 µs.

## Power module (Holybro PM06 V1) and battery

Fitted 2026-10-14 with the Akita pack: **6S2P Li-ion, 6,000 mAh, no BMS**. With no BMS, the battery failsafe below is the only protection against over-discharge, so keep the voltage calibrated and always balance-charge.

| Parameter | Value | Note |
|---|---|---|
| `BATT_MONITOR` | 4 | Analog voltage and current. Reboot after setting |
| `BATT_VOLT_PIN` / `BATT_CURR_PIN` | 2 / 3 | Pixhawk 2.4.8 power port |
| `BATT_VOLT_MULT` | **10.930** | Calibrated 2026-10-14: multimeter 24.34 V, HUD 24.33 V afterwards. The PM06 **V2** value (18.182) read 40.49 V on this V1 |
| `BATT_AMP_PERVLT` | 36.364 | **Not calibrated** (a V2 value, probably wrong for the V1). Correct it from the mAh the charger puts back after a run |
| `BATT_CAPACITY` | 6000 | mAh |
| `BATT_ARM_VOLT` | 21.6 | 3.6 V per cell: won't arm on a half-flat pack |

Calibrating the voltage: Mission Planner's "Measured battery voltage" box wouldn't edit (under Mono), so work it out by hand: new `BATT_VOLT_MULT` = old × multimeter ÷ HUD.

## Battery failsafe

| Parameter | Value | Note |
|---|---|---|
| `BATT_FS_VOLTSRC` | 1 | Sag-compensated, so full-throttle bursts don't trigger it |
| `BATT_LOW_VOLT` / `BATT_LOW_MAH` | 19.8 / 1500 | 3.3 V per cell, or 25% left |
| `BATT_LOW_TIMER` | 10 | Seconds |
| `BATT_FS_LOW_ACT` | 1 | RTL |
| `BATT_CRT_VOLT` / `BATT_CRT_MAH` | 18.6 / 900 | 3.1 V per cell, or 15% left |
| `BATT_FS_CRT_ACT` | 1 | RTL too: stranded 180 m out is worse than one deeper discharge |

- The mAh triggers are only approximate until `BATT_AMP_PERVLT` is calibrated, and the count starts at switch-on: only power up on a fully charged pack.
- Log the mAh used per drop to get real drop counts per charge.
