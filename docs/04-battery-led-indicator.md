# Battery LED indicator

The stock boat has a 4-LED battery gauge (3 blue + 1 red) that only understands 2S. The plan (options 1 + 3 from the [chat export](sources/2026-10-08-earlier-chat-export.md)): reuse those LEDs, driven by a small microcontroller, with the Pixhawk battery failsafe as the real safety net.

## Hardware

- MCU: ATtiny85, Nano or ESP32.
- Battery voltage through a divider, e.g. 100k / 10k.
- Powered from an ESC's 5 V BEC.
- Bypass the stock board: cut its battery feed, isolate the LEDs from its chip, and drive them through resistors: 150-330 Ω for blue, 220-470 Ω for red, at 5 V.

## Logic

Auto-detect 4S or 6S at power-up, then show the per-cell voltage:

| Per cell | LEDs |
|---|---|
| 3.95 V or more | 3 blue |
| 3.80 V or more | 2 blue |
| 3.65 V or more | 1 blue |
| below 3.65 V | red |
| below 3.5 V | red, flashing |

These thresholds suit LiPo. Lower them for Li-ion.
