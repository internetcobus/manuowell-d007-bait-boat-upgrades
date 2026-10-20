# Draws pool-tab-2026-10-20.png: nose angle, speed and current at full stick,
# loaded and empty, for no tab at 50 %, the 10° trim tab at 50 %, and at 55 %.
#   python3 pool_tab_compare.py docs/images/pool-tab-2026-10-20.png
import csv, sys, statistics as st
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
RUNS = [('No tab\n50 %', 'data/2026-10-20-pool-run-thr50.csv', 50),
        ('10° tab\n50 %', 'data/2026-10-20-pool-run-tab10.csv', 50),
        ('10° tab\n55 %', 'data/2026-10-20-pool-run-tab10-thr55.csv', 55)]
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
        vals[name, k] = [st.median(f(r, c) for r in z) for c in ('pitch_deg', 'groundspeed', 'amps')]
names = [n for n, _, _ in RUNS]; ORANGE, BLUE = '#e05a20', '#2a6fe0'
fig, axs = plt.subplots(1, 3, figsize=(13, 4.8), dpi=110)
for ax, (i, title, unit, fmtv) in zip(axs, ((0, 'Nose angle', '°', '%.1f°'), (1, 'Speed (GPS)', 'm/s', '%.2f'), (2, 'Current', 'A', '%.1f A'))):
    w = 0.38
    for dx, k, c in ((-w / 2, 'loaded', ORANGE), (w / 2, 'empty', BLUE)):
        ys = [vals[n, k][i] for n in names]
        ax.bar([j + dx for j in range(3)], ys, w, color=c, label='~1 kg loaded' if k == 'loaded' else 'empty')
        for j, y in enumerate(ys): ax.text(j + dx, y + (0.02 * max(ys) if y >= 0 else -0.08 * max(ys)), fmtv % y, ha='center', fontsize=9, color=c, fontweight='bold')
    ax.set_xticks(range(3)); ax.set_xticklabels(names); ax.set_title(title + ' (' + unit + ', median at full stick)', fontweight='bold', fontsize=11)
    ax.axhline(0, color='#555', lw=0.8)
for a in axs: a.set_ylim(0, a.get_ylim()[1] * 1.25)
axs[0].legend(loc='upper right', fontsize=9, ncol=2)
fig.suptitle('Trim tab pool test 2026-10-20 (12 m pool): best = 10° tab at MOT_THR_MAX 50', fontweight='bold')
fig.tight_layout(); fig.savefig(sys.argv[1])
