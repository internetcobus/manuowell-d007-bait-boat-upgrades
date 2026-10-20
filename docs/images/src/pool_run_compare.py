# Draws pool-run-2026-10-20-compare.png: nose angle (absolute, Pixhawk pitch)
# and speed against throttle, empty vs ~1 kg in the hoppers, two panels.
#   python3 pool_run_compare.py data/2026-10-20-pool-run.csv data/2026-10-20-pool-run-1kg.csv docs/images/pool-run-2026-10-20-compare.png
import csv, sys, statistics as st
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

def binned(p):
    R = [r for r in csv.DictReader(open(p)) if r['out1'] and r['volt'] and r['throttle_pct']]
    pitch, speed = {}, {}
    for r in R:
        k = int(float(r['throttle_pct']) // 10) * 10
        pitch.setdefault(k, []).append(float(r['pitch_deg']))
        speed.setdefault(k, []).append(float(r['groundspeed']))
    rest = st.median(pitch[0])
    return (round(rest) + 0, {k: st.median(v) for k, v in pitch.items() if k >= 10},
            {k: st.median(v) for k, v in speed.items() if k >= 10})

(re, pe, se), (rl, pl, sl) = binned(sys.argv[1]), binned(sys.argv[2])
xs = sorted(set(pe) | set(pl)); lab = ['%d-%d' % (x, x + 9) for x in xs]
BLUE, ORANGE, GREEN = '#2a6fe0', '#e05a20', '#1a9a3a'
fig, (ax, bx) = plt.subplots(2, 1, figsize=(10, 8), dpi=110, sharex=True, gridspec_kw={'height_ratios': [3, 2]})
w = 0.38
ax.bar([i - w / 2 for i in range(len(xs))], [pe.get(x, 0) for x in xs], w, color=BLUE, label='empty (rest %d°)' % re)
ax.bar([i + w / 2 for i in range(len(xs))], [pl.get(x, 0) for x in xs], w, color=ORANGE, label='~1 kg in hoppers (rest %d°)' % rl)
for i, x in enumerate(xs):
    for dx, d, c in ((-w / 2, pe, BLUE), (w / 2, pl, ORANGE)):
        if x in d: ax.text(i + dx, d[x] + (0.6 if d[x] >= 0 else -1.8), '%.0f°' % d[x], ha='center', color=c, fontsize=9, fontweight='bold')
ax.axhline(0, color='#555', lw=1)
ax.set_ylabel('Nose angle (degrees)')
ax.set_title('Pool runs 2026-10-20: nose angle and speed, empty vs ~1 kg in the hoppers', fontweight='bold')
ax.legend(loc='upper left')
for i, (d, c, name) in enumerate(((se, BLUE, 'empty'), (sl, ORANGE, '~1 kg'))):
    ys = [d.get(x) for x in xs]
    bx.plot(range(len(xs)), ys, 's-', color=c, lw=2.5, label=name)
    for j, v in enumerate(ys):
        if v is not None: bx.text(j, v + (0.07 if i == 0 else -0.13), '%.2f' % v, ha='center', color=c, fontsize=9, fontweight='bold')
bx.set_ylim(0, max(list(se.values()) + list(sl.values())) * 1.25)
bx.set_ylabel('Speed (m/s, GPS median)'); bx.legend(loc='upper left')
bx.set_xticks(range(len(xs))); bx.set_xticklabels(lab); bx.set_xlabel('Throttle % (Pixhawk output)')
for a in (ax, bx): a.axvline(3.5, color=GREEN, ls='--', lw=2)
ax.text(3.55, ax.get_ylim()[1] * 0.9, 'MOT_THR_MAX 50\n(set 2026-10-20)', ha='left', color=GREEN, fontweight='bold')
fig.tight_layout(); fig.savefig(sys.argv[3])
