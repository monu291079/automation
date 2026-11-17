import json,re,sys
segs=[(0,1.55),(1.78,6.05),(6.63,7.87),(8.28,9.07),(9.83,12.89),(13.10,15.02),(15.22,17.41),(17.88,23.01),(23.75,25.37),(25.83,27.13),(27.48,29.17),(29.59,32.16),(33.11,35.07),(35.46,38.16),(38.81,41.44),(41.78,43.85),(44.24,46.05),(46.43,47.69),(48.01,51.27),(51.70,53.29),(53.86,55.13),(55.60,58.62)]
# (segment indices, text)  — '*' marks highlight keyword
groups=[
 ([0],"Jaipur mein ek aisi jagah hai…"),
 ([1],"jahan kadam rakhte hi aapko lagega ki aap kisi Raja-Maharaja ke daur mein pahunch gaye hain!"),
 ([2],"Aur us jagah ka naam hai…"),
 ([3],"*AMER *FORT!"),
 ([4,5,6],"Aravalli ki beautiful hills ke beech bana ye royal fort, aaj bhi apni shahi khoobsurati aur history se har kisi ko impress kar deta hai."),
 ([7],"Is kile ka construction *1592 mein Raja *Man *Singh *Pratham ne shuru karwaya tha."),
 ([8,9,10,11],"Yahan ka famous *Sheesh *Mahal, khoobsurat *Ganesh *Pol aur saamne phaili *Maota *Lake… har jagah aapko photography karne par majboor kar degi!"),
 ([12,13],"Lekin Jaipur mein sirf Amer Fort hi nahi, ghoomne ke liye aur bhi kai amazing tourist places hain."),
 ([14,15,16,17,18],"Agar aapko Jaipur ki complete travel guide chahiye, jismein sabhi tourist places ki location, ek jagah se doosri jagah ki distance, opening aur closing time aur car ya public transport se pahunchne ka complete route mile…"),
 ([19],"Toh comment mein likhiye *JAIPUR!"),
 ([20,21],"Aur is video ko save kar lijiye, kyunki Jaipur trip plan karte samay ye aapke bahut kaam aayegi!"),
]
def syl(w):
    w=w.lower().strip('*.,!…?-')
    if w.isdigit(): return 7
    n=len(re.findall(r'[aeiouy]+',w)); return max(1,n)+0.3
out=[]
for gi,(si,txt) in enumerate(groups):
    words=txt.split()
    ws=[syl(w) for w in words]; tot=sum(ws)
    spans=[segs[i] for i in si]; dur=sum(b-a for a,b in spans)
    def tmap(x):  # x in [0,dur] -> real time
        for a,b in spans:
            if x<=b-a+1e-9: return a+x
            x-=b-a
        return spans[-1][1]
    c=0
    for w,s in zip(words,ws):
        t0=tmap(c/tot*dur); c+=s; t1=tmap(c/tot*dur)
        out.append(dict(w=w.strip('*'),hl=w.startswith('*'),s=round(t0,3),e=round(t1,3),g=gi))
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
for o in out: print(o['s'],o['w'])
