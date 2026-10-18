# Picture generators

PIL scripts that draw the battery-gauge pictures in `docs/images/`, so they can be changed and redrawn instead of edited by hand:

- `python3 gauge_boards.py docs/images` draws `gauge-led-strip.png` and `gauge-driver-board.png`
- `python3 gauge_connections.py docs/images/gauge-connections.png` (all three pieces and every wire)
- `python3 gauge_stack.py docs/images/gauge-stack.png` (side view of the stack)
- `python3 gauge_wiring.py docs/images/gauge-wiring.png`
- `python3 gauge_c3_harness.py docs/images/gauge-c3-harness.png` labels a copy of Cobus's photo `/mnt/hgfs/Temp/20261016_122206.jpg` (the photo itself is not in the repo)
