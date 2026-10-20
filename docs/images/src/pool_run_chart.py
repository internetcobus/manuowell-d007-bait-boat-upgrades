# Draws pool-run-2026-10-20.png from data/2026-10-20-pool-run.csv:
# nose rise and battery power against throttle, binned in 10 % steps.
#   python3 pool_run_chart.py data/2026-10-20-pool-run.csv docs/images/pool-run-2026-10-20.png
import csv, sys, statistics as st
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = [r for r in csv.DictReader(open(sys.argv[1])) if r['out1'] and r['volt'] and r['throttle_pct']]
REST_PITCH = st.median(float(r['pitch_deg']) for r in R if float(r['throttle_pct']) < 5)
REST_AMPS = st.median(float(r['amps']) for r in R if float(r['throttle_pct']) < 5)
bins = {}
for r in R: bins.setdefault(int(float(r['throttle_pct']) // 10) * 10, []).append(r)
xs = sorted(b for b in bins if b >= 10)
rise = [st.median(float(r['pitch_deg']) for r in bins[b]) - REST_PITCH for b in xs]
watts = [st.median(float(r['volt']) for r in bins[b]) * max(0, st.median(float(r['amps']) for r in bins[b]) - REST_AMPS) for b in xs]
speed = [st.median(float(r['groundspeed']) for r in bins[b]) for b in xs]
lab = ['%d-%d' % (b, b + 9) for b in xs]
fig, ax1 = plt.subplots(figsize=(11.5, 5.8), dpi=110)
ax1.bar(lab, rise, color='#2a6fe0', label='nose rise (deg)')
for i, v in enumerate(rise): ax1.text(i, max(v / 2, 0.3), '%.0f°' % v, ha='center', va='center', color='white' if v > 2 else '#2a6fe0', fontweight='bold')
ax1.set_xlabel('Throttle % (Pixhawk output)'); ax1.set_ylabel('Nose rise above rest (degrees)', color='#2a6fe0')
ax2 = ax1.twinx(); ax2.set_ylim(0, max(watts) * 1.18); ax2.plot(lab, watts, 'o-', color='#e05a20', lw=2.5, label='battery power (W)')
for i, v in enumerate(watts): ax2.text(i - 0.32, v + 6, '%.0f W' % v, ha='center', color='#e05a20', fontsize=9, fontweight='bold')
ax2.set_ylabel('Battery power (W, radio offset removed)', color='#e05a20')
ax3 = ax1.twinx(); ax3.spines['right'].set_position(('axes', 1.11)); ax3.set_ylim(0, max(speed) * 1.18)
ax3.plot(lab, speed, 's--', color='#1a9a3a', lw=2.5)
for i, v in enumerate(speed): ax3.text(i + 0.3, v - 0.07, '%.2f m/s' % v, ha='center', color='#1a9a3a', fontsize=9, fontweight='bold')
ax3.set_ylabel('Speed (m/s, GPS, median)', color='#1a9a3a')
ax1.axvspan(3.5, 5.5, color='#ffd54a', alpha=0.25)
ax1.set_ylim(0, max(rise) * 1.18); ax1.text(4.5, max(rise) * 1.1, 'nose climbs sharply here', ha='center', fontsize=10)
ax1.set_title('Pool run 2026-10-20 (empty): nose rise, power and speed against throttle (12 m pool)', fontweight='bold')
fig.tight_layout(); fig.savefig(sys.argv[2])
