# Content for the Jaipur Complete Travel Guide (Hinglish edition, Nov 2026)
# Clusters: A = Amer & North, W = Walled City (Pink City), C = Central & South, E = Hills & East, O = Outskirts

CLUSTERS = {
    'A': ('Amer & North', '#E07B12'),
    'W': ('Walled City', '#C8436E'),
    'C': ('Central & South', '#1E7F7A'),
    'E': ('Hills & East', '#4A4FA3'),
    'O': ('Outskirts', '#6B7A26'),
}

# key, name, hindi, cluster, ticket, timing, need, best, must(1/0)
GLANCE = [
    ('amer', 'Amer Fort', 'आमेर किला', 'A', '₹200', '8:00 AM–5:30 PM', '2.5–3 hr', 'Subah 8–10', 1),
    ('jaigarh', 'Jaigarh Fort', 'जयगढ़ किला', 'A', '₹100–200', '9:00 AM–5:00 PM', '1–1.5 hr', 'Amer ke baad', 0),
    ('panna', 'Panna Meena ka Kund', 'पन्ना मीणा का कुंड', 'A', 'Free', 'Din me', '20–30 min', 'Subah', 0),
    ('anokhi', 'Anokhi Museum', 'अनोखी म्यूज़ियम', 'A', 'Paid', 'Din me (weekly off)', '45–60 min', 'Amer ke saath', 0),
    ('jalmahal', 'Jal Mahal (view)', 'जल महल', 'A', 'Free', 'Kabhi bhi', '15–30 min', 'Sunset', 1),
    ('kanak', 'Kanak Vrindavan', 'कनक वृंदावन', 'A', 'Chhota fee', 'Din me', '30–45 min', 'Shaam', 0),
    ('nahargarh', 'Nahargarh Fort', 'नाहरगढ़ किला', 'E', '₹100', '10:00 AM–9:00 PM', '2–3 hr', 'Sunset + raat', 1),
    ('gaitore', 'Gaitore ki Chhatriyan', 'गैटोर की छतरियाँ', 'E', 'Chhota fee', '9:00 AM–5:00 PM', '30–45 min', 'Subah', 0),
    ('hawa', 'Hawa Mahal', 'हवा महल', 'W', '₹100', '9:00 AM–5:00 PM', '45–60 min', 'Subah 9 baje', 1),
    ('citypalace', 'City Palace', 'सिटी पैलेस', 'W', '₹400 approx', '9:30 AM–6:30 PM', '1.5–2.5 hr', 'Dopahar se pehle', 1),
    ('jantar', 'Jantar Mantar', 'जंतर मंतर', 'W', '₹100', '9:00 AM–7:00 PM', '45–75 min', 'Dhoop wala din', 1),
    ('govind', 'Govind Dev Ji Temple', 'गोविंद देव जी', 'W', 'Free', 'Darshan jhaankiyan', '30–60 min', 'Aarti time', 0),
    ('isarlat', 'Isarlat (Swargasuli)', 'ईसरलाट', 'W', 'Chhota fee', 'Din me', '30 min', 'Subah', 0),
    ('albert', 'Albert Hall Museum', 'अल्बर्ट हॉल', 'C', '₹100', '9:00 AM–8:00 PM', '1–1.5 hr', 'Shaam (lights)', 1),
    ('masala', 'Masala Chowk', 'मसाला चौक', 'C', 'Chhota entry', 'Dopahar–raat', '45–60 min', 'Dinner', 0),
    ('birla', 'Birla Mandir', 'बिड़ला मंदिर', 'C', 'Free', '6–12 & 3–9 PM', '30–45 min', 'Shaam', 0),
    ('motidungri', 'Moti Dungri Ganesh', 'मोती डूंगरी गणेश', 'C', 'Free', 'Darshan time', '20–40 min', 'Budhwar avoid', 0),
    ('rajmandir', 'Raj Mandir Cinema', 'राज मंदिर', 'C', 'Movie ticket', 'Show-wise', '3 hr', 'Raat ka show', 0),
    ('patrika', 'Patrika Gate', 'पत्रिका गेट', 'C', 'Free', 'Din me', '30 min', 'Subah (photos)', 1),
    ('jkk', 'Jawahar Kala Kendra', 'जवाहर कला केंद्र', 'C', 'Mostly free', 'Event-wise', '45–60 min', 'Event ho tab', 0),
    ('galtaji', 'Galtaji (Monkey Temple)', 'गलताजी', 'E', 'Free', 'Din me', '1–1.5 hr', 'Subah/shaam', 0),
    ('sisodia', 'Sisodia Rani Garden', 'सिसोदिया रानी बाग', 'E', 'Chhota fee', 'Din me', '30–45 min', 'Subah', 0),
    ('jhalana', 'Jhalana Leopard Safari', 'झालाना लेपर्ड सफारी', 'E', '₹1,350/seat', '2 shift (subah/shaam)', '2.5 hr', 'Subah ki shift', 1),
    ('chokhi', 'Chokhi Dhani', 'चोखी ढाणी', 'O', 'Package', 'Shaam 5–11 PM', '3–4 hr', 'Dinner', 0),
]

MAPQ = {
    'amer': 'Amer Fort Jaipur', 'jaigarh': 'Jaigarh Fort Jaipur', 'panna': 'Panna Meena ka Kund Jaipur', 'anokhi': 'Anokhi Museum of Hand Printing Amer',
    'jalmahal': 'Jal Mahal Jaipur', 'kanak': 'Kanak Vrindavan Garden Jaipur', 'nahargarh': 'Nahargarh Fort Jaipur', 'gaitore': 'Gaitore ki Chhatriyan Jaipur',
    'hawa': 'Hawa Mahal Jaipur', 'citypalace': 'City Palace Jaipur', 'jantar': 'Jantar Mantar Jaipur', 'govind': 'Govind Dev Ji Temple Jaipur',
    'isarlat': 'Isarlat Swargasuli Jaipur', 'albert': 'Albert Hall Museum Jaipur', 'masala': 'Masala Chowk Ram Niwas Garden Jaipur', 'birla': 'Birla Mandir Jaipur',
    'motidungri': 'Moti Dungri Ganesh Temple Jaipur', 'rajmandir': 'Raj Mandir Cinema Jaipur', 'patrika': 'Patrika Gate Jaipur', 'jkk': 'Jawahar Kala Kendra Jaipur',
    'galtaji': 'Galtaji Temple Jaipur', 'sisodia': 'Sisodia Rani Garden Jaipur', 'vidyadhar': 'Vidyadhar Garden Jaipur', 'jhalana': 'Jhalana Leopard Safari Jaipur',
    'chokhi': 'Chokhi Dhani Jaipur', 'abhaneri': 'Chand Baori Abhaneri', 'bhangarh': 'Bhangarh Fort', 'sambhar': 'Sambhar Salt Lake',
}

# Detailed place info: intro, car, public, tip, (optional) facts list
PLACES = {
    'amer': dict(
        intro='1592 me Raja Man Singh I ne iska nirmaan shuru karwaya. Aravalli ki pahadi par bana ye palace-fort Jaipur ki sabse badi pehchaan hai — Ganesh Pol, Sheesh Mahal, Diwan-e-Aam, Sukh Niwas aur neeche Maota Lake.',
        see=['Ganesh Pol — painted royal gate', 'Sheesh Mahal — mirror work wala hall', 'Diwan-e-Aam — 40 pillars wala darbar', 'Sukh Niwas & Maota Lake view'],
        car='Amer Road (Jal Mahal ke raaste) se ~11 km. Fort parking me gaadi lagaiye, wahan se paidal ya jeep.',
        public='Badi Chaupar / Hawa Mahal se Amer jaane wali city bus ya auto. Metro Amer tak nahi jaati.',
        tip='Subah 8 baje pahunchiye — bheed aur dhoop dono kam. Comfortable joote pehniye, andar bahut seedhiyan aur dhalaan hai. Gate par sirf ID card wale approved guide lijiye.'),
    'jaigarh': dict(
        intro='Amer ke theek upar "Cheel ka Teela" pahadi par bana military fort. Yahan Jaivana tope hai — duniya ki sabse badi pahiye wali topon me se ek.',
        car='Amer se ~4 km pahadi road. Car/taxi sabse aasaan.', public='Amer se local jeep/taxi. Seedhi bus nahi.',
        tip='Amer ke saath hi same din kariye. Fort bada hai — paani saath rakhiye.'),
    'panna': dict(
        intro='Amer ke paas 16vi sadi ki stepwell (baori) — criss-cross seedhiyon ki wajah se Jaipur ka sabse photogenic spot.',
        car='Amer Fort se sirf ~1 km. Gaadi Amer parking me hi rakh sakte hain.', public='Amer se paidal 10–12 min ya auto.',
        tip='Seedhiyon par utarna mana hai — barrier cross mat kariye. Subah ki roshni me photos sabse achhi aati hain.'),
    'anokhi': dict(
        intro='Amer ki restored haveli me block printing ka museum. Live demo me karigar haath se printing karte dikhte hain.',
        car='Amer ki galiyon me — gaadi bahar rakh kar paidal jaiye.', public='Amer tak bus/auto, phir paidal.',
        tip='Weekly off hota hai — jaane se pehle website par din check kar lijiye.'),
    'jalmahal': dict(
        intro='Man Sagar jheel ke beech khada "Water Palace". Andar entry nahi hai, par kinaare ki sadak se view hi asli attraction hai.',
        car='Amer Road par, Hawa Mahal se ~6 km. Sadak kinaare thodi der ruk sakte hain.', public='Amer jaane wali har bus/auto yahin se guzarti hai.',
        tip='Sunset ke time sabse sundar. Busy road hai — sadak dhyan se paar kariye.'),
    'kanak': dict(
        intro='Nahargarh ki pahadiyon ke neeche shaant landscaped garden aur purane mandir — Amer road par ek relaxing stop.',
        car='Jal Mahal se ~3 km, Amer Road par.', public='Amer Road ki bus/auto.',
        tip='Bheed se door 30 min ka break chahiye to perfect.'),
    'nahargarh': dict(
        intro='1734 me Maharaja Sawai Jai Singh II ne banwaya. Aravalli ki chotti par bana ye kila kabhi Jaipur ka "suraksha kawach" tha. Naam ki kahani Nahar Singh Bhomia se judi maani jaati hai.',
        see=['Madhavendra Bhawan — 9 ek jaise royal suites', 'Sunset point — ek taraf Jal Mahal, ek taraf shehar', 'Raat ko jagmagata Pink City', 'Wax Museum & Sheesh Mahal (alag ticket)'],
        car='Pahadi ghumavdaar road (Amer Road side se). Raat ko dhyan se chalaiye, mod par gaadi mat rokiye.',
        public='Auto/cab hi best. Seedhi bus/metro nahi — wapsi ki gaadi pehle se fix kariye.',
        tip='Fort area raat 9 baje tak khula rehta hai — isliye shaam 5 baje pahunchiye: pehle Madhavendra Bhawan (museum timing din ki hai), phir sunset aur raat ki lights.'),
    'gaitore': dict(
        intro='Kachwaha rajaon ki marble chhatriyan (cenotaphs) — baarik nakkashi aur ekdum shaant mahaul.',
        car='Nahargarh road ke neeche, Hawa Mahal se ~4 km.', public='Auto/e-rickshaw.',
        tip='Nahargarh jaate waqt raaste me 30 min ka stop.'),
    'hawa': dict(
        intro='1799 me Maharaja Sawai Pratap Singh ne banwaya. 5 manzil, 953 jharokhe — rani-mahaaraniyan yahan se bina dikhe bazaar ka nazaara dekhti thi.',
        car='Old city me parking mushkil — Badi Chaupar ke paas designated parking me lagaiye aur paidal chaliye.',
        public='Metro: Badi Chaupar station — 5 min paidal. E-rickshaw har jagah milta hai.',
        tip='Famous front photo ke liye saamne wale rooftop cafés par jaiye. Andar entry peechhe ki taraf se hai.'),
    'citypalace': dict(
        intro='Shahi parivaar ka mahal-complex — Mubarak Mahal, galleries aur Pritam Niwas Chowk ke 4 famous rangeen darwaze.',
        car='Jalebi Chowk/Gate 2 ke paas parking.', public='Metro Badi Chaupar, phir 10 min paidal.',
        tip='Chandra Mahal ka royal tour alag premium ticket hai. Standard ticket me bhi 4 darwaze dikh jaate hain.'),
    'jantar': dict(
        intro='Sawai Jai Singh II ki banayi UNESCO World Heritage observatory — 19 yantra, jinme Samrat Yantra duniya ki sabse badi sundial hai.',
        car='City Palace ke bagal me — same parking.', public='Metro Badi Chaupar, paidal.',
        tip='Guide ya audio guide zaroor lijiye — warna yantra sirf deewar lagenge. Dhoop me sundial kaam karta dikhta hai.'),
    'govind': dict(
        intro='Jaipur ke rajparivaar ke aaradhya Shri Krishna ka mandir — Jaipur ki aastha ka dil.',
        car='City Palace parking.', public='Badi Chaupar se paidal.',
        tip='Darshan din me kai jhaankiyon me hote hain, beech me pat band rehte hain. Aarti time pe bheed bahut hoti hai.'),
    'isarlat': dict(
        intro='Tripolia Bazaar ke beech oonchi meenar — upar se poore Pink City ke chhato ka 360° view.',
        car='Old city — paidal best.', public='Metro Chhoti Chaupar, paidal.',
        tip='Seedhiyan sankari hain. Hawa Mahal ke baad 30 min ka bonus stop.'),
    'albert': dict(
        intro='Ram Niwas Garden me Indo-Saracenic shaili ka Rajasthan ka sabse purana museum — Egyptian mummy, paintings, hathiyaar aur textiles.',
        car='Ram Niwas Garden parking.', public='JLN Marg ki bus ya auto.',
        tip='Shaam ko building roshni me nahaati hai — bahar se photo zaroor. Saath me Masala Chowk me dinner.'),
    'masala': dict(
        intro='Albert Hall ke bagal me open-air food court — Jaipur ke famous street food stalls ek hi jagah.',
        car='Ram Niwas Garden parking.', public='Albert Hall ke paas.',
        tip='Pyaaz kachori, mirchi vada aur kulfi ek hi jagah try kariye.'),
    'birla': dict(
        intro='Safed marble ka Laxmi Narayan mandir, Moti Dungri ke neeche. Raat ki roshni me ekdum chamakta hai.',
        car='Mandir parking.', public='JLN Marg bus/auto.',
        tip='Shaam ki aarti ke time aaiye. Andar photography mana ho sakti hai.'),
    'motidungri': dict(
        intro='Jaipur ka sabse popular Ganesh mandir — har shubh kaam yahan se shuru hota hai.',
        car='Birla Mandir ke bagal me.', public='JLN Marg bus/auto.',
        tip='Budhwar aur tyohaar par lambi line — doosre din jaiye.'),
    'rajmandir': dict(
        intro='"Pride of Asia" kehlaane wala 1976 ka iconic cinema hall — meringue jaisi pink interior.',
        car='MI Road/Bhagwan Das Road ke paas.', public='Metro Sindhi Camp/auto.',
        tip='Hindi movie ka ek show dekhna apne aap me experience hai — ticket pehle book kar lijiye.'),
    'patrika': dict(
        intro='Jawahar Circle ka rangeen gate — har corridor me Rajasthan ke alag shehar ki painting.',
        car='Jawahar Circle parking, airport ke paas.', public='Airport side bus/auto.',
        tip='Subah 7–9 me jaiye — khaali corridors me best photos.'),
    'jkk': dict(
        intro='Architect Charles Correa ka design kiya arts centre — galleries, theatre aur cultural events.',
        car='JLN Marg par.', public='JLN Marg bus/auto.',
        tip='Jaane se pehle event calendar dekh lijiye.'),
    'galtaji': dict(
        intro='Pahadiyon ke beech prachin teerth — kund, mandir aur prakritik jharne. Bandaron ki wajah se "Monkey Temple".',
        car='Galta Gate tak gaadi, phir paidal.', public='Auto/cab, last part paidal.',
        tip='Khaane ka saamaan chhupa kar rakhiye — bandar chheen lete hain. Bandaron ko khilana mana hai.'),
    'sisodia': dict(
        intro='18vi sadi ka seedhinuma bagh — fountains, pavilions aur Radha-Krishna ki deewar chitrakari.',
        car='Agra Road par, Hawa Mahal se ~7 km. Paas me Vidyadhar Garden bhi.', public='Agra Road bus + auto.',
        tip='Galtaji ke saath ek hi trip me kariye.'),
    'jhalana': dict(
        intro='Shehar ke beech leopard reserve — Jaipur ki sabse anokhi activity. Open gypsy me safari, kismat achhi ho to leopard dikhta hai.',
        car='Jhalana gate, Malviya Nagar side. Hawa Mahal se ~8 km.', public='Cab/auto se gate tak.',
        tip='Online FMDSS portal se pehle booking kariye. Shared seat ~₹1,350, poori gypsy ~₹7,000 (Indian). 30 min pehle pahunchiye.'),
    'chokhi': dict(
        intro='Rajasthani gaon ka theme resort — folk dance, kathputli, camel ride aur zameen par baith kar bhar-pet Rajasthani thali.',
        car='Tonk Road, Hawa Mahal se ~20 km. Cab best.', public='Tonk Road bus + last mile cab.',
        tip='Package aur din pehle confirm kariye. 3–4 ghante rakhiye.'),
}

DISTANCES = [
    ('Amer Fort', 'Panna Meena Kund', '1 km', '5 min', 'Paidal/auto'),
    ('Amer Fort', 'Jaigarh Fort', '4 km', '15 min', 'Car/jeep'),
    ('Amer Fort', 'Jal Mahal', '5 km', '15 min', 'Car/bus/auto'),
    ('Jal Mahal', 'Hawa Mahal', '6 km', '20 min', 'Car/bus/auto'),
    ('Hawa Mahal', 'City Palace', '1 km', '10 min', 'Paidal'),
    ('City Palace', 'Jantar Mantar', '0.2 km', '3 min', 'Paidal'),
    ('Hawa Mahal', 'Isarlat', '1 km', '10 min', 'Paidal'),
    ('Hawa Mahal', 'Albert Hall', '3.5 km', '15 min', 'Auto/cab'),
    ('Albert Hall', 'Birla Mandir', '2.5 km', '10 min', 'Auto/cab'),
    ('Birla Mandir', 'Moti Dungri', '0.5 km', '5 min', 'Paidal'),
    ('Hawa Mahal', 'Nahargarh Fort', '~15 km', '40 min', 'Cab (pahadi road)'),
    ('Hawa Mahal', 'Galtaji', '~9 km', '30 min', 'Auto/cab'),
    ('Hawa Mahal', 'Jhalana Safari', '~8 km', '25 min', 'Cab'),
    ('Hawa Mahal', 'Patrika Gate', '~12 km', '35 min', 'Cab/auto'),
    ('Hawa Mahal', 'Chokhi Dhani', '~20 km', '45 min', 'Cab'),
    ('Hawa Mahal', 'Airport', '~12 km', '35 min', 'Cab'),
    ('Hawa Mahal', 'Jaipur Junction', '~5 km', '15 min', 'Metro/auto'),
]

EXTRA = {
    'jaigarh': (['Jaivana tope', 'Armoury & museum', 'Amer ka top view'], 'Amer Fort'),
    'panna': (['Criss-cross seedhiyan', 'Pahadi ka backdrop', 'Morning light photos'], 'Amer Fort, Anokhi Museum'),
    'anokhi': (['Live block-print demo', 'Restored haveli', 'Museum shop'], 'Panna Meena ka Kund'),
    'jalmahal': (['Jheel ka promenade', 'Sunset reflection', 'Rangeen street stalls'], 'Kanak Vrindavan, Amer'),
    'kanak': (['Terraced garden', 'Purane mandir', 'Shaant photo spots'], 'Jal Mahal'),
    'gaitore': (['Marble chhatriyan', 'Baarik nakkashi', 'Pahadi backdrop'], 'Nahargarh road'),
    'hawa': (['953 jharokhe', 'Upar se Jantar Mantar view', 'Front facade photo'], 'Isarlat, City Palace'),
    'isarlat': (['360° Pink City view', 'Tripolia Bazaar'], 'Hawa Mahal'),
    'citypalace': (['Pritam Niwas ke 4 darwaze', 'Mubarak Mahal', 'Diwan-e-Khas ke chaandi ke kalash'], 'Jantar Mantar, Govind Dev Ji'),
    'jantar': (['Samrat Yantra', 'Rashi Valaya (12 rashiyan)', 'Jai Prakash Yantra'], 'City Palace'),
    'govind': (['Mangla se Shayan jhaankiyan', 'Jai Niwas Bagh'], 'City Palace'),
    'albert': (['Egyptian mummy', 'Miniature paintings', 'Raat ki lighting'], 'Masala Chowk, Birla Mandir'),
    'masala': (['Street food stalls', 'Family seating'], 'Albert Hall'),
    'birla': (['Safed marble', 'Glass panels pe Gita updesh', 'Shaam ki aarti'], 'Moti Dungri'),
    'motidungri': (['Ganesh ji ke darshan', 'Pahadi par mahal (bahar se)'], 'Birla Mandir'),
    'rajmandir': (['Pink lobby', 'Bade chandelier', 'Bollywood vibe'], 'MI Road'),
    'patrika': (['Rangeen corridors', 'Jawahar Circle garden'], 'Airport'),
    'jkk': (['Correa ka architecture', 'Art galleries', 'Coffee house'], 'JLN Marg, Birla Mandir'),
    'galtaji': (['Pavitra kund', 'Pahadi mandir', 'Upar Surya Mandir'], 'Sisodia Rani Garden'),
    'sisodia': (['Seedhinuma bagh', 'Fountains', 'Deewar chitrakari'], 'Vidyadhar Garden, Galtaji'),
    'jhalana': (['Leopard', 'Nilgai & hiran', 'Pakshi'], 'Malviya Nagar'),
    'chokhi': (['Folk dance', 'Kathputli show', 'Rajasthani thali'], 'Tonk Road'),
}
