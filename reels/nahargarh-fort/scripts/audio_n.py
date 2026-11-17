import numpy as np, wave, sys
SR=44100; DUR=53.4; N=int(SR*DUR); t=np.arange(N)/SR
rng=np.random.default_rng(3)
mus=np.zeros(N); sfx=np.zeros(N)
def add(buf,start,sig):
    i=int(start*SR); j=min(N,i+len(sig)); buf[i:j]+=sig[:j-i]
def env(n,a,d):
    x=np.arange(n)/SR; return np.minimum(1,x/a)*np.exp(-x/d)
# --- tanpura drone (D): Pa Sa Sa Sa'(low) pattern
root=146.83
def tanpura(f,dur=2.4):
    n=int(dur*SR); x=np.arange(n)/SR; s=np.zeros(n)
    for h in range(1,14):
        s+= (1/h**0.9)*np.sin(2*np.pi*f*h*x*(1+0.0007*h))*np.exp(-x/(1.2+0.15*h))*(1+0.3*np.sin(2*np.pi*(0.7+h*0.1)*x))
    return s*env(n,0.02,9)
pat=[root*1.5/2, root, root, root/2]
step=0.62
k=0; tt=0.0
while tt<DUR:
    add(mus,tt,0.16*tanpura(pat[k%4])); tt+=step; k+=1
# --- low pad swell
pad=np.zeros(N)
for f in (root/2, root/2*1.5, root):
    pad+=np.sin(2*np.pi*f*t+np.sin(2*np.pi*0.2*t))
mus+=0.05*pad*(0.6+0.4*np.sin(2*np.pi*t/8))
# --- percussion (dhol-ish) after reveal, 97bpm
bpm=108; beat=60/bpm
def kick():
    n=int(0.45*SR); x=np.arange(n)/SR
    f=55+90*np.exp(-x*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-x*7)
def slap():
    n=int(0.2*SR); x=np.arange(n)/SR
    nz=rng.standard_normal(n); nz=np.convolve(nz,np.ones(6)/6,'same')
    return (0.5*nz+np.sin(2*np.pi*330*x))*np.exp(-x*28)
b=0.0; i=0
while b<DUR-0.5:
    if not (13.55<b<15.5):
        pos=i%8
        if pos in (0,3,5): add(mus,b,0.5*kick())
        if pos in (2,6): add(mus,b,0.22*slap())
        if pos in (7,): add(mus,b+beat/2,0.14*slap())
    b+=beat/2; i+=1
# fade
mus*=np.clip(t/1.0,0,1)*np.clip((DUR-t)/1.5,0,1)
# --- SFX
def whoosh(d=0.35):
    n=int(d*SR); x=np.arange(n)/SR; nz=rng.standard_normal(n)
    # sweeping lowpass via cumulative smoothing
    out=np.zeros(n); y=0
    a=np.linspace(0.02,0.35,n)**1.5
    for i_ in range(n): y+=a[i_]*(nz[i_]-y); out[i_]=y
    e=np.sin(np.pi*np.minimum(1,x/d))**2
    return out*e*2.5
def boom():
    n=int(1.6*SR); x=np.arange(n)/SR
    f=38+70*np.exp(-x*6); ph=2*np.pi*np.cumsum(f)/SR
    nz=np.convolve(rng.standard_normal(n),np.ones(40)/40,'same')
    return (np.sin(ph)+0.6*nz*np.exp(-x*5))*np.exp(-x*2.2)
def shutter():
    n=int(0.12*SR); x=np.arange(n)/SR; nz=rng.standard_normal(n)
    return nz*(np.exp(-x*90)+0.6*np.exp(-np.abs(x-0.05)*120))*0.6
def ding():
    n=int(0.6*SR); x=np.arange(n)/SR
    return (np.sin(2*np.pi*1318*x)+0.5*np.sin(2*np.pi*1976*x))*np.exp(-x*7)*0.35
def pop():
    n=int(0.08*SR); x=np.arange(n)/SR
    return np.sin(2*np.pi*(600+2000*x)*x)*np.exp(-x*50)*0.5
W=whoosh(); 
cuts=[1.95,4.05,6.30,9.05,13.55,17.90,20.35,23.00,24.90,26.95,29.25,31.30,33.85,36.60,38.70,42.50,46.00,48.60,51.20]
for c in cuts: add(sfx,c-0.2,0.35*W)
add(sfx,4.12,0.8*boom()); add(sfx,5.74,0.6*boom()); add(sfx,31.3,0.7*boom())
add(sfx,13.6,0.5*whoosh(0.5))
add(sfx,36.6,0.8*shutter())
for c in (2.6,): add(sfx,c,0.6*pop())
for c in (9.4,12.0,20.6,25.0,29.4,31.9,36.75): add(sfx,c,0.5*pop())
import json
ws=json.load(open(sys.argv[1]+'/nwords.json'))
def wt(w): return [o['s'] for o in ws if o['w'].lower().strip(',.!?')==w][0]
for w in ('location','distance','opening-closing','transport'): add(sfx,wt(w),ding())
add(sfx,wt('jaipur!') if False else 47.6,ding()); add(sfx,wt('save'),ding())
def wr(fn,x):
    x=np.clip(x,-1,1); w=wave.open(fn,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
mus/=np.abs(mus).max(); sfx/=max(1,np.abs(sfx).max())
wr(sys.argv[1]+'/music.wav',mus*0.9); wr(sys.argv[1]+'/sfx.wav',sfx*0.9)
