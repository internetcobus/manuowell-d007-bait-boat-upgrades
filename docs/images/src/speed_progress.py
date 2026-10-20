# Draws speed-progress-2026-10-20.png: speed from the stock boat to the kept
# setup. Stock 0.8 m/s is Cobus's figure (docs/01 had "about 0.7 m/s loaded");
# the rest are pool medians at full stick (12 m pool: open water will be faster).
#   python3 speed_progress.py docs/images/speed-progress-2026-10-20.png
import csv, sys, statistics as st
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
STOCK = 0.8
RUNS = [('New thrusters\nno tab, 50 %', 'data/2026-10-20-pool-run-thr50.csv', 50),
        ('10° tab\n55 %', 'data/2026-10-20-pool-run-tab10-thr55.csv', 55),
        ('10° tab + 8° tilt\n60 % (kept)', 'data/2026-10-20-pool-run-tilt8-thr60.csv', 60)]
f = lambda r, k: float(r[k])
def split(R):
    out = {'empty': [], 'loaded': []}; state = None
    for r in R:
        if f(r, 'throttle_pct') < 3: state = 'loaded' if f(r, 'pitch_deg') > -3 else 'empty'
        elif state: out[state].append(r)
    return out
sp, nose = {}, {}
for name, p, top in RUNS:
    R = [r for r in csv.DictReader(open(p)) if r['out1'] and r['volt'] and r['throttle_pct']]
    for k, rows in split(R).items():
        z = [r for r in rows if f(r, 'throttle_pct') >= top - 3]
        sp[name, k] = st.median(f(r, 'groundspeed') for r in z); nose[name, k] = st.median(f(r, 'pitch_deg') for r in z)
ORANGE, BLUE, GREY, GREEN = '#e05a20', '#2a6fe0', '#9a9a9a', '#1a9a3a'
fig, ax = plt.subplots(figsize=(11, 6), dpi=110)
ax.bar(0, STOCK, 0.5, color=GREY); ax.text(0, STOCK + 0.03, '%.2f m/s' % STOCK, ha='center', fontweight='bold', color='#555')
w = 0.36
for j, (name, _, _) in enumerate(RUNS, 1):
    for dx, k, c in ((-w / 2, 'loaded', ORANGE), (w / 2, 'empty', BLUE)):
        v = sp[name, k]; ax.bar(j + dx, v, w, color=c, label=('~1 kg loaded' if k == 'loaded' else 'empty') if j == 1 else None)
        ax.text(j + dx, v + 0.03, '%.2f' % v, ha='center', fontweight='bold', color=c)
        ax.text(j + dx, 0.06, 'nose\n%.0f°' % nose[name, k], ha='center', color='white', fontsize=9, fontweight='bold')
    pct = (sp[name, 'loaded'] / STOCK - 1) * 100
    ax.text(j, max(sp[name, 'loaded'], sp[name, 'empty']) + 0.14, 'loaded %+.0f %%\nvs stock' % pct, ha='center', fontsize=9, color='#333')
ax.axhline(1.0, color=GREEN, ls='--', lw=1.8); ax.text(-0.3, 1.02, 'goal: ~1 m/s loaded (docs/02)', ha='left', color=GREEN, fontweight='bold', fontsize=9)
ax.set_xticks(range(4)); ax.set_xticklabels(['Stock boat\n(your figure)'] + [n for n, _, _ in RUNS])
ax.set_ylabel('Speed (m/s, GPS median at full stick)'); ax.set_ylim(0, 1.75)
ax.set_title('Speed progress: stock → new thrusters → trim tab → tab + tilt (pool, 2026-10-20)', fontweight='bold')
ax.legend(loc='upper left', bbox_to_anchor=(0, 0.92)); fig.tight_layout(); fig.savefig(sys.argv[1])
