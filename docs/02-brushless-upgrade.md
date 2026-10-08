# Brushless upgrade

## Goal

About **1 m/s loaded outbound** (now about 0.7 m/s) so the fishing lines sag less, which is a thrust problem. About 2 m/s empty on the return is a bonus. Loaded speed is capped by hull speed, about 0.9-1 m/s for a hull this size, so the extra thrust shows more on the return.

## Thrusters (ordered, AliExpress)

Brushless, ducted, 4-blade, CW/CCW pair:

- **480 Kv**, 12-24 V, 13 A, 30-200 W, about **2 kg thrust each at 24 V**
- 162 g each, 75 mm long, **62 mm diameter** (duct opening measured 2026-10-08), 250 mm leads
- Mounting: **three 3 mm holes in a straight line along the top, 20 mm apart** (Cobus, 2026-10-08). Threaded or plain not yet checked. The [thruster mount](../designs/thruster-mount/) uses the outer pair.

A different listing, [KINGMODEL 4000074645091](https://www.aliexpress.com/item/4000074645091.html), was looked at on 2026-10-08. It describes 1000 KV / 20 A / 74 mm thrusters with a PLA shell and a semi-submersible prop. The 62 mm measurement shows these are not those thrusters, so ignore that listing's figures.

## ESCs (ordered)

Two BLHeli ESCs: **40 A (50 A burst), 2S-6S, 5 V / 3 A BEC, bidirectional**, programmable. They replace the CL9030s, which are brushed only.

## Power module

Holybro **PM06**, on hand, not fitted yet. Per [Holybro's PM06 V2 specs](https://www.getfpv.com/electronics/autopilot-systems/pm06-14s-power-module.html): 2S-14S, 60 A rated (120 A for under 60 s), 5.1-5.3 V / 3 A output to the Pixhawk, XT60 on 12 AWG (rated 30 A continuous, 60 A for under a minute), 35 × 35 mm, 24 g. The original PM06 (V1) is 2S-6S. Either version covers 6S.

- **Connector:** the PM06 has a 6-pin **JST-GH** cable; the Pixhawk 2.4.8 power port is a 6-pin **DF13**. An adapter cable is needed.
- The XT60 lead is rated 30 A continuous. Full throttle on 6S is about 26 A in total, so that's within its rating but close.

## Why 6S

The rated thrust is at 24 V. 4S gives only about 0.75-1 kg per thruster; 6S about 1.7 kg. A full 6S pack is 25.2 V, slightly over the 24 V rating, so cap `MOT_THR_MAX` at about 90%.

## Battery options

Energy: about 14 Wh per drop at cruise, about 33 Wh per drop at full throttle on 6S. Plan on 80% of the pack being usable.

| Pack | Weight | Top speed loaded / empty | Drops cruise / full |
|---|---|---|---|
| 4S 5500 LiPo | ~550 g | 0.9-1.1 / 1.5-1.8 m/s | ~4-5 / same |
| 6S 5000 LiPo | ~750 g | 1.2-1.4 / 2+ m/s | ~6 / ~2-3 |
| 6S1P 21700 P42A | ~420 g | 1.15-1.3 / ~2 m/s | ~5 / ~2 |
| 6S2P 21700 P42A (8,400 mAh, ~181 Wh) | ~880 g | 1.2-1.4 / 2+ m/s | ~10 / ~4 |

- Both LiPos (5000+ mAh) are probably too long for the 98 mm bay. Measure first.
- A 6S2P P42A pack is about 450-500 g heavier than the stock pack; the whole upgrade is about 750-800 g over stock.
- **6S2P fit:** a 4 × 3 upright brick is about 88-92 × 66-70 × 74-78 mm and fits the bay. Glue the cells, no printed holders; a lid about 10 mm taller for the wiring.

## Sourcing (South Africa)

- **Molicel P42A** (21700, 4200 mAh, 45 A): DIYElectronics (~R209), The Vapery, Vaporworx (~R230), Vanilla Vape.
- **Akita Custom Batteries** (Randburg, 011 704 2429, info@akita.co.za) quoted a 6S2P Samsung 30P (6,000 mAh) with a 12 A BMS for R2,662 incl. VAT.
  - The 12 A BMS is too small: full throttle is about 26 A. They have no 30 A BMS.
  - Their concern about the P42A was mistaken; it is rated 45 A per cell.
  - Fix: ask for **no BMS** (XT60 plus a 7-pin JST-XH balance lead) or a charge-only BMS.
- **AliExpress best fit:** 2× **Auline 21700 S70 6S 4500 mAh** (75 × 64 × 42 mm, 70 A each) in parallel, about 9,000 mAh, standing side by side in the bay.
  - Buy a matched pair, parallel them only at equal voltage, with an XT60 Y-harness.
  - Check whether lithium ships to South Africa.

## Hull

Probably fine for now. Risks: pod mounting strength under thrust, stern freeboard, ESC heat.

- **Bath test:** about 1 kg of ballast plus a full bait load. 3 cm or more of freeboard is OK; about 2 cm is marginal.
- **Fallback:** print a hull on the K1C (220 × 220 × 250 mm bed) in sections, in ASA, with an epoxy or fibreglass skin.
