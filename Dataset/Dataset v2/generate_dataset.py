import csv
import random
import string

# --- CONFIGURATION ---
TARGET_COUNT_PER_CATEGORY = 500 
OUTPUT_FILENAME = "populse_dataset.csv"

# --- 1. CONTEXTUAL DATA (Naga City) ---
landmark_db = {
    "medical": [
        "Naga City Hospital", "Bicol Medical Center (BMC)", "Mother Seton Hospital", 
        "Plaza Medica", "St. John Hospital", "City Health Office", "Naga Imaging Center",
        "NICC Doctors Hospital", "Ago Foundation", "Metro Health"
    ],
    "education": [
        "Ateneo de Naga", "University of Nueva Caceres (UNC)", "Naga Central School", 
        "Camarines Sur National High School", "Naga City Science High School", 
        "Brentwood College", "Naga Parochial School", "Naga College Foundation (NCF)",
        "Tinago High School", "Concepcion Pequeña Elementary School", "BISCAST"
    ],
    "commercial": [
        "SM City Naga", "Robinsons Place", "LCC Mall", "Naga City People's Mall", 
        "Puregold", "Robertson Mall", "Public Market", "Unitop", "Gaisano Mall",
        "Vista Mall", "Deca Homes area", "Magsaysay Food Strip", "Diversion Road commercial area"
    ],
    "religious": [
        "Metropolitan Cathedral", "Basilica Minore", "San Francisco Church", 
        "Iglesia ni Cristo", "Peñafrancia Shrine", "Carmelite Monastery",
        "Our Lady of Immaculate Conception"
    ],
    "govt": [
        "City Hall", "Capitol", "Police Station 1", "Barangay Hall", 
        "Bicol Central Station", "Fire Station", "LTO Naga", "Hall of Justice",
        "Civic Center"
    ],
    "generic": [
        "Abella", "Bagumbayan", "Balatas", "Calauag", "Cararayan", "Carolina", 
        "Concepcion Grande", "Concepcion Pequeña", "Dayangdang", "Del Rosario", 
        "Dinaga", "Igualdad", "Lerma", "Liboton", "Mabolo", "Pacol", "Panicuason", 
        "Peñafrancia", "Sabang", "San Felipe", "San Francisco", "San Isidro", 
        "Santa Cruz", "Tabuco", "Tinago", "Triangulo"
    ]
}

prepositions = [
    "sa tapat ng", "sa likod ng", "near the gate of", "inside the vicinity of", 
    "sa may", "malapit sa", "front of", "beside", "sa parking ng", "across", "along"
]

# --- 2. MASSIVE SEED DATABASE (approx 100 per category) ---
seeds = {
    "health": [
        "tumataas ang cases ng dengue", "maraming bata ang nilalagnat", "walang doctor sa health center", 
        "ubos na ang gamot sa center", "need namin ng schedule for anti-rabies", "masungit ang nurse sa clinic", 
        "flu outbreak sa area namin", "requesting ambulance assistance", "daming lamok, need fumigation", 
        "walang available na covid vaccine", "high blood pressure monitoring request", "stray dogs chasing people", 
        "may nakagat ng aso", "positive sa leptospirosis", "heat stroke victim", "need oxygen tank", 
        "insulin for diabetes unavailable", "prenatal checkup schedule", "libreng tuli operation", 
        "medical mission request", "malnourished kids feeding", "diarrhea cases increasing", 
        "dirty water causing sickness", "sore eyes outbreak", "chicken pox spreading", "measles vaccine inquiry", 
        "animal bite center schedule", "emergency room full", "no attending physician", "nurse shift complaint", 
        "pharmacy ran out of paracetamol", "botika ng bayan inquiry", "free vitamins for seniors", 
        "dental services unavailable", "tooth extraction schedule", "pregnant women assistance", 
        "birthing home sanitation", "lying-in clinic closed", "midwife not available", "barangay health worker rude", 
        "blood donation drive schedule", "dialysis assistance request", "chemotherapy financial aid", 
        "mental health consultation", "depression hotline inquiry", "suicide prevention help", 
        "tuberculosis meds out of stock", "lung center referral", "heart center referral", 
        "kidney transplant assistance", "philhealth coverage inquiry", "malasakit center requirements", 
        "indigent patient assistance", "white card application", "yellow card renewal", "health certificate processing", 
        "sanitary permit for food", "food poisoning incident", "vomiting and dizziness reported", 
        "respiratory infection surge", "asthma attacks due to dust", "skin rashes outbreak", 
        "scabies infection in kids", "lice infestation in school", "deworming schedule", 
        "polio vaccine availability", "flu vaccine for seniors", "pneumonia vaccine inquiry", 
        "tetanus shot request", "rabies injection out of stock", "cat bite incident", 
        "rat bite concern", "snake bite emergency", "unknown insect bite swelling", 
        "allergic reaction assistance", "fainting incident in public", "heart attack emergency", 
        "stroke victim needs transport", "car accident victim medical help", "burn victim assistance", 
        "drowning incident first aid", "choking emergency", "poisoning emergency", "drug overdose suspicion", 
        "alcoholic liver disease help", "smoking cessation program", "vape regulation inquiry", 
        "health sanitation inspection", "quarantine protocol inquiry", "isolation facility status", 
        "contact tracing update", "rapid test kit availability", "swab test schedule", "health advisory request",
        "dengue misting request", "fogging schedule"
    ],
    "sanitation": [
        "sobrang baho ng kanal", "tambak na basura sa kalsada", "may patay na daga sa daan", 
        "marumi ang tubig na lumalabas sa gripo", "ipis infestation sa area", "amoy imbornal ang paligid", 
        "dumi ng aso sa sidewalk", "clogged drainage causing smell", "mabaho ang poultry", 
        "unsanitary street food vendors", "public toilet walang tubig at madumi", "nagkalat na used face masks",
        "puno na ang septic tank", "maraming langaw sa palengke", "estero cleaning needed", 
        "basura sa harap ng school", "amoy ihi ang pader", "dumudura kung saan saan", 
        "nagluluto sa maduming bangketa", "worms in tap water", "rusty water form faucet", 
        "muddy water supply", "bad smell from piggery", "chicken dung smell", "goat manure on road", 
        "cow dung scattering", "dead cat on street", "dead dog decomposing", "rotting garbage smell", 
        "leaking garbage truck juice", "flies swarming trash", "maggots in garbage pile", 
        "mosquito breeding ground", "stagnant water in tires", "open canal hazard", "overflowing sewage", 
        "burst sewage pipe", "human waste in river", "people defecating in river", "urinating in public", 
        "spitting momma everywhere", "vomit on sidewalk", "blood stains on road", "oil spill on road", 
        "grease trap overflow", "market stall dirty", "fish section smelly", "meat section unsanitary", 
        "rotten vegetables dumping", "fruit peelings scattered", "plastic cups clogging drain", 
        "styrofoam waste blocking flow", "diapers thrown in canal", "sanitary napkins on street", 
        "hospital waste mixed with trash", "hazardous waste dumping", "chemical smell from factory", 
        "smoke from burning rubber", "dust from construction", "mud from trucks", "sand clogging drainage", 
        "silt in river", "algae bloom in pond", "murky river water", "floating trash in river", 
        "dead fish in river", "rat infestation in market", "cockroach in restaurant", "hair in food complaint", 
        "dirty utensils in carinderia", "no hairnet food server", "dirty apron food vendor", 
        "handling food with bare hands", "sneezing on food", "coughing without mask", "dirty fingernails server", 
        "pest control in barangay hall", "disinfection of public area", "sanitize waiting shed", 
        "cleaning of public park", "grass cutting request", "overgrown weeds hiding trash", 
        "dog poop not picked up", "pet owners irresponsible", "piggery too close to houses", "poultry fly infestation"
    ],
    "infrastructure": [
        "ang lalim ng lubak sa daan", "sira ang tulay, delikado", "nakatagilid na ang poste", 
        "unfinished road works causing traffic", "bitak-bitak na ang pader", "busted ang street lights, madilim", 
        "walang sidewalk na madaanan", "falling debris from construction", "road widening project delay", 
        "sira ang bubong ng waiting shed", "baha sa kalsada", "bumabaha tuwing umuulan", "substandard road project",
        "walang drainage system", "guho ang lupa", "landslide prone area", "collapsed riprap sa ilog", 
        "defective solar lights", "renovation request", "cctv camera not working", "drainage cover is missing",
        "manhole walang takip", "open manhole danger", "steel plate on road slippery", "humps masyadong mataas", 
        "walang warning sign sa roadwork", "cracked concrete pavement", "aspalto natutunaw", "lubog ang kalsada", 
        "water lily blocking bridge", "bridge railing broken", "hanging bridge sway", "footbridge rusted", 
        "overpass dirty and dark", "underpass flooded", "waiting shed dilapidated", "basketball court sira ring", 
        "barangay hall leaking roof", "daycare center cracks", "school building condemned", "public market roof leaking", 
        "terminal flooring broken", "stage renovation request", "playground equipment broken", "swing set dangerous", 
        "seesaw broken", "slide rusted", "benches broken", "street sign missing", "street name painted over", 
        "traffic light sira", "pedestrian lane faded", "road markings invisible", "cat eyes missing", 
        "barrier broken", "divider destroyed", "fence collapsed", "gate broken", "wall leaning", 
        "structural integrity doubt", "building code violation", "encroachment on sidewalk", "illegal structure on road", 
        "post obstructing way", "tree roots destroying road", "tree branches hitting wire", "tree about to fall", 
        "soil erosion near house", "riverbank eroding", "dike breached", "flood control failure", 
        "pumping station not working", "sluice gate stuck", "canal silted up", "drainage disconnected", 
        "culvert collapsed", "road repair abandoned", "contractor ran away", "budget for road missing", 
        "ghost project reported", "white elephant building", "unfinished government building", 
        "basketball court no lights", "covered court roof hole", "plaza tiles broken", "fountain not working",
        "monument vandalized", "historical marker missing"
    ],
    "employment": [
        "delayed ang sweldo ng workers", "unfair labor practice sa trabaho", "looking for summer job for students", 
        "naghahanap ng trabaho", "discrimination sa hiring process", "walang benefits na binibigay", 
        "contractualization issue", "kailan ang next job fair", "inquiry for DOLE TUPAD program", 
        "unpaid overtime pay", "illegal dismissal complaint", "hiring ba ng security guard", 
        "openings for construction workers", "mababa ang pasahod", "employer not paying SSS contribution", 
        "job opening for senior high", "cash for work payout delay", "tesda training schedule", 
        "livelihood program for moms", "call center hiring", "work from home scam", "fake recruiter report", 
        "agency fee exorbitant", "placement fee complaint", "salary below minimum wage", "no 13th month pay", 
        "holiday pay not given", "night differential missing", "service incentive leave denied", 
        "maternity leave declined", "paternity leave refused", "sick leave deduction", "forced resignation", 
        "harassment in workplace", "sexual harassment at work", "unsafe working condition", "no ppe provided", 
        "hazard pay inquiry", "separation pay dispute", "retirement benefit calculation", "final pay delay", 
        "certificate of employment withheld", "clearance holding", "poaching of employees", "child labor report", 
        "senior citizen employment", "pwd employment quota", "discrimination against lgbt at work", 
        "age limit in hiring", "height requirement complaint", "appearance discrimination", "religious discrimination work", 
        "union busting activity", "strike dispersal violence", "labor inspector request", "dole complaint filing", 
        "nrcp clearance inquiry", "police clearance for work", "nbi clearance slot", "medical exam for work", 
        "drug test for employment", "resume writing assistance", "interview coaching help", "job portal city hall", 
        "pesonaga hiring list", "overseas employment listing", "ofw help desk", "illegal recruitment agency", 
        "human trafficking suspicion", "stay-in helper abuse", "kasambahay law violation", "driver boundary system", 
        "no contract signed", "endo contract renewal", "job order delay salary", "contract of service issue", 
        "government internship program", "spes requirements", "summer job application form"
    ],
    "public_safety": [
        "may nag-aaway na lasing", "may magnanakaw na umaaligid", "suspicious drug related activity", 
        "sobrang dilim ng eskinita", "akyat bahay incident report", "riot ng mga kabataan kagabi", 
        "snatching incident sa kanto", "suspicious person taking photos", "sobrang ingay ng videoke", 
        "curfew violation ng mga minor", "inom sa kalsada hanggang madaling araw", "drag racing ng motor sa gabi", 
        "vandalism sa pader", "may sunog sa residential area", "fire truck assistance needed", 
        "holdup incident report", "bato-bato sa sasakyan", "tanod sleeping on duty", "requesting police visibility", 
        "gang war threat", "missing person report", "kidnapping attempt", "human trafficking suspicion", 
        "rape attempt report", "sexual harassment in public", "catcalling complaint", "flashing incident", 
        "voyeurism report", "stalker alert", "domestic violence sounds", "child abuse shouting", 
        "animal cruelty report", "illegal gambling tupada", "cara y cruz on street", "video karera machine", 
        "fruit game gambling", "illegal possession of firearms", "gunshots heard", "explosion heard", 
        "bomb threat received", "terrorist suspicion", "checkpoint request", "police response slow", 
        "911 not answering", "emergency hotline busy", "ambulance late", "fire hydrant blocked", 
        "fire extinguisher missing", "smoke alarm broken", "fire exit locked", "gas leak smell", 
        "lpg explosion danger", "chemical spill hazard", "radioactive material suspicion", "biohazard waste exposed", 
        "rabid dog roaming", "snake entered house", "monitor lizard in ceiling", "bee hive dangerous", 
        "wasp nest removal", "wild monkey aggressive", "crocodile sighting", "drowning risk in river", 
        "falling tree branch", "electrocution hazard", "open pit danger", "construction accident", 
        "scaffolding collapse", "crane collapse fear", "glass falling from building", "elevator stuck", 
        "escalator accident", "stampede risk", "overcrowding violation", "social distancing violation", 
        "quarantine breach", "mask mandate violation", "fake id usage", "scammer alert", 
        "budol-budol gang", "dugo-dugo gang", "investment scam", "online scammer location", 
        "identity theft report", "cyberbullying report", "blackmail report", "extortion attempt"
    ],
    "utilities": [
        "walang tubig simula kanina", "brownout nanaman dito", "sobrang hina ng signal", 
        "may putol na kable sa daan", "fluctuating ang kuryente", "nawalan ng internet connection", 
        "water pipe leak sa kalsada", "sumabog ang transformer", "shocking electricity bill amount", 
        "illegal jumper connection report", "dirty water supply from faucet", "unannounced water interruption", 
        "dead spot area for globe/smart", "meter reading error complaint", "sparking wires sa poste", 
        "low water pressure tuwing umaga", "street light flickering on and off", "pldt down no service", 
        "converge no internet", "sky cable no signal", "casureco brownout schedule", "mnwd water interruption", 
        "prime water complaint", "high water bill", "wrong reading electric meter", "stolen electric meter", 
        "stolen water meter", "tampered seal meter", "flying connection report", "octopus connection fire hazard", 
        "leaning electric post", "rotten wood post", "termite infested post", "low lying wires", 
        "truck hit wire", "kite entangled in wire", "tree touching wire", "bird nest on transformer", 
        "substation noise", "voltage surge damage appliances", "low voltage aircon not working", 
        "frequent power blink", "scheduled blackout inquiry", "rotational brownout complaint", 
        "street light bulb busted", "street light sensor broken", "solar street light stolen", 
        "water pump broken", "water tank leaking", "water turbid", "water salty taste", 
        "water chlorine smell strong", "no water in second floor", "air lock in water pipe", 
        "illegal tapping of water", "wasting water car wash", "leaking fire hydrant", 
        "internet slow speed", "high latency ping", "packet loss internet", "fiber cut report", 
        "modem replacement request", "landline noisy static", "cannot call landline", 
        "mobile data slow", "cannot receive otp", "signal jammer suspicion", "cell tower radiation fear", 
        "cable tv fuzzy", "missing channels cable", "pay per view not working", "utility pole obstruction", 
        "guy wire dangerous", "insulator broken", "cross arm broken", "fuse cutout exploded"
    ],
    "waste_management": [
        "hindi dumaan ang garbage truck", "nagsusunog ng plastic ang kapitbahay", "pagtapon ng basura sa ilog", 
        "illegal dumping site sa vacant lot", "walang segregation policy", "kalat ang basura sa park", 
        "kailan ang schedule ng hakot", "basura bumabara sa drainage", "bulky waste pickup request", 
        "recycling inquiry", "walang garbage collector personnel", "di hinahakot ang nabubulok", 
        "basurahan puno na", "penalty for littering inquiry", "composting facility foul odor", 
        "tapon basura kahit saan", "mabaho ang mrF", "garbage truck juice leaking", "garbage truck noisy", 
        "garbage collector asking money", "garbage collector rude", "missed collection again", 
        "dogs scattering trash", "cats opening trash bags", "birds picking trash", "wind blowing trash", 
        "trash bins stolen", "trash bins broken", "no trash bins in plaza", "cigarette butts everywhere", 
        "candy wrappers litter", "plastic bottles scattered", "styrofoam pollution", "single use plastic violation", 
        "plastic straw ban inquiry", "ecobrick donation", "junk shop complaint", "scrap metal messy", 
        "burning leaves smoke", "burning rubber smell", "hospital waste mixed", "hazardous waste disposal", 
        "e-waste disposal where", "battery disposal bin", "light bulb disposal", "paint can disposal", 
        "construction debris dumping", "garden waste pickup", "tree cutting debris", "dead animal pickup", 
        "diaper disposal problem", "sanitary napkin clutter", "river cleanup request", "coastal cleanup schedule", 
        "estero rangers inactive", "basura patrol report", "no segregation no collection", 
        "biodegradable not collected", "recyclable collection schedule", "residual waste pile up", 
        "special waste handling", "infectious waste reported", "sharp object in trash", "broken glass danger", 
        "scavengers scattering trash", "waste picker complaint", "illegal landfill report", "open dumpsite smell", 
        "leachate contamination", "methane gas smell", "flies from dumpsite", "birds from dumpsite"
    ],
    "traffic": [
        "grabe ang traffic ngayon", "illegal parking sa kalsada", "counter-flow na tricycle", 
        "sira ang traffic light", "road obstruction by vendors", "no entry violation reports", 
        "tricycle overcharging fare", "congested intersection always", "jeepney cutting trip violation", 
        "colorum vehicles operating", "faded pedestrian lane markings", "loading/unloading violation", 
        "truck ban inquiry time", "traffic enforcer nangongotong", "double parking sa main road", 
        "traffic rerouting confusion", "road rage incident report", "walang traffic enforcer", 
        "one way violation", "u-turn violation", "beating the red light", "swerving violation", 
        "reckless driving report", "overspeeding motorcycle", "drag racing car", "drunk driving suspicion", 
        "texting while driving", "no helmet motorcycle", "overloading tricycle", "overloading jeep", 
        "topload passenger jeep", "hanging on jeepney", "tricycle refusal to convey", "tricycle rude driver", 
        "taxi meter not used", "taxi contracting fare", "grab car unavailable", "bus terminal chaotic", 
        "van terminal illegal", "pedicab on highway", "kuliglig on main road", "e-trike regulation", 
        "bicycle lane blocked", "motorcycle on bike lane", "car on bike lane", "vendor on bike lane", 
        "sidewalk parking", "driveway blocked", "fire hydrant blocked parking", "pwd ramp blocked", 
        "crosswalk blocked", "yellow box junction blocked", "jaywalking rampant", "pedestrian not respected", 
        "crossing guard needed", "school zone speeding", "hospital zone noise", "horn honking excessive", 
        "muffler loud noise", "smoke belching jeep", "smoke belching truck", "bus emitting black smoke", 
        "unregistered vehicle", "expired registration", "no license plate", "fake license plate", 
        "conduction sticker missing", "student driver unattended", "driving without license", 
        "fake license used", "towing request", "clamped vehicle inquiry", "ticket contestation", 
        "traffic adjudication office", "coding scheme inquiry", "number coding violation", 
        "window hour inquiry", "truck ban exemption", "delivery truck blocking road", "container van parking", 
        "jeepney strike stranded", "transport strike update", "libre sakay schedule", "puj phaseout concern"
    ],
    "social_services": [
        "wala pa kaming natatanggap na ayuda", "status of scholarship application", "senior citizen pension delay", 
        "paano kumuha ng pwd id", "kulang ang binigay na relief goods", "burial assistance request", 
        "4ps beneficiary inquiry", "solo parent benefits inquiry", "medical assistance for indigent", 
        "birthday cash gift for senior", "feeding program request for kids", "vawc desk assistance needed", 
        "child abuse report", "lost id replacement process", "financial aid for poor students", 
        "calamity loan inquiry", "social pension payout schedule", "binaha ang bahay need relief goods",
        "nasunugan need assistance", "typhoon victim help", "earthquake assistance", "evacuation center status", 
        "relief operation schedule", "food pack distribution", "cash assistance payout", "educational assistance payout", 
        "uniform allowance student", "school supplies distribution", "free tablet for students", "laptop loan for teachers", 
        "daycare center enrollment", "supplemental feeding program", "milk feeding program", "nutribun distribution", 
        "senior citizen booklet", "movie privilege senior", "medicine discount senior", "grocery discount senior", 
        "pwd booklet missing", "pwd accessibility ramp", "sign language interpreter", "braille materials request", 
        "wheelchair donation request", "cane for blind request", "hearing aid assistance", "prosthetic leg help", 
        "solo parent id renewal", "solo parent leave benefit", "solo parent scholarship", "4ps delisting complaint", 
        "4ps pawning cash card", "4ps gambling money", "listahan inquiry", "indigent certification", 
        "certificate of residency", "barangay clearance fee", "cedula application", "voter registration schedule", 
        "comelec satellite office", "wedding civil ceremony", "mass wedding schedule", "birth certificate correction", 
        "late registration birth", "death certificate error", "marriage license requirement", "cenomar request", 
        "foundling child report", "adoption process inquiry", "foster care application", "orphanage donation", 
        "home for the aged visit", "street children rescue", "mendicancy law violation", "beggars on street", 
        "badjao scattering trash", "indigenous people assistance", "tribal hall request", "muslim community help", 
        "gender development program", "women's month activity", "children's month contest", "family week celebration", 
        "drug rehabilitation referral", "balay silangan status", "community service inquiry", "volunteer program join"
    ]
}

# --- 3. CODE-SWITCHING ENGINE (Language Modes) ---
vocab_map = {
    # Tagalog to English
    "sa": "in", "ang": "the", "ng": "of", "mga": "the", "may": "there is",
    "wala": "no", "walang": "no", "kami": "us", "ako": "me", "niyo": "you",
    "dito": "here", "kasi": "because", "naman": "please", "po": "", "lang": "just",
    "sira": "broken", "mabaho": "smelly", "madumi": "dirty", "tubig": "water",
    "gamot": "medicine", "lagnat": "fever", "ubo": "cough", "bata": "children",
    "matanda": "elderly", "bahay": "house", "daan": "road", "kalsada": "street",
    "lubak": "potholes", "tulay": "bridge", "ilaw": "lights", "poste": "post",
    "basura": "trash", "kanal": "canal", "daga": "rats", "ipis": "roaches",
    "aso": "dog", "pusa": "cat", "patay": "dead", "amoy": "smell",
    "sweldo": "salary", "trabaho": "job", "sahod": "wages", "kulang": "lacking",
    "magnanakaw": "thief", "dilim": "dark", "ingay": "noise", "lasing": "drunk",
    "bato": "stone", "away": "fight", "droga": "drugs",
    "kuryente": "electricity", "kable": "cable", "mahina": "weak",
    "sunog": "burning", "tapon": "throw", "kalat": "litter", "hakot": "collection",
    "grabe": "severe", "trapik": "traffic", "buhol-buhol": "congested",
    "ayuda": "aid", "tagal": "delay", "tumataas": "rising", "maraming": "many",
    "ubos": "out of stock", "masungit": "rude", "daming": "many",
    "sobrang": "very", "tambak": "piled up", "marumi": "dirty", "lumalabas": "coming out",
    "gripo": "faucet", "paligid": "surroundings", "nakatambak": "piled",
    "nagkalat": "scattered", "puno": "full", "lalim": "deep", "nakatagilid": "leaning",
    "bitak-bitak": "cracked", "pader": "wall", "bubong": "roof", "naghahanap": "looking for",
    "binibigay": "given", "kailan": "when", "umaaligid": "lurking", "madaling araw": "dawn",
    "simula": "since", "kanina": "earlier", "hina": "weak", "putol": "cut",
    "nawalan": "lost", "sumabog": "exploded", "hindi": "did not", "dumaan": "pass",
    "kapitbahay": "neighbor", "bumabara": "clogging", "hinahakot": "collected",
    "nabubulok": "biodegradable", "nangongotong": "extorting", "natatanggap": "received",
    "paano": "how", "kumuha": "get", "binigay": "given", "nagsusunog": "burning",
    "baha": "flood", "bumabaha": "flooding", "lubog": "submerged",
    
    # English to Tagalog
    "report": "sumbong", "complaint": "reklamo", "requesting": "hiling",
    "need": "kailangan", "help": "tulong", "urgent": "madalian",
    "please": "pakiusap", "check": "suriin", "fix": "ayusin",
    "update": "balita", "concern": "problema", "inquiry": "tanong",
    "located": "matatagpuan", "regarding": "ukol sa", "assistance": "tulong",
    "dangerous": "delikado", "smelly": "mabaho", "dirty": "madumi",
    "broken": "sira", "traffic": "trapik", "delay": "antala",
    "salary": "sahod", "water": "tubig", "lights": "ilaw",
    "road": "kalsada", "bridge": "tulay", "trash": "basura",
    "cases": "kaso", "outbreak": "pagkalat", "schedule": "iskedyul",
    "monitoring": "pagbabantay", "chasing": "hinahabol", "medication": "gamot",
    "infestation": "peste", "vendors": "tindero", "cleaning": "paglinis",
    "construction": "konstruksyon", "renovation": "pinaayos", "practice": "gawain",
    "hiring": "tumatanggap", "violation": "paglabag", "incident": "insidente",
    "leak": "tulo", "interruption": "kawalan", "collection": "koleksyon",
    "segregation": "paghihiwalay", "congestion": "sikip", "confusion": "kalituhan",
    "application": "aplikasyon", "pension": "pensyon", "replacement": "pagpalit",
    "flood": "baha", "flooding": "pagbaha"
}

def apply_code_switch(text, mode):
    if mode == "taglish": return text
    words = text.split()
    new_words = []
    for word in words:
        clean = word.lower().translate(str.maketrans('', '', '.,!?'))
        if clean in vocab_map:
            if mode == "english":
                replacement = vocab_map[clean]
                new_words.append(replacement)
            elif mode == "tagalog":
                replacement = vocab_map[clean]
                new_words.append(replacement)
            else:
                new_words.append(word)
        else:
            new_words.append(word)
    return " ".join(new_words)

# --- 4. ANTI-OVERFIT AUGMENTERS ---
synonym_map_taglish = {
    "report": ["sumbong", "ireport", "file ng complaint", "ipaalam", "raise ng concern", "reklamo"],
    "need": ["kailangan", "need namin", "we need", "gusto sana namin", "requesting"],
    "help": ["tulong", "assist", "saklolo", "tabang", "helppp"],
    "sira": ["broken", "di gumagana", "wasak", "palpak", "defect", "not working"],
    "mabaho": ["mapanghi", "smelly", "stinky", "amoy patay", "nakakasuka ang amoy"],
    "traffic": ["trapik", "mausad", "congested", "gridlock", "buhol-buhol"],
    "delay": ["matagal", "late", "antagal", "petsa na", "bagal"],
    "kailan": ["kelan", "when", "ano oras", "what time", "kailan kaya"],
    "barangay": ["brgy", "baranggay", "area namin", "lugar namin", "vicinity"],
    "sa": ["s", "dito sa", "sa may", "near", "loc:"],
    "ang": ["yung", "ung", "ang mga", "ng"],
    "please": ["pls", "paki", "sana", "kindly", "parang awa niyo na"],
    "wala": ["ala", "walang", "zero", "no", "missing"],
    "grabe": ["lala", "sobra", "grabeh", "tindi"],
    "check": ["inspect", "tignan", "paki-check", "silipin"],
}

synonym_map_eng = {
    "report": ["file a complaint about", "notify you regarding", "inform you about", "raise an issue on"],
    "need": ["require", "are requesting", "demand", "ask for"],
    "help": ["assistance", "aid", "support", "immediate action"],
    "broken": ["defective", "busted", "damaged", "not functioning"],
    "smelly": ["stinky", "foul odor", "bad smell", "unpleasant odor"],
    "traffic": ["congestion", "gridlock", "heavy traffic", "jam"],
    "delay": ["hold up", "lateness", "slow service"],
    "please": ["kindly", "could you please", "we ask you to"],
    "check": ["inspect", "investigate", "look into", "examine"],
    "located": ["situated", "found", "happening", "occurring"],
    "assistance": ["help", "support", "intervention"]
}

synonym_map_tag = {
    "sumbong": ["ireklamo", "ipagbigay-alam", "sabihin"],
    "kailangan": ["nais", "gusto", "hangad"],
    "tulong": ["saklolo", "ayuda"],
    "sira": ["wasak", "di gumagana", "palpak"],
    "mabaho": ["mapanghi", "masangsang", "amoy patay"],
    "trapik": ["sikip ng daloy", "buhol-buhol"],
    "matagal": ["antagal", "kupad", "bagal"],
    "kailan": ["kelan", "ano oras"],
    "pakiusap": ["maaari ba", "sana naman", "parang awa niyo na"],
    "suriin": ["tignan", "silipin", "imbestigahan"],
    "ayusin": ["kumpunihin", "gawan ng paraan"],
    "problema": ["suliranin", "aberya"]
}

def augment_text(text, mode="taglish"):
    words = text.split()
    new_sentence = []
    if mode == "english": current_map = synonym_map_eng
    elif mode == "tagalog": current_map = synonym_map_tag
    else: current_map = synonym_map_taglish

    for word in words:
        clean_word = word.lower().translate(str.maketrans('', '', '.,!?'))
        if clean_word in current_map and random.random() < 0.30:
            replacement = random.choice(current_map[clean_word])
            if word[0].isupper(): replacement = replacement.capitalize()
            if word.endswith("."): replacement += "."
            elif word.endswith(","): replacement += ","
            elif word.endswith("!"): replacement += "!"
            new_sentence.append(replacement)
        elif random.random() < 0.02 and len(word) > 4: # Fat finger
            char_idx = random.randint(1, len(word)-2)
            word_list = list(word)
            if random.random() < 0.5: word_list[char_idx] = 'x'
            else: del word_list[char_idx]
            new_sentence.append("".join(word_list))
        else:
            new_sentence.append(word)
    return " ".join(new_sentence)

# --- 5. THE GENERATOR LOGIC ---
def get_confusing_location(category):
    prep = random.choice(prepositions)
    if category == "traffic": loc_type = random.choice(["medical", "education", "religious", "commercial"])
    elif category == "health": loc_type = random.choice(["education", "commercial", "govt"])
    elif category == "sanitation": loc_type = random.choice(["medical", "religious", "govt"])
    elif category == "public_safety": loc_type = random.choice(["religious", "education", "generic"])
    else: loc_type = random.choice(list(landmark_db.keys()))
    landmark = random.choice(landmark_db[loc_type])
    return f"{prep} {landmark}"

def generate_row(category):
    base_issue = random.choice(seeds[category])
    
    if random.random() < 0.5: loc = get_confusing_location(category)
    else: loc = random.choice(landmark_db["generic"]) 
    
    rand_val = random.random()
    if rand_val < 0.8: mode = "taglish"
    elif rand_val < 0.9: mode = "english"
    else: mode = "tagalog"

    processed_issue = apply_code_switch(base_issue, mode)
    if mode == "english":
        loc = loc.replace("sa tapat ng", "in front of").replace("sa likod ng", "behind").replace("sa may", "near").replace("malapit sa", "near").replace("sa parking ng", "at the parking of")

    text = ""
    if mode == "english":
        templates = [
            f"I am writing to formally report {processed_issue} in {loc}.",
            f"We are requesting immediate assistance regarding {processed_issue} near {loc}.",
            f"Please be informed that there is {processed_issue} at {loc}.",
            f"This is a notification about {processed_issue} located at {loc}.",
            f"Concern: {processed_issue} observed in {loc}. Please investigate.",
            f"I noticed {processed_issue} in {loc}. Hoping for action.",
            f"Alert: {processed_issue} detected at {loc}.",
            f"Kindly check {loc} due to {processed_issue}.",
            f"We need help with {processed_issue} around {loc}.",
        ]
        text = augment_text(random.choice(templates), mode="english")
        
    elif mode == "tagalog":
        templates = [
            f"Nais ko pong ipagbigay alam na {processed_issue} sa {loc}.",
            f"Humihingi po kami ng tulong dahil {processed_issue} sa {loc}.",
            f"Maari po bang aksyunan ang {processed_issue} dito sa {loc}.",
            f"Sumbong ko lang po ang {processed_issue} sa may {loc}.",
            f"Pakitignan naman po ang {processed_issue} sa {loc}. Salamat.",
            f"Kailan po maaayos ang {processed_issue} sa {loc}?",
            f"Pakiusap, may {processed_issue} sa {loc}.",
            f"May problema sa {loc}: {processed_issue}.",
            f"Tulungan niyo kami sa {loc}, {processed_issue}.",
        ]
        text = augment_text(random.choice(templates), mode="tagalog")
        
    else: # Taglish
        style = random.choice(["formal", "netizen", "sms", "concerned"])
        if style == "formal":
            templates = [
                f"I would like to report that {base_issue} {loc}.",
                f"Good day. Requesting assistance: {base_issue} {loc}.",
                f"Formal complaint: {base_issue} located {loc}.",
            ]
        elif style == "netizen":
            templates = [
                f"Grabe naman, {base_issue} dito {loc}! Ano na??",
                f"Huy pansinin niyo naman to. {base_issue} {loc}. Nakaka-stress!",
                f"Shoutout sa LGU, {base_issue} {loc}. Please actionan agad.",
            ]
        elif style == "sms":
            templates = [
                f"Report ko lng {base_issue} {loc}.",
                f"Help. {base_issue} {loc}. Pls fix.",
                f"Urgent: {base_issue} {loc}.",
            ]
        elif style == "concerned":
            templates = [
                f"Ask ko lang po kung may action na, {base_issue} kasi dito {loc}.",
                f"Concerned lang po kami sa mga bata, {base_issue} {loc}.",
                f"Kami po ay taga {loc}, report ko lang na {base_issue}.",
            ]
        
        raw_tmpl = random.choice(templates)
        if style == "sms": raw_tmpl = raw_tmpl.replace("ang", "ng").replace("sa", "s")
        text = augment_text(raw_tmpl, mode="taglish")

    if random.random() < 0.05: text = text.upper()
    elif random.random() < 0.05: text = text.lower()

    return [text, category]

def main():
    data = []
    print("Generating POPULSE ULTIMATE DATASET...")
    for category in seeds.keys():
        for _ in range(TARGET_COUNT_PER_CATEGORY):
            data.append(generate_row(category))
    random.shuffle(data)
    with open(OUTPUT_FILENAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["text", "category"])
        writer.writerows(data)
    print(f"SUCCESS! Generated {len(data)} rows in {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()