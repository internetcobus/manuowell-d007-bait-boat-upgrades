from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
F=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',s)
B=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s)
src=Image.open('/mnt/hgfs/Temp/20261016_122206.jpg').convert('RGB')
S=3; x0,y0=300,330
c=src.crop((x0,y0,485,560)); c=c.resize((c.width*S,c.height*S),Image.LANCZOS); c=ImageEnhance.Sharpness(c).enhance(1.6)
W,H=1400,850; im=Image.new('RGB',(W,H),'white'); ox,oy=380,60; im.paste(c,(ox,oy)); d=ImageDraw.Draw(im)
d.text((20,12),'C3 Zero harness: solder to the header pin tips (board FACE-DOWN, this side up)',fill='black',font=B(24))
# pin positions in crop px (2x crop measured): rows y = 60 + 43.2*i, left x ~30, right x ~322
L=lambda i: (ox+int(30/2*S), oy+int((60+43.6*i)/2*S))
R=lambda i: (ox+int(322/2*S), oy+int((60+43.6*i)/2*S))
right=['5V','GND','3V3','GP0','GP1','GP2','GP3','GP4','GP5']
left=['GP21','GP20','GP19','GP18','GP10','GP9','GP8','GP7','GP6']
use_r={'5V':('#ff7a00','from driver P5 (5 V)'),'GND':('#777','from driver P2 (GND)'),'GP3':('#f0a000','from driver O5 (battery sense)'),
       'GP4':('#d22','from driver A6 (LED 1, red)'),'GP5':('#2a6fe0','from driver D6 (LED 2)')}
use_l={'GP7':('#9a3ad0','from driver J6 (LED 4)'),'GP6':('#1a9a3a','from driver G6 (LED 3)')}
for i,n in enumerate(right):
    if n in use_r:
        col,t=use_r[n]; x,y=R(i); d.ellipse((x-14,y-14,x+14,y+14),outline=col,width=5)
        d.line((x+16,y,ox+c.width+40,y),fill=col,width=3); d.text((ox+c.width+48,y-12),n+'  '+t,fill=col,font=B(19))
for i,n in enumerate(left):
    if n in use_l:
        col,t=use_l[n]; x,y=L(i); d.ellipse((x-14,y-14,x+14,y+14),outline=col,width=5)
        d.line((x-16,y,ox-30,y),fill=col,width=3); tw=d.textlength(t+'  '+n,font=B(19)); d.text((ox-38-tw,y-12),t+'  '+n,fill=col,font=B(19))
d.multiline_text((20,H-90),"USB-C end at the top stays free for reflashing. Stick the board down face-down on thick foam tape, higher up and away\nfrom the hull bottom. Keep the other pins clear; a short piece of 7-core ribbon cable, ~10 cm, keeps the harness neat.",fill='#333',font=F(17),spacing=6)
im.save(sys.argv[1])
