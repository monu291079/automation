import json,re,sys
segs=[(0,1.82),(2.45,4.84),(5.36,7.57),(8.33,9.70),(10.17,12.41),(13.11,14.05),(14.33,16.94),(17.55,18.73),(19.38,20.81),(21.23,23.89),(24.58,25.46),(25.81,26.90),(27.24,28.37),(29.02,31.75),(32.82,34.59),(35.07,37.07),(37.63,38.33),(38.55,38.96),(39.51,41.47),(41.76,42.6)]
groups=[
 ([0],"*Brahma ji ka sabse mashhoor mandir!"),
 ([1,2],"Poore Bharat me Brahma ji ke bahut kam mandir hain, aur unme sabse prasiddh hai yahan *Pushkar me!"),
 ([3,4],"Sabse pehle *Pushkar *jheel! Kehte hain ye jheel Brahma ji ke *kamal se bani thi."),
 ([5,6],"Ghaat par baithiye... *aarti suniye... aur paani me tairte *diye dekhiye."),
 ([7,8,9],"Ab chaliye *Brahma *Mandir! Sangmarmar ki seedhiyan chadhiye, upar *laal *shikhar aur andar *chaandi ki nakkashi!"),
 ([10,11,12,13],"Lekin dhyaan rakhiye! *Bheed jaldi badhti hai, isliye *subah jaldi aaiye. Aur pooja ke naam par *paise maangne walon se saavdhaan rahiye!"),
 ([14,15],"Poora *2 *din ka Pushkar plan chahiye? Kahan rukein, kya khaayein, kitna kharch?"),
 ([16,17],"Comment me likhiye... *PUSHKAR!"),
 ([18,19],"Aur aise hi asli travel guides ke liye *follow zaroor kijiye!"),
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
