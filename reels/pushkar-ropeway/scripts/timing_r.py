import json,re,sys
segs=[(0,5.50),(5.88,10.78),(11.01,15.49),(15.75,19.82),(20.36,22.65),(22.94,23.06),(23.25,26.93),(27.21,31.08),(31.43,33.51),(33.98,34.74),(34.93,38.19),(38.73,39.68),(40.23,43.25)]
groups=[
 ([0],"Pushkar aaye hain to *Savitri *Mata ke mandir tak pahunchne ka ye shaandaar anubhav bilkul miss mat karna!"),
 ([1],"Pahaad ki chadhaai karne ki zaroorat nahi, kyunki yahan aapko milta hai ek romaanchak *Ropeway *Experience,"),
 ([2],"jahan aasmaan se dikhaai deta hai khoobsurat *Pushkar aur *Aravalli ki pahaadiyan!"),
 ([3],"Aur is Ropeway ka Adult Ticket hai sirf *₹195 prati vyakti!"),
 ([4,5],"Lekin rukiye! Yahan ek zaroori baat jaan lijiye."),
 ([6],"Savitri Mata ka mandir dopahar *12 baje se *2 baje tak *band rehta hai."),
 ([7],"Isliye agar aap is samay pahunchte hain, to aapko *intezaar karna pad sakta hai."),
 ([8],"Hum bhi abhi mandir khulne ka intezaar kar rahe hain!"),
 ([9,10],"Vaise aap bataiye, aapko *pahaadon par chadhna pasand hai ya aisa *Ropeway Experience?"),
 ([11],"Comment me zaroor bataiye"),
 ([12],"aur Pushkar ki aisi hi travel tips ke liye *follow karna mat bhooliye!"),
]
def syl(w):
    w=w.lower().strip('*.,!…?-')
    if w.isdigit() or w.startswith('₹'): return 5
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
