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

**Cells:** the invoice says "INR18650-30" and the seller said Samsung, so they are taken to be **Samsung INR18650-30Q** (the pack is wrapped, so the label can't be checked). Datasheet figures:

| | Per cell | 6S2P pack |
|---|---|---|
| Charge voltage | 4.20 V | 25.2 V |
| Absolute discharge cut-off | 2.5 V | 15.0 V |
| Max continuous discharge | 15 A | **30 A** |
| Standard / max charge | 1.5 A / 4 A | **3 A** / 8 A |

**Charging:** balance charger on Li-ion, balance lead always plugged in (no BMS), 3 A.
- Before a fishing day: charge to **4.20 V** the night before.
- Storage (a week or more unused): the charger's storage mode, about 3.8 V per cell (22.8 V pack). Sitting full at 4.2 V for weeks ages Li-ion.
- 4.10 V (the charger's default) gives ~90% capacity for longer life. Use it when charging days ahead.

**Watch the 30 A pack limit:** two 480 Kv thrusters on 6S may pull more than that together. On the first run, give it a few seconds at full throttle and read the peak amps on the HUD.

| Parameter | Value | Note |
|---|---|---|
| `BATT_MONITOR` | 4 | Analog voltage and current. Reboot after setting |
| `BATT_VOLT_PIN` / `BATT_CURR_PIN` | 2 / 3 | Pixhawk 2.4.8 power port |
| `BATT_VOLT_MULT` | **10.930** | Calibrated 2026-10-14: multimeter 24.34 V, HUD 24.33 V afterwards. The PM06 **V2** value (18.182) read 40.49 V on this V1 |
| `BATT_AMP_PERVLT` | 36.364 | **Not calibrated.** Holybro's published PM06 figure. Their voltage figure (18.182) was badly wrong on this V1, but one PM06 user on the ArduPilot forum calibrated current to 38, so this is probably within ~5%. Correct it with a meter in series, or from the mAh the charger puts back after a run |
| `BATT_CAPACITY` | 6000 | mAh |
| `BATT_ARM_VOLT` | 21.6 | 3.6 V per cell: won't arm on a half-flat pack |

Calibrating the voltage: Mission Planner's "Measured battery voltage" box wouldn't edit (under Mono), so work it out by hand: new `BATT_VOLT_MULT` = old × multimeter ÷ HUD.

## Battery failsafe

| Parameter | Value | Note |
|---|---|---|
| `BATT_FS_VOLTSRC` | 1 | Sag-compensated, so full-throttle bursts don't trigger it |
| `BATT_LOW_VOLT` / `BATT_LOW_MAH` | 19.8 / **0** | 3.3 V per cell. mAh trigger off (2026-10-14) |
| `BATT_LOW_TIMER` | 10 | Seconds |
| `BATT_FS_LOW_ACT` | 1 | RTL |
| `BATT_CRT_VOLT` / `BATT_CRT_MAH` | 18.6 / **0** | 3.1 V per cell. mAh trigger off (2026-10-14) |
| `BATT_FS_CRT_ACT` | 1 | RTL too: stranded 180 m out is worse than one deeper discharge |

- **Voltage only, on purpose.** The boat is switched off between drops, and ArduPilot's mAh count starts from zero at every power-up, so mAh triggers (and the HUD's battery %) would read far too full after the first drop. Read the HUD **voltage** before each drop instead.
- The current sensor stays on: it gives live amps (fouled prop, the 30 A pack limit) and makes `BATT_FS_VOLTSRC` = 1 work.
- **mAh used per drop:** Mission Planner, Data screen, Quick tab: double-click a box, tick `battery_usedmah`. It resets at power-up. Each power-up's DataFlash log keeps it as `BAT.CurrTot`, so a day's drops can be added up afterwards.
- **Calibrating current from a day out:** new `BATT_AMP_PERVLT` = 36.364 × mAh the charger puts back ÷ total of the logs' final `CurrTot`. More accurate: a DC clamp meter on a battery lead at steady throttle, new = old × clamp ÷ HUD amps.
