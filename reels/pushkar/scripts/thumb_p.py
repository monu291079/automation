from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
import numpy as np, sys
S=sys.argv[1]; OUT=sys.argv[2]
W,H=1080,1920
F=lambda n,s: ImageFont.truetype(f'{S}/fonts/{n}.ttf',s)
im=Image.open(f'{S}/pprep/9244.jpg'); m=Image.open(f'{S}/pprep/9244_m.png')
# crop: zoom so couple big, lower-center
z=1.0; s0=max(W/im.width,H/im.height); ww,hh=W/(s0*z),H/(s0*z)
cx,cy=.5*im.width,.5*im.height; box=(cx-ww/2,cy-hh/2,cx+ww/2,cy+hh/2)
bg=im.resize((W,H),Image.LANCZOS,box=box); mk=m.resize((W,H),Image.LANCZOS,box=box)
bg=ImageEnhance.Color(bg).enhance(1.35); bg=ImageEnhance.Contrast(bg).enhance(1.12)
# warm sky tint gradient top + dark bottom
g=np.linspace(0,1,H)[:,None]
arr=np.asarray(bg).astype(np.float32)
top=np.clip(1-g/0.45,0,1)[...,None]; arr=arr*(1-0.35*top)+np.array([255,140,40])*0.35*top
bot=np.clip((g-0.62)/0.38,0,1)[...,None]; arr=arr*(1-0.75*bot)
bg=Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
subj=bg.copy()
def txt(t,font,fill,stroke=0,sf=(0,0,0),sp=0):
    d=ImageDraw.Draw(Image.new('L',(1,1)))
    ws=[d.textlength(c,font=font)+sp for c in t]; tw=int(sum(ws)-sp); a,de=font.getmetrics()
    P=40+stroke; L=Image.new('RGBA',(tw+2*P,a+de+2*P),(0,0,0,0)); dd=ImageDraw.Draw(L); x=P
    for c,w in zip(t,ws): dd.text((x,P),c,font=font,fill=fill,stroke_width=stroke,stroke_fill=sf); x+=w
    return L
def grad(L,c1,c2):
    g=Image.linear_gradient('L').resize(L.size)
    col=Image.composite(Image.new('RGBA',L.size,c2+(255,)),Image.new('RGBA',L.size,c1+(255,)),g); col.putalpha(L.getchannel('A')); return col
def glow(L,col,r=18,a=200):
    gl=Image.new('RGBA',L.size,col+(0,)); gl.putalpha(L.getchannel('A').point(lambda v:int(v*a/255))); return gl.filter(ImageFilter.GaussianBlur(r))
def paste(base,L,cx,cy): base.alpha_composite(L,(int(cx-L.width/2),int(cy-L.height/2)))
can=bg.convert('RGBA')
# BEHIND: AMER FORT huge
amer=grad(txt('PUSHKAR',F('Anton-Regular',300),(255,255,255),sp=6),(255,245,180),(255,110,20))
if amer.width-80>W-40: amer=amer.resize((W-40+80,int(amer.height*(W-40+80)/amer.width)),Image.LANCZOS)
for L,y in ((amer,470),):
    sh=Image.new('RGBA',L.size,(0,0,0,0)); sh.putalpha(L.getchannel('A').point(lambda v:int(v*.55))); sh=sh.filter(ImageFilter.GaussianBlur(14))
    paste(can,sh,W/2,y+12); paste(can,L,W/2,y)
can=Image.composite(subj.convert('RGBA'),can,mk)
# FRONT: hook pill top
d=ImageDraw.Draw(can)
hook=txt('DUNIYA KA SABSE MASHHOOR',F('Montserrat-Black',46),(255,255,255),sp=3)
pw=hook.width; d.rounded_rectangle((W/2-pw/2,175,W/2+pw/2,275),50,fill=(200,30,30,255))
paste(can,hook,W/2,228)
# bottom headline
l1=txt('BRAHMA',F('Anton-Regular',150),(255,255,255),stroke=8,sf=(40,10,0))
l2=grad(txt('MANDIR!',F('Anton-Regular',210),(255,255,255),sp=6),(255,230,90),(255,120,20))
o2=txt('MANDIR!',F('Anton-Regular',210),(40,10,0),stroke=10,sf=(40,10,0),sp=6)
paste(can,glow(l1,(0,0,0),20,220),W/2,1360); paste(can,l1,W/2,1360)
paste(can,o2,W/2,1555); paste(can,l2,W/2,1555)
# badge circle
bx,by,r=880,1130,120
d=ImageDraw.Draw(can); d.ellipse((bx-r,by-r,bx+r,by+r),fill=(255,196,46),outline=(255,255,255),width=8)
for t,y,sz in (('2 DIN',by-28,70),('PLAN',by+38,40)):
    L=txt(t,F('Anton-Regular',sz),(60,20,0)); paste(can,L,bx,y)
# bottom strip
ft=txt('PUSHKAR GUIDE  👉  COMMENT "PUSHKAR"'.replace('  👉  ',' • '),F('Montserrat-Black',31),(255,255,255),sp=1)
d.rounded_rectangle((W/2-ft.width/2+18,1695,W/2+ft.width/2-18,1771),42,fill=(0,0,0,170),outline=(255,196,46),width=4)
paste(can,ft,W/2,1733)
can.convert('RGB').save(OUT,quality=95)
