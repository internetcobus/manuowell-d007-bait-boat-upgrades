# Draws pool-setups-2026-10-20.png: nose angle, speed and current at full stick,
# loaded and empty, for every setup tried in the pool on 2026-10-20, plus the
# energy per metre (current / speed) that sets the drops per charge.
#   python3 pool_setup_compare.py docs/images/pool-setups-2026-10-20.png
import csv, sys, statistics as st
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
RUNS = [('No tab\n50 %', 'data/2026-10-20-pool-run-thr50.csv', 50),
        ('Tab\n50 %', 'data/2026-10-20-pool-run-tab10.csv', 50),
        ('Tab+tilt\n50 %', 'data/2026-10-20-pool-run-tilt8.csv', 50),
        ('Tab+tilt\n60 %', 'data/2026-10-20-pool-run-tilt8-thr60.csv', 60),
        ('Tab+tilt\n65 %', 'data/2026-10-20-pool-run-tilt8-thr65.csv', 65)]
CHOSEN = 3   # index of the setup kept (tab + tilt at 60 %)
f = lambda r, k: float(r[k])
def split(R):   # loaded/empty from the rest pitch before each run (loaded rests about 0°, empty about -6°)
    out = {'empty': [], 'loaded': []}; state = None
    for r in R:
        if f(r, 'throttle_pct') < 3: state = 'loaded' if f(r, 'pitch_deg') > -3 else 'empty'
        elif state: out[state].append(r)
    return out
vals = {}
for name, p, top in RUNS:
    R = [r for r in csv.DictReader(open(p)) if r['out1'] and r['volt'] and r['throttle_pct']]
    for k, rows in split(R).items():
        z = [r for r in rows if f(r, 'throttle_pct') >= top - 3]
        pm, sp, am = (st.median(f(r, c) for r in z) for c in ('pitch_deg', 'groundspeed', 'amps'))
        vals[name, k] = [pm, sp, am, am / sp]
names = [n for n, _, _ in RUNS]; ORANGE, BLUE, GREEN = '#e05a20', '#2a6fe0', '#1a9a3a'
fig, axs = plt.subplots(2, 2, figsize=(14, 9), dpi=105)
panels = ((0, 'Nose angle (°)', '%.1f°'), (1, 'Speed, GPS (m/s)', '%.2f'), (2, 'Current (A)', '%.1f'), (3, 'Energy per metre (A per m/s: lower = more drops)', '%.1f'))
for ax, (i, title, fmtv) in zip(axs.flat, panels):
    w = 0.38
    for dx, k, c in ((-w / 2, 'loaded', ORANGE), (w / 2, 'empty', BLUE)):
        ys = [vals[n, k][i] for n in names]
        ax.bar([j + dx for j in range(len(names))], ys, w, color=c, label='~1 kg loaded' if k == 'loaded' else 'empty')
        for j, y in enumerate(ys): ax.text(j + dx, y + 0.02 * max(ys), fmtv % y, ha='center', fontsize=8.5, color=c, fontweight='bold')
    ax.axvspan(CHOSEN - 0.5, CHOSEN + 0.5, color='#ffd54a', alpha=0.25)
    ax.set_xticks(range(len(names))); ax.set_xticklabels(names, fontsize=9)
    ax.set_title(title + ', median at full stick', fontweight='bold', fontsize=11)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.2)
axs[0][0].axhline(15, color=GREEN, ls='--', lw=1.5); axs[0][0].text(1.55, 15.4, 'loaded limit ~15°', color=GREEN, fontsize=9, fontweight='bold')
axs[0][0].legend(loc='upper right', fontsize=9, ncol=2)
fig.suptitle('Pool tests 2026-10-20 (12 m pool, 6S2P): kept = 10° trim tab + 8° tilt at MOT_THR_MAX 60 (yellow)', fontweight='bold')
fig.tight_layout(); fig.savefig(sys.argv[1])
