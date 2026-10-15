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

## NeoPixel on AUX 5 (fitted)

Cobus has a NeoPixel driven straight from the Pixhawk's **AUX 5** output. It works.

Since 2026-10-15 the LED is a **WS2812D** (the through-hole one, as on the camping fan). It takes its colours in **RGB** order, not the usual NeoPixel GRB, so with `NTF_LED_TYPES` set to NeoPixel, green showed as red. Fix: in `NTF_LED_TYPES`, untick **NeoPixel** (bit 8) and tick **NeoPixelRGB** (bit 18), then reboot. Both types use the same output (`SERVO13_FUNCTION` = 120, NeoPixel1, on AUX 5), so nothing else changes. NeoPixelRGB needs **Rover 4.5 or newer**. Set and confirmed working 2026-10-15 (green shows green).

| Wire | From | Through | To NeoPixel |
|---|---|---|---|
| Data | AUX 5 signal (3.3 V logic) | **330 Ω resistor**, as close to the LED as possible | DIN |
| Power | 5 V | **diode** (same as the camping fan's) | VDD |
| Ground | AUX ground | | GND |

- **Why the diode on VDD:** the Pixhawk's AUX outputs send a 3.3 V signal. A NeoPixel on a full 5 V wants about 0.7 × VDD (3.5 V) to count as a "high", so 3.3 V falls just short. Fed straight from 5 V it **did not work**. The diode drops VDD so that 3.3 V counts as high.
- **Target VDD: 3.9–4.43 V, measured with the LED dark.** Too high and the data fails, too low and green and blue go dim. This is the same rule as the camping fan, which needed two of Cobus's diodes (about 0.35 V drop each) to reach 4.30 V; one gave 4.67 V and failed. Here, VDD has not been measured yet.
- **Why the 330 Ω resistor:** it limits the current into DIN if data arrives before the LED's supply is up, and it damps ringing on the data line. Solder it inline and heat-shrink it; the hull is damp. (Added 2026-10-15.)
