from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np, sys
S=sys.argv[1]; OUT=sys.argv[2]; W,H=1080,1920
F=lambda n,s: ImageFont.truetype(f'{S}/fonts/{n}.ttf',s)
bg=Image.open(f'{S}/n/night.png').convert('RGB')
bg=ImageEnhance.Brightness(bg).enhance(1.25); bg=ImageEnhance.Color(bg).enhance(1.4)
# warm sky glow gradient top
arr=np.asarray(bg).astype(np.float32); g=np.linspace(0,1,H)[:,None]
top=np.clip(1-g/0.5,0,1)[...,None]**1.3
arr=arr*(1-0.55*top)+np.array([255,110,60])*0.55*top
bg=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).convert('RGBA')
im=Image.open(f'{S}/nprep/8951.jpg'); m=Image.open(f'{S}/nprep/8951_m.png')
# cutout: subject scaled to width 1180, aligned bottom
sc=1180/im.width; im=im.resize((1180,int(im.height*sc)),Image.LANCZOS); m=m.resize(im.size,Image.LANCZOS)
cut=im.convert('RGBA'); cut.putalpha(m)
cut=ImageEnhance.Brightness(cut).enhance(1.08)
yoff=H-int(cut.height*0.80)
# rim glow behind subject
glow=Image.new('RGBA',cut.size,(255,170,60,0)); glow.putalpha(m.point(lambda v:int(v*0.55))); glow=glow.filter(ImageFilter.GaussianBlur(26))
def txt(t,font,fill,stroke=0,sf=(0,0,0),sp=0):
    d=ImageDraw.Draw(Image.new('L',(1,1)))
    ws=[d.textlength(c,font=font)+sp for c in t]; tw=int(sum(ws)-sp); a,de=font.getmetrics()
    P=40+stroke; L=Image.new('RGBA',(tw+2*P,a+de+2*P),(0,0,0,0)); dd=ImageDraw.Draw(L); x=P
    for c,w in zip(t,ws): dd.text((x,P),c,font=font,fill=fill,stroke_width=stroke,stroke_fill=sf); x+=w
    return L
def grad(L,c1,c2):
    g=Image.linear_gradient('L').resize(L.size)
    col=Image.composite(Image.new('RGBA',L.size,c2+(255,)),Image.new('RGBA',L.size,c1+(255,)),g); col.putalpha(L.getchannel('A')); return col
def paste(base,L,cx,cy): base.alpha_composite(L,(int(cx-L.width/2),int(cy-L.height/2)))
def fit(L,w):
    return L if L.width<=w else L.resize((w,int(L.height*w/L.width)),Image.LANCZOS)
can=bg
# behind subject: NAHARGARH huge
nah=fit(grad(txt('NAHARGARH',F('Anton-Regular',330),(255,255,255),sp=4),(255,240,170),(255,110,30)),W+60)
sh=Image.new('RGBA',nah.size,(0,0,0,0)); sh.putalpha(nah.getchannel('A').point(lambda v:int(v*.6))); sh=sh.filter(ImageFilter.GaussianBlur(16))
paste(can,sh,W/2,560); paste(can,nah,W/2,545)
can.alpha_composite(glow,(W//2-cut.width//2,yoff)); can.alpha_composite(cut,(W//2-cut.width//2,yoff))
d=ImageDraw.Draw(can)
hook=txt('JAIPUR KA SABSE',F('Montserrat-Black',56),(255,255,255),sp=4)
d.rounded_rectangle((W/2-hook.width/2,190,W/2+hook.width/2,290),50,fill=(200,30,30,255)); paste(can,hook,W/2,243)
l1=txt('SHAANDAAR VIEW!',F('Anton-Regular',150),(255,255,255),stroke=8,sf=(40,10,0))
l1=fit(l1,W-10); paste(can,l1,W/2,800)
# badge
bx,by,r=935,985,95
d.ellipse((bx-r,by-r,bx+r,by+r),fill=(255,196,46),outline=(255,255,255),width=8)
for t_,y,sz in (('SUNSET',by-30,46),('+ NIGHT',by+30,40)): paste(can,txt(t_,F('Anton-Regular',sz),(60,20,0)),bx,y)
ft=txt('JAIPUR GUIDE • COMMENT "JAIPUR"',F('Montserrat-Black',34),(255,255,255),sp=1)
d.rounded_rectangle((W/2-ft.width/2+18,1695,W/2+ft.width/2-18,1771),40,fill=(0,0,0,190),outline=(255,196,46),width=4); paste(can,ft,W/2,1733)
can.convert('RGB').save(OUT,quality=95)
