# Pushkar Complete Travel Guide 2026 — content in Hindi (hi) and English (en).
# Every text field is a (hi, en) tuple. Edit here and rebuild.

CLUSTERS = {
    'L': (('झील और घाट', 'Lake & Ghats'), '#1F7A8C'),
    'T': (('मंदिर', 'Temples'), '#C0392B'),
    'H': (('पहाड़ी मंदिर', 'Hill Temples'), '#7B4BA8'),
    'M': (('बाज़ार और खाना', 'Bazaar & Food'), '#D9822B'),
    'D': (('रेगिस्तान और मेला', 'Desert & Fair'), '#A0782C'),
    'X': (('आस-पास', 'Nearby'), '#4F7A28'),
}

# key, name(hi,en), cluster, ticket(hi,en), timing(hi,en), need(hi,en), best(hi,en), must
GLANCE = [
    ('brahma', ('ब्रह्मा मंदिर', 'Brahma Temple'), 'T', ('निःशुल्क', 'Free'), ('सुबह 6:30–1:30, दोपहर 3–9 बजे', '6:30 AM–1:30 PM, 3–9 PM'), ('45–60 मिनट', '45–60 min'), ('सुबह 7 बजे', '7 AM'), 1),
    ('lake', ('पुष्कर झील', 'Pushkar Lake'), 'L', ('निःशुल्क', 'Free'), ('हमेशा खुली', 'Always open'), ('1–2 घंटे', '1–2 hr'), ('सूर्योदय / सूर्यास्त', 'Sunrise / sunset'), 1),
    ('varaha_ghat', ('वराह घाट आरती', 'Varaha Ghat Aarti'), 'L', ('निःशुल्क', 'Free'), ('सूर्यास्त के समय', 'At sunset'), ('45 मिनट', '45 min'), ('शाम', 'Evening'), 1),
    ('gau_ghat', ('गऊ घाट (गांधी घाट)', 'Gau Ghat (Gandhi Ghat)'), 'L', ('निःशुल्क', 'Free'), ('हमेशा खुला', 'Always open'), ('30 मिनट', '30 min'), ('सुबह', 'Morning'), 0),
    ('savitri', ('सावित्री माता मंदिर', 'Savitri Mata Temple'), 'H', ('रोपवे ₹ अलग', 'Ropeway extra'), ('सुबह 5–शाम 7 (लगभग)', '5 AM–7 PM (approx)'), ('2 घंटे', '2 hr'), ('सूर्योदय', 'Sunrise'), 1),
    ('gayatri', ('गायत्री मंदिर (पाप मोचनी)', 'Gayatri Temple (Pap Mochani)'), 'H', ('निःशुल्क', 'Free'), ('दिन में', 'Daytime'), ('1–1.5 घंटे', '1–1.5 hr'), ('सूर्योदय', 'Sunrise'), 0),
    ('rangji', ('रंगजी मंदिर', 'Rangji Temple'), 'T', ('निःशुल्क', 'Free'), ('दर्शन समय', 'Darshan hours'), ('30 मिनट', '30 min'), ('सुबह', 'Morning'), 1),
    ('varaha_temple', ('वराह मंदिर', 'Varaha Temple'), 'T', ('निःशुल्क', 'Free'), ('दर्शन समय', 'Darshan hours'), ('20–30 मिनट', '20–30 min'), ('सुबह', 'Morning'), 0),
    ('aptaeshwar', ('आप्तेश्वर महादेव', 'Aptaeshwar Mahadev'), 'T', ('निःशुल्क', 'Free'), ('दर्शन समय', 'Darshan hours'), ('20 मिनट', '20 min'), ('शाम', 'Evening'), 0),
    ('manmahal', ('मान महल', 'Man Mahal'), 'L', ('बाहर से निःशुल्क', 'Free (outside)'), ('दिन में', 'Daytime'), ('20 मिनट', '20 min'), ('दोपहर', 'Afternoon'), 0),
    ('bazaar', ('सदर बाज़ार', 'Sadar Bazaar'), 'M', ('—', '—'), ('सुबह 9–रात 9', '9 AM–9 PM'), ('1–2 घंटे', '1–2 hr'), ('शाम', 'Evening'), 1),
    ('desert', ('डेज़र्ट कैंप और कैमल सफ़ारी', 'Desert Camp & Camel Safari'), 'D', ('पैकेज', 'Package'), ('सूर्यास्त', 'Sunset'), ('3–4 घंटे', '3–4 hr'), ('सूर्यास्त', 'Sunset'), 1),
    ('fair', ('पुष्कर ऊँट मेला', 'Pushkar Camel Fair'), 'D', ('निःशुल्क', 'Free'), ('कार्तिक (अक्टू–नवं)', 'Kartik (Oct–Nov)'), ('1–2 दिन', '1–2 days'), ('मेले के दिन', 'Fair days'), 1),
    ('ajmer', ('अजमेर शरीफ़ दरगाह', 'Ajmer Sharif Dargah'), 'X', ('निःशुल्क', 'Free'), ('सुबह 4–रात 10 (लगभग)', '4 AM–10 PM (approx)'), ('1.5–2 घंटे', '1.5–2 hr'), ('सुबह', 'Morning'), 0),
    ('anasagar', ('आना सागर झील, अजमेर', 'Ana Sagar Lake, Ajmer'), 'X', ('निःशुल्क', 'Free'), ('दिन में', 'Daytime'), ('45 मिनट', '45 min'), ('शाम', 'Evening'), 0),
]

MAPQ = {
    'brahma': 'Brahma Temple Pushkar', 'lake': 'Pushkar Lake', 'varaha_ghat': 'Varaha Ghat Pushkar', 'gau_ghat': 'Gau Ghat Pushkar',
    'savitri': 'Savitri Mata Temple Pushkar', 'gayatri': 'Gayatri Mata Temple Pushkar', 'rangji': 'Old Rangji Temple Pushkar',
    'varaha_temple': 'Varaha Temple Pushkar', 'aptaeshwar': 'Aptaeshwar Mahadev Temple Pushkar', 'manmahal': 'RTDC Hotel Sarovar Man Mahal Pushkar',
    'bazaar': 'Sadar Bazaar Pushkar', 'desert': 'Pushkar sand dunes desert camp', 'fair': 'Pushkar Mela Ground', 'ajmer': 'Ajmer Sharif Dargah',
    'anasagar': 'Ana Sagar Lake Ajmer', 'pushkar_bus': 'Pushkar Bus Stand', 'ajmer_jn': 'Ajmer Junction railway station', 'kishangarh': 'Kishangarh Airport',
}

PLACES = {
    'brahma': dict(
        intro=('पूरी दुनिया में ब्रह्मा जी के गिने-चुने मंदिर हैं, और उनमें सबसे प्रसिद्ध यही है। संगमरमर की सीढ़ियाँ, लाल शिखर, हंस की आकृति और चाँदी के सिक्कों से जड़ा फ़र्श इसकी पहचान हैं। मौजूदा मंदिर 14वीं सदी का माना जाता है।',
               'One of the very few Brahma temples in the world, and the most famous. Marble steps, a red spire, the swan (hamsa) motif and a floor studded with silver coins. The present structure is believed to date to the 14th century.'),
        see=(['संगमरमर की सीढ़ियाँ और लाल शिखर', 'गर्भगृह में चतुर्मुखी ब्रह्मा जी', 'चाँदी की नक़्क़ाशी और सिक्कों वाला फ़र्श', 'शाम की आरती'],
             ['Marble staircase and red spire', 'Four-faced Brahma idol in the sanctum', 'Silver work and coin-studded floor', 'Evening aarti']),
        reach=('झील के पश्चिमी किनारे पर, मुख्य बाज़ार से 5 मिनट पैदल। गाड़ी बाहर पार्किंग में छोड़िए — अंदर की गलियाँ सिर्फ़ पैदल हैं।',
               'On the western side of the lake, 5 minutes on foot from the main bazaar. Leave vehicles at the outer parking; the lanes are walk-only.'),
        tip=('मोबाइल, कैमरा और चमड़े का सामान अंदर नहीं ले जा सकते — बाहर लॉकर/काउंटर पर जमा करें। सुबह 7 बजे जाएँ, 10 बजे के बाद लंबी लाइन।',
             'Phones, cameras and leather items are not allowed inside; deposit them at the counter outside. Go at 7 AM — queues build after 10.')),
    'lake': dict(
        intro=('हिंदू मान्यता के अनुसार यह झील ब्रह्मा जी के हाथ से गिरे कमल से बनी। इसके चारों ओर 52 घाट और 500 से ज़्यादा मंदिर हैं। कार्तिक पूर्णिमा पर यहाँ स्नान का बड़ा महत्व है।',
               'Hindu tradition says the lake formed where a lotus fell from Brahma’s hand. It is ringed by 52 ghats and more than 500 temples, and bathing here on Kartik Purnima is especially sacred.'),
        see=(['52 घाटों की परिक्रमा', 'सूर्योदय पर शांत पानी', 'घाट पर दीपदान', 'छत वाले कैफ़े से झील का नज़ारा'],
             ['Walk the ghats around the lake', 'Still water at sunrise', 'Float a diya (deep daan)', 'Lake view from rooftop cafés']),
        reach=('पूरे कस्बे के बीच में — हर होटल से पैदल। झील की पूरी परिक्रमा लगभग 1 घंटा।', 'In the middle of town — walkable from every hotel. A full loop of the lake takes about an hour.'),
        tip=('घाट पर जूते उतारें। नहाते हुए श्रद्धालुओं की फ़ोटो न लें — यहाँ कई घाटों पर फ़ोटोग्राफ़ी मना है।', 'Remove shoes on the ghats. Do not photograph people bathing; photography is restricted at many ghats.')),
    'varaha_ghat': dict(
        intro=('पुष्कर की सबसे प्रसिद्ध शाम की आरती यहीं होती है — घंटियाँ, शंख, दीपों की लौ और पानी में तैरते दीये। ब्रह्मा घाट पर भी आरती होती है।',
               'Pushkar’s best-known evening aarti happens here: bells, conch shells, lamp flames and diyas floating on the water. Brahma Ghat also holds an aarti.'),
        reach=('ब्रह्मा मंदिर से 5–7 मिनट पैदल, बाज़ार के रास्ते।', '5–7 minutes on foot from Brahma Temple, through the bazaar.'),
        tip=('सूर्यास्त से 20 मिनट पहले पहुँचें ताकि सीढ़ियों पर अच्छी जगह मिले।', 'Arrive 20 minutes before sunset to get a good spot on the steps.')),
    'gau_ghat': dict(
        intro=('1948 में महात्मा गांधी की अस्थियाँ यहीं विसर्जित की गईं, इसलिए इसे गांधी घाट भी कहते हैं। सबसे बड़ा और साफ़ घाट।',
               'Mahatma Gandhi’s ashes were immersed here in 1948, so it is also called Gandhi Ghat. One of the largest and cleanest ghats.'),
        reach=('मुख्य बाज़ार के बीच से घाट की सीढ़ियाँ।', 'Steps lead down from the middle of the main bazaar.'),
        tip=('सुबह की धूप में यहाँ से झील की सबसे साफ़ फ़ोटो आती है।', 'Morning light here gives the clearest lake photos.')),
    'savitri': dict(
        intro=('रत्नागिरि पहाड़ी पर ब्रह्मा जी की पत्नी सावित्री माता का मंदिर। ऊपर से पूरा पुष्कर, झील और अरावली दिखती है — शहर का सबसे सुंदर सूर्योदय।',
               'Temple of Savitri, Brahma’s consort, on Ratnagiri hill. From the top you see all of Pushkar, the lake and the Aravallis — the town’s best sunrise.'),
        see=(['सूर्योदय / सूर्यास्त पॉइंट', 'रोपवे की सवारी', 'पूरे पुष्कर का 360° नज़ारा'], ['Sunrise / sunset point', 'Ropeway ride', '360° view of Pushkar']),
        reach=('झील से लगभग 2 किमी। लगभग 650+ सीढ़ियाँ (45–60 मिनट) या रोपवे (5 मिनट)।', 'About 2 km from the lake. Roughly 650+ steps (45–60 min) or the ropeway (5 min).'),
        tip=('बुज़ुर्गों और बच्चों के लिए रोपवे लें। पानी साथ रखें, ऊपर दुकानें कम हैं। रोपवे टिकट और समय काउंटर पर देखें।', 'Take the ropeway with elders or kids. Carry water — there are few shops on top. Check ropeway fare and hours at the counter.')),
    'gayatri': dict(
        intro=('झील के दूसरी तरफ़ की पहाड़ी पर गायत्री माता (पाप मोचनी) मंदिर — सावित्री मंदिर से कम भीड़, सूर्योदय के लिए शानदार।',
               'Gayatri (Pap Mochani) temple on the hill across the lake — quieter than Savitri and excellent for sunrise.'),
        reach=('कस्बे के पूर्व से लगभग 20–30 मिनट की चढ़ाई।', 'A 20–30 minute climb from the east side of town.'),
        tip=('अंधेरे में चढ़ाई के लिए टॉर्च रखें। अकेले जा रहे हैं तो किसी को बताकर जाएँ।', 'Carry a torch for a pre-dawn climb, and tell someone if you go alone.')),
    'rangji': dict(
        intro=('भगवान विष्णु (रंगनाथ) का मंदिर, जिसकी बनावट में दक्षिण भारतीय गोपुरम, राजपूत और मुग़ल शैली का मेल है। पुराना और नया रंगजी, दोनों देखने लायक।',
               'Temple to Vishnu as Ranganath, mixing a South Indian gopuram with Rajput and Mughal styles. Both the Old and New Rangji temples are worth seeing.'),
        reach=('ब्रह्मा मंदिर से 10 मिनट पैदल।', '10 minutes on foot from Brahma Temple.'),
        tip=('कुछ हिस्सों में सिर्फ़ हिंदू श्रद्धालुओं को प्रवेश हो सकता है — गेट पर लगा बोर्ड पढ़ें।', 'Some areas may be open to Hindu devotees only; read the board at the gate.')),
    'varaha_temple': dict(
        intro=('विष्णु के वराह अवतार को समर्पित पुराना मंदिर, जिसे कई बार दोबारा बनाया गया।', 'An old temple to Vishnu’s boar avatar, Varaha, rebuilt several times over the centuries.'),
        reach=('वराह घाट के पास बाज़ार में।', 'In the bazaar near Varaha Ghat.'), tip=('आरती से पहले यहाँ दर्शन कर लें।', 'Visit just before the ghat aarti.')),
    'aptaeshwar': dict(
        intro=('ज़मीन के नीचे बना प्राचीन शिव मंदिर — शांत और ठंडा।', 'An ancient underground Shiva temple — quiet and cool.'),
        reach=('ब्रह्मा मंदिर के पास।', 'Near Brahma Temple.'), tip=('सीढ़ियाँ संकरी हैं, धीरे उतरें।', 'The steps are narrow; go slowly.')),
    'manmahal': dict(
        intro=('आमेर के राजा मान सिंह प्रथम का झील किनारे बना महल, जो अब RTDC का होटल सरोवर है।', 'Lakeside palace of Raja Man Singh I of Amer, now RTDC’s Hotel Sarovar.'),
        reach=('झील के पूर्वी किनारे पर।', 'On the eastern edge of the lake.'), tip=('होटल के लॉन से झील का शांत नज़ारा और चाय।', 'Tea with a calm lake view from the hotel lawns.')),
    'bazaar': dict(
        intro=('ब्रह्मा मंदिर से झील तक फैला सदर बाज़ार — चाँदी के गहने, रंगीन कपड़े, चमड़े के बैग, गुलाब के उत्पाद और हैंडीक्राफ़्ट।',
               'Sadar Bazaar runs from Brahma Temple to the lake: silver jewellery, colourful clothes, leather bags, rose products and handicrafts.'),
        see=(['चाँदी के गहने', 'पुष्कर का गुलकंद और गुलाब जल', 'बंधेज और हिप्पी कपड़े', 'चमड़े के बैग और जूतियाँ'],
             ['Silver jewellery', 'Pushkar gulkand and rose water', 'Bandhej and boho clothing', 'Leather bags and mojaris']),
        reach=('पैदल — गाड़ियाँ अंदर नहीं जातीं।', 'On foot; vehicles are not allowed in.'),
        tip=('पहले दाम का 40–50% से मोलभाव शुरू करें। चाँदी के लिए हॉलमार्क/बिल माँगें।', 'Start bargaining at 40–50% of the first price. Ask for a hallmark or bill on silver.')),
    'desert': dict(
        intro=('पुष्कर के बाहर रेत के टीलों पर डेज़र्ट कैंप — ऊँट सफ़ारी, सूर्यास्त, लोक नृत्य और राजस्थानी खाना।',
               'Desert camps on the dunes outside Pushkar: camel safari, sunset, folk dance and Rajasthani dinner.'),
        see=(['ऊँट / जीप सफ़ारी', 'टीलों पर सूर्यास्त', 'कालबेलिया नृत्य', 'तारों भरा आसमान'], ['Camel or jeep safari', 'Sunset on the dunes', 'Kalbeliya dance', 'Starry night sky']),
        reach=('कस्बे से 3–8 किमी। ज़्यादातर कैंप पिक-अप देते हैं।', '3–8 km from town. Most camps offer pick-up.'),
        tip=('पैकेज में क्या शामिल है (खाना, सफ़ारी, ट्रांसफ़र) पहले लिखित में लें। ऊँट वाले से रेट पहले तय करें।', 'Get package inclusions (meal, safari, transfer) in writing. Fix the camel ride price before you start.')),
    'fair': dict(
        intro=('दुनिया के सबसे बड़े पशु मेलों में से एक — कार्तिक महीने में, कार्तिक पूर्णिमा तक। हज़ारों सजे ऊँट, लोक संगीत, प्रतियोगिताएँ और हॉट-एयर बैलून।',
               'One of the world’s largest livestock fairs, held in the Hindu month of Kartik and ending on Kartik Purnima. Thousands of decorated camels, folk music, contests and hot-air balloons.'),
        see=(['सजे हुए ऊँट और व्यापारी', 'मूंछ और पगड़ी प्रतियोगिता', 'हॉट-एयर बैलून', 'पूर्णिमा स्नान'], ['Decorated camels and traders', 'Moustache and turban contests', 'Hot-air balloons', 'Purnima holy dip']),
        reach=('मेला ग्राउंड कस्बे के पश्चिम में, पैदल 15–20 मिनट।', 'The fairground is west of town, 15–20 minutes on foot.'),
        tip=('मेले के दिनों में होटल 2–3 महीने पहले बुक करें, रेट 2–3 गुना हो जाते हैं। तारीख़ें Rajasthan Tourism पर देखें।', 'Book stays 2–3 months ahead; prices rise 2–3×. Check exact dates on Rajasthan Tourism.')),
    'ajmer': dict(
        intro=('पुष्कर से 15 किमी — ख़्वाजा मोइनुद्दीन चिश्ती की दरगाह, हर धर्म के लोगों की आस्था का केंद्र।', '15 km from Pushkar — the shrine of Khwaja Moinuddin Chishti, revered by people of every faith.'),
        reach=('नाग पहाड़ घाटी के रास्ते टैक्सी/बस से 30 मिनट।', '30 minutes by taxi or bus over the Nag Pahar ghat road.'),
        tip=('सिर ढककर जाएँ। भीड़ में जेब और फ़ोन का ध्यान रखें।', 'Cover your head. Watch your pockets and phone in the crowd.')),
    'anasagar': dict(
        intro=('अजमेर की 12वीं सदी की कृत्रिम झील, संगमरमर की बारादरी और शाम की ठंडी हवा।', 'Ajmer’s 12th-century man-made lake with marble pavilions (baradari) and a cool evening breeze.'),
        reach=('दरगाह से 3 किमी।', '3 km from the Dargah.'), tip=('दरगाह के बाद शाम यहाँ बिताएँ।', 'Spend the evening here after the Dargah.')),
}

# Traveller types: title, emoji, tips list
TYPES = [
    (('परिवार', 'Families'), '👨‍👩‍👧', (['सावित्री मंदिर के लिए रोपवे', 'झील किनारे का होटल — बच्चे पैदल घूम सकें', 'डेज़र्ट कैंप में शाम का कल्चरल शो', 'दोपहर 1–3 बजे आराम (मंदिर बंद)'],
                                          ['Ropeway for Savitri temple', 'Lakeside hotel so kids can walk everywhere', 'Cultural evening at a desert camp', 'Rest 1–3 PM while temples close'])),
    (('कपल', 'Couples'), '💑', (['छत वाले कैफ़े पर सूर्यास्त', 'टीलों पर निजी डिनर', 'हॉट-एयर बैलून (मेले में)', 'हेरिटेज हवेली स्टे'],
                                ['Sunset at a rooftop café', 'Private dinner on the dunes', 'Hot-air balloon (fair season)', 'Heritage haveli stay'])),
    (('सोलो / बैकपैकर', 'Solo & Backpackers'), '🎒', (['ब्रह्मा मंदिर के पास हॉस्टल ₹400–800', 'गायत्री मंदिर पर सूर्योदय', 'शेयर्ड ऊँट सफ़ारी', 'कैफ़े में दूसरे यात्रियों से मिलें'],
                                               ['Hostels near Brahma Temple ₹400–800', 'Sunrise at Gayatri temple', 'Shared camel safari', 'Meet travellers in the cafés'])),
    (('बुज़ुर्ग / तीर्थयात्री', 'Seniors & Pilgrims'), '🙏', (['सुबह जल्दी दर्शन, कम भीड़', 'घाट के पास धर्मशाला', 'सावित्री मंदिर सिर्फ़ रोपवे से', 'कार्तिक पूर्णिमा पर बहुत भीड़ — पहले से योजना'],
                                                       ['Early darshan, smaller crowds', 'Dharamshala near the ghats', 'Savitri temple by ropeway only', 'Kartik Purnima is very crowded — plan ahead'])),
    (('बजट ट्रैवलर', 'Budget travellers'), '💰', (['अजमेर तक ट्रेन, फिर ₹30–40 बस', 'थाली ₹150–250', 'ज़्यादातर मंदिर निःशुल्क', 'स्कूटी किराया ₹300–500/दिन'],
                                              ['Train to Ajmer, then a ₹30–40 bus', 'Thali for ₹150–250', 'Most temples are free', 'Scooter rental ₹300–500/day'])),
    (('फ़ोटोग्राफ़र', 'Photographers'), '📸', (['सूर्योदय: सावित्री पहाड़ी', 'गोल्डन आवर: गऊ घाट', 'मेले में पोर्ट्रेट — पहले अनुमति लें', 'नहाते लोगों की फ़ोटो कभी नहीं'],
                                         ['Sunrise: Savitri hill', 'Golden hour: Gau Ghat', 'Fair portraits — ask first', 'Never photograph people bathing'])),
]

DISTANCES = [
    (('पुष्कर', 'Pushkar'), ('अजमेर', 'Ajmer'), '15 km', ('30 मिनट', '30 min'), ('बस / टैक्सी', 'Bus / taxi')),
    (('पुष्कर', 'Pushkar'), ('किशनगढ़ एयरपोर्ट', 'Kishangarh Airport'), '~40 km', ('1 घंटा', '1 hr'), ('टैक्सी', 'Taxi')),
    (('पुष्कर', 'Pushkar'), ('जयपुर', 'Jaipur'), '~145 km', ('3 घंटे', '3 hr'), ('कार / बस', 'Car / bus')),
    (('पुष्कर', 'Pushkar'), ('जोधपुर', 'Jodhpur'), '~190 km', ('3.5–4 घंटे', '3.5–4 hr'), ('कार / बस', 'Car / bus')),
    (('पुष्कर', 'Pushkar'), ('उदयपुर', 'Udaipur'), '~280 km', ('5 घंटे', '5 hr'), ('कार / बस', 'Car / bus')),
    (('पुष्कर', 'Pushkar'), ('दिल्ली', 'Delhi'), '~410 km', ('7–8 घंटे', '7–8 hr'), ('ट्रेन अजमेर तक', 'Train to Ajmer')),
    (('ब्रह्मा मंदिर', 'Brahma Temple'), ('वराह घाट', 'Varaha Ghat'), '0.6 km', ('7 मिनट', '7 min'), ('पैदल', 'Walk')),
    (('ब्रह्मा मंदिर', 'Brahma Temple'), ('सावित्री रोपवे', 'Savitri ropeway'), '~2 km', ('10 मिनट', '10 min'), ('ई-रिक्शा', 'E-rickshaw')),
    (('बाज़ार', 'Bazaar'), ('मेला ग्राउंड', 'Fair ground'), '~1.5 km', ('20 मिनट', '20 min'), ('पैदल', 'Walk')),
    (('पुष्कर', 'Pushkar'), ('डेज़र्ट कैंप', 'Desert camps'), '3–8 km', ('15 मिनट', '15 min'), ('जीप / पिक-अप', 'Jeep / pick-up')),
]
