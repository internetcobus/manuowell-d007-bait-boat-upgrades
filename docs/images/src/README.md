# Picture generators

PIL scripts that draw the battery-gauge pictures in `docs/images/`, so they can be changed and redrawn instead of edited by hand:

- `python3 gauge_boards.py docs/images` draws `gauge-led-strip.png` and `gauge-driver-board.png`
- `python3 gauge_connections.py docs/images/gauge-connections.png` (all three pieces and every wire)
- `python3 gauge_stack.py docs/images/gauge-stack.png` (side view of the stack)
- `python3 gauge_wiring.py docs/images/gauge-wiring.png`
- `python3 gauge_c3_harness.py docs/images/gauge-c3-harness.png` labels a copy of Cobus's photo `/mnt/hgfs/Temp/20261016_122206.jpg` (the photo itself is not in the repo)
- `python3 pm06_current_filter.py docs/images/pm06-current-filter.png` (the 10k + 100 nF current filter that was tried on 2026-10-19 and did not help)
- `python3 pool_run_chart.py data/2026-10-20-pool-run.csv docs/images/pool-run-2026-10-20.png` (empty pool run: nose rise, power, speed by throttle)
- `python3 pool_run_compare.py data/2026-10-20-pool-run.csv data/2026-10-20-pool-run-1kg.csv docs/images/pool-run-2026-10-20-compare.png` (nose angle and speed, empty vs ~1 kg)
- `python3 pool_tab_compare.py docs/images/pool-tab-2026-10-20.png` (trim tab test: nose, speed, current; no tab / 10° tab at 50 % / at 55 %)
- `python3 pool_setup_compare.py docs/images/pool-setups-2026-10-20.png` (every pool setup of 2026-10-20: nose, speed, current, energy per metre)
- `python3 speed_progress.py docs/images/speed-progress-2026-10-20.png` (speed: stock 0.8 m/s → new thrusters → tab → tab + tilt at 60 %)
