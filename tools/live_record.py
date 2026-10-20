# Live recorder for the pool test: python3 live_record.py <seconds> <out.csv>
# Connects through the MAVProxy relay (udpin 14561), asks for ATTITUDE /
# SERVO_OUTPUT_RAW / RC_CHANNELS / VFR_HUD at 10 Hz (temporary, gone at reboot),
# and writes one CSV row per ATTITUDE with the latest of everything else.
import sys, time, math, csv
from pymavlink import mavutil
dur=float(sys.argv[1]); out=sys.argv[2]
m=mavutil.mavlink_connection('udpin:127.0.0.1:14561',source_system=250); m.wait_heartbeat(timeout=30)
for msgid in (30, 36, 65, 74):   # ATTITUDE, SERVO_OUTPUT_RAW, RC_CHANNELS, VFR_HUD
    m.mav.command_long_send(1,1,mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,0,msgid,100000,0,0,0,0,0)
last={}; t0=time.time(); n=0
with open(out,'w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['t','pitch_deg','roll_deg','out1','out3','rc3','rc1','groundspeed','throttle_pct','volt','amps'])
    while time.time()-t0<dur:
        r=m.recv_match(type=['ATTITUDE','SERVO_OUTPUT_RAW','RC_CHANNELS','VFR_HUD','SYS_STATUS'],blocking=True,timeout=2)
        if not r or r.get_srcSystem()!=1: continue
        last[r.get_type()]=r
        if r.get_type()!='ATTITUDE': continue
        s=last.get('SERVO_OUTPUT_RAW'); c=last.get('RC_CHANNELS'); v=last.get('VFR_HUD'); b=last.get('SYS_STATUS')
        w.writerow([round(time.time()-t0,2),round(math.degrees(r.pitch),2),round(math.degrees(r.roll),2),
                    s.servo1_raw if s else '',s.servo3_raw if s else '',c.chan3_raw if c else '',c.chan1_raw if c else '',
                    round(v.groundspeed,2) if v else '',v.throttle if v else '',b.voltage_battery/1000 if b else '',b.current_battery/100 if b else ''])
        n+=1
        if n%10==0: fh.flush()
        if n%100==0: print('%.0fs rows %d pitch %.1f out1 %s'%(time.time()-t0,n,math.degrees(r.pitch),s.servo1_raw if s else '-'),flush=True)
print('done',n)
