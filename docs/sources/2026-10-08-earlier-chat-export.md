# Manuowell D007 Bait Boat — Motor & Battery Upgrade (Session Export)
Exported: 8 Oct 2026

## Boat & current setup
- Manuowell D007 bait boat, used ~4×/year, drops ~180 m out
- Pixhawk 2.4.8 + GPS on ArduPilot Rover (working well); telemetry via SiK radio to phone
- Stock thrusters: 390 brushed, 7.4V/2S, ~10,000 RPM, 26 mm 3-blade prop, inline pods
- Stock battery: 7.4V 2S Li-ion, ~10 Ah (~400 g est. — weigh to confirm)
- Battery bay: ~98 × 73 × 82 mm (can print a taller lid)
- Stock 4-LED voltage indicator (3 blue + 1 red), 2S only

## Goal
- ~1 m/s loaded outbound so fishing lines sag less (thrust problem); ~2 m/s empty return is a bonus
- Current loaded speed: ~0.7 m/s

## Thrusters & ESCs (ordered, AliExpress)
- Brushless ducted 4-blade thrusters, CW/CCW pair
  - 480 Kv, 12–24 V, 13 A, 30–200 W, ~2 kg thrust each @ 24 V
  - 162 g each, 75 mm long, 62 mm Ø, 20 mm mounting hole spacing, 250 mm leads
- ESCs: BLHeli 40 A (50 A burst), 2S–6S, 5V/3A BEC, bidirectional, programmable

## Key conclusions
- **Go 6S**: rated thrust is at 24 V; 4S gives only ~0.75–1 kg/thruster, 6S ~1.7 kg
- Cap `MOT_THR_MAX` ~90% (full 6S = 25.2 V, slightly over 24 V rating)
- Loaded speed limited by hull speed (~0.9–1 m/s for this size hull); extra thrust shows more on the return

## Battery comparison (cruise ≈ 14 Wh/drop, full throttle 6S ≈ 33 Wh/drop, 80% usable)
| Pack | Weight | Top speed loaded / empty | Drops cruise / full |
|---|---|---|---|
| 4S 5500 LiPo | ~550 g | 0.9–1.1 / 1.5–1.8 m/s | ~4–5 / same |
| 6S 5000 LiPo | ~750 g | 1.2–1.4 / 2+ m/s | ~6 / ~2–3 |
| 6S1P 21700 P42A | ~420 g | 1.15–1.3 / ~2 m/s | ~5 / ~2 |
| 6S2P 21700 P42A (8,400 mAh, ~181 Wh) | ~880 g | 1.2–1.4 / 2+ m/s | ~10 / ~4 |
- Both LiPos (5000+ mAh) likely too long for the 98 mm bay — measure
- 6S2P P42A is ~450–500 g heavier than the stock 10 Ah pack; total upgrade ~750–800 g over stock

## 6S2P sizing
- 4×3 upright brick: ~88–92 × 66–70 × 74–78 mm — fits bay (glue cells, no printed holders; +~10 mm lid for wiring)

## Sourcing (South Africa)
- Molicel P42A (21700, 4200 mAh, 45 A): DIYElectronics (~R209), The Vapery, Vaporworx (~R230), Vanilla Vape
- Akita Custom Batteries (Randburg, 011 704 2429, info@akita.co.za): quoted 6S2P Samsung 30P (6,000 mAh) + 12 A BMS = R2,662 incl VAT
  - Issue: 12 A BMS too small (full throttle ~26 A); they have no 30 A BMS
  - Note: P42A is 45 A per cell — their concern about it was mistaken
  - Fix: ask for **no BMS** (XT60 + 7-pin JST-XH balance lead), or charge-only BMS
- AliExpress best fit: **2× Auline 21700 S70 6S 4500 mAh** (75×64×42 mm, 70 A each) in parallel → ~9,000 mAh, fits bay standing side by side
  - Buy as matched pair, parallel only at equal voltage, XT60 Y-harness; check SA lithium shipping

## ArduPilot Rover setup notes
- Skid steering: `SERVO1/3_FUNCTION = 73/74`, min/trim/max 1000/1500/2000, `MOT_PWM_TYPE = 0`
- ESCs in bidirectional (3D) mode, neutral 1500 µs
- Battery failsafe with RTL: Li-ion ~3.3 V/cell (19.8 V for 6S); set above any BMS cutoff
- Log mAh used per drop to get real drop counts

## Battery level LEDs (plan: options 1 + 3)
- Reuse stock 4 LEDs driven by a small MCU (ATtiny85/Nano/ESP32), divider e.g. 100k/10k, powered from ESC BEC
- Auto-detect 4S/6S at power-up; thresholds per cell: 3 blue ≥3.95, 2 ≥3.80, 1 ≥3.65, red <3.65, flash <3.5 (adjust lower for Li-ion)
- Bypass stock board logic: cut battery feed, isolate LEDs from chip, drive via resistors (150–330 Ω blue, 220–470 Ω red at 5 V)
- Plus Pixhawk battery failsafe as the safety net

## Hull
- Probably fine for now; risks: pod mounting strength under thrust, stern freeboard, ESC heat
- Bath test with ~1 kg ballast + full bait: ≥3 cm freeboard OK, ~2 cm marginal
- Fallback: print hull on K1C (220×220×250 mm) in sections, ASA, epoxy/fibreglass skin

## Next steps
1. Wait for thrusters; bench test with props in water
2. Decide pack: 2× Auline S70 (AliExpress) or no-BMS P42A 6S2P (Akita/DIY)
3. Weigh stock battery; bath/ballast hull test
4. Design printed thruster mounts (20 mm hole spacing) and taller battery lid
5. Configure Rover params + battery failsafe; build LED indicator
