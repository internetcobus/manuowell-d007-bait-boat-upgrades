from PIL import Image, ImageDraw, ImageFont
import sys
F=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',s)
B=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s)
W,H=1460,780; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
d.text((20,12),'Battery gauge: wiring',fill='black',font=B(28))
def box(x,y,w,h,t,fill,tc='black'):
    d.rounded_rectangle((x,y,x+w,y+h),8,fill=fill,outline='#333',width=2); d.multiline_text((x+10,y+8),t,fill=tc,font=B(16),spacing=4)
def line(pts,c='black',w=3): d.line(pts,fill=c,width=w)
def res(x,y,t,vert=False):
    if vert: d.rectangle((x-9,y-28,x+9,y+28),fill='#e8d3a9',outline='#333'); d.text((x+14,y-9),t,font=F(15),fill='#333')
    else: d.rectangle((x-30,y-9,x+30,y+9),fill='#e8d3a9',outline='#333'); d.text((x-24,y-32),t,font=F(15),fill='#333')
def gnd(x,y):
    line([(x,y),(x,y+10)]);
    for i,w in enumerate((16,10,4)): line([(x-w,y+10+i*5),(x+w,y+10+i*5)],w=2)
# left: boat side
box(20,90,250,90,'6S pack (+)\nafter the switch:\nESC + or PM06 out',"#ffe0e0")
box(20,330,250,80,'ESC that does NOT\npower the Pixhawk:\n5 V BEC lead','#e0f0ff')
# 330k at the battery end
line([(270,135),(350,135)],'#c00000'); res(380,135,'330k'); line([(410,135),(560,135)],'#b06000')
d.text((300,160),'330k soldered at the battery end,\nheat-shrunk: the sense wire then\ncarries no current if it chafes',fill='#c00000',font=F(14))
# board
box(560,70,880,680,'',"#f6efe0"); d.text((575,78),'Driver board + C3 Zero (the LEDs are on their own strip at the hull holes)',font=B(19),fill='black')
# divider
line([(560,135),(700,135)],'#b06000'); d.ellipse((694,129,706,141),fill='black')
line([(700,135),(700,200)]); res(700,230,'10k',True); line([(700,258),(700,300)]); gnd(700,300)
line([(700,135),(790,135)]); line([(790,135),(790,195)]); d.rectangle((775,198,805,203),fill='#333'); d.rectangle((775,210,805,215),fill='#333'); d.text((812,197),'100n',font=F(15),fill='black'); line([(790,215),(790,300)]); gnd(790,300)
line([(700,135),(940,135)]); box(940,100,200,320,'ESP32-C3\nZero\n\nGP3 (ADC)\n\nGP4  LED 1 (red)\nGP5  LED 2\nGP6  LED 3\nGP7  LED 4\n\n5V   GND','#2a5fb0','white')
d.text((800,112),'0.74 V at 25.2 V',font=F(13),fill='#555')
# power
line([(270,360),(960,360)],'#e03030'); line([(960,360),(960,440),(1040,440),(1040,420)],'#e03030'); d.text((300,336),'BEC red = 5 V',font=F(14),fill='#e03030')

line([(270,390),(930,390)],'#222'); line([(930,390),(930,455),(1100,455),(1100,420)],'#222'); d.text((300,396),'BEC black = GND (same as battery -)',font=F(14),fill='#222')

# one LED channel
x0=620; y0=470
d.text((x0-40,y0-12),'x4 (one per LED):',font=B(16),fill='black')

line([(x0+430,y0+10),(x0+430,y0+40)],'#e03030'); d.text((x0+440,y0+8),'5 V',font=F(14),fill='#e03030')
res(x0+430,y0+115,'330',True)
# LED
d.polygon([(x0+415,y0+45),(x0+445,y0+45),(x0+430,y0+70)],fill='#2a6fe0'); line([(x0+415,y0+71),(x0+445,y0+71)],w=3)
d.text((x0+452,y0+46),'LED on the LED strip (5 V common)',font=F(14),fill='#2a6fe0')
line([(x0+430,y0+40),(x0+430,y0+45)]); line([(x0+430,y0+71),(x0+430,y0+87)]); line([(x0+430,y0+143),(x0+430,y0+155)])
# transistor
d.ellipse((x0+380,y0+150,x0+450,y0+220),outline='black',width=2)
line([(x0+400,y0+165),(x0+400,y0+205)],w=4); line([(x0+400,y0+175),(x0+430,y0+155)]); line([(x0+400,y0+195),(x0+430,y0+215)])
d.text((x0+455,y0+170),'BC547',font=B(14),fill='black'); d.text((x0+436,y0+150),'C',font=F(12),fill='black'); d.text((x0+436,y0+205),'E',font=F(12),fill='black'); d.text((x0+383,y0+190),'B',font=F(12),fill='black')
line([(x0+430,y0+215),(x0+430,y0+228)]); gnd(x0+430,y0+228)
line([(x0+100,y0+185),(x0+330,y0+185)]); res(x0+240,y0+185,'10k'); line([(x0+330,y0+185),(x0+400,y0+185)])
d.text((x0+60,y0+175),'GPx',font=B(15),fill='black'); d.text((x0+40,y0+205),'HIGH = LED on',font=F(13),fill='#555')
im.save(sys.argv[1])
