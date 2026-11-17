import json,re,sys
segs=[(0,1.83),(2.11,3.84),(4.12,5.23),(5.44,8.94),(9.19,13.42),(13.66,15.40),(15.64,20.19),(20.42,26.77),(27.06,29.14),(29.37,33.66),(33.92,38.58),(38.84,41.05),(41.34,43.26),(43.51,44.51),(44.85,45.86),(46.09,48.43),(48.73,52.45)]
groups=[
 ([0],"Jaipur ka sabse shaandaar view dekhna hai?"),
 ([1],"Toh is kile ko bilkul miss mat karna!"),
 ([2],"Ye hai *NAHARGARH *FORT,"),
 ([3],"jise *1734 mein Maharaja *Sawai *Jai *Singh dwitiya ne banwaya tha."),
 ([4],"Aravalli ki pahadiyon par bana ye kila kabhi Jaipur ki suraksha ka aham hissa hua karta tha!"),
 ([5],"Aur jaante hain iska naam Nahargarh kaise pada?"),
 ([6],"Manyata hai ki *Nahar *Singh *Bhomia se judi ek kahani ke kaaran iska naam Nahargarh rakha gaya!"),
 ([7],"Kile ke andar bana *Madhavendra *Bhawan, iski shaandaar architecture aur royal rooms aapko purane rajsi daur ki yaad dila denge!"),
 ([8],"Lekin asli mazaa toh yahan shaam ke samay aata hai!"),
 ([9],"Ek taraf khoobsurat *sunset aur doosri taraf roshni se jagmagata poora *Pink *City!"),
 ([10],"Aisa shaandaar panoramic view aapko Jaipur ki sabse yaadgaar tasveeron mein se ek de sakta hai!"),
 ([11],"Agar aapko Jaipur ki complete travel guide chahiye,"),
 ([12,13,14],"jismein sabhi tourist places ki location, aapas ki distance, opening-closing time aur car va public transport ke poore routes hon,"),
 ([15],"toh comment mein likhiye *JAIPUR!"),
 ([16],"Video ko save kar lo aur Jaipur ghoomne nikal pado!"),
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
