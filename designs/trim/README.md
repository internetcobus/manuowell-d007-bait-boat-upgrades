# Trim tab (centre, transom)

Bolt-on plate under the hull's centre V, sticking out 35 mm behind the transom with its trailing edge angled down, so the water lifts the stern and lowers the nose near hull speed. Source: [`trim_tab.scad`](trim_tab.scad) (header has the WHY, geometry and fixing).

- **Fitted 2026-10-20: the 10° version** (`stl/trim_tab_10.stl`). Results in [docs/03](../../docs/03-ardupilot-setup.md#throttle-limit-from-the-pool-runs-2026-10-20).
- **Fixing:** two ears under the bases' EXISTING inboard aft post screws (12 mm forward of the transom, 99.5 mm apart, found with the fit gauge). ST2.9 × 13 keeps ~4.5 mm in the post; ST2.9 × 16 to keep it on for good.
- **Hull shape (Cobus, 2026-10-20):** the bases' underside is 4 mm deeper than the V's edges; the keel 12 mm deeper than the edges.
- `stl/`: `trim_tab_00/05/10.stl` (flush, 5°, 10°), `trim_tab_fit_gauge.stl`. Print ASA/ABS, hull face on the bed, a little support under the V.
- `measure/`: Cobus's photos and sketches (`*_cobus.*`, never overwrite) and my labelled copies.
- Ideas not tried: a longer tab (50 mm, ~40 % more lift), smoothing the bottom scoops (tape test first), a buoyant stern pod.
