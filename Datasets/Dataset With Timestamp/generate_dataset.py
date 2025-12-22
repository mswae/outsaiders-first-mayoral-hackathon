import csv
import random
import string
import re
from datetime import datetime, timedelta

"""
PEOPULSE DATASET GENERATOR (v3.0)
--------------------------------
A script to generate synthetic, code-switched (Tagalog-English), and 
timestamped complaints data for Naga City context.

Features:
1. Fat-finger typo generation.
2. Context-aware code-switching (Nouns/Adjectives only).
3. 5 Distinct sentence structure templates to prevent overfitting.
4. Weighted category distribution based on real-world probability.
"""

# --- CONFIGURATION ---
TOTAL_ROWS = 500
OUTPUT_FILENAME = "peopulse_dataset_timestamped.csv"
START_DATE = datetime(2025, 7, 1, 0, 0, 0)
END_DATE = datetime(2025, 12, 31, 23, 59, 59)

# Probability distribution for categories (Real-world simulation)
CATEGORY_WEIGHTS = {
    "social_services": 0.25,        
    "utilities": 0.20,     
    "sanitation": 0.15,    
    "health": 0.10,        
    "public_safety": 0.10,
    "infrastructure": 0.08, 
    "traffic": 0.07, 
    "employment": 0.05      
}

# --- 1. CONTEXTUAL DATA (Naga City) ---
landmark_db = {
    "medical": [
        "Naga City Hospital", "Bicol Medical Center (BMC)", "Mother Seton Hospital", 
        "Plaza Medica", "St. John Hospital", "City Health Office", "Naga Imaging Center",
        "NICC Doctors Hospital", "Ago Foundation", "Metro Health", "Bicol AccessHealth",
        "Our Lady of Lourdes Infirmary", "Isarog Family Care"
    ],
    "education": [
        "Ateneo de Naga", "University of Nueva Caceres (UNC)", "Naga Central School", 
        "Camarines Sur National High School (CamHigh)", "Naga City Science High School", 
        "Brentwood College", "Naga Parochial School", "Naga College Foundation (NCF)",
        "Tinago High School", "Concepcion Pequeña Elementary School", "BISCAST",
        "Mariners Polytechnic", "STI College Naga", "WRI College", "AMA Computer College"
    ],
    "commercial": [
        "SM City Naga", "Robinsons Place", "LCC Mall", "Naga City People's Mall", 
        "Puregold", "Robertson Mall", "Public Market", "Unitop", "Gaisano Mall",
        "Vista Mall", "Deca Homes area", "Magsaysay Food Strip", "Diversion Road commercial area",
        "Yashano Mall", "Super Metro", "Primark Town Center"
    ],
    "religious": [
        "Metropolitan Cathedral", "Basilica Minore", "San Francisco Church", 
        "Iglesia ni Cristo", "Peñafrancia Shrine", "Carmelite Monastery",
        "Our Lady of Immaculate Conception", "Holy Cross Parish", "San Jude Thaddeus Parish"
    ],
    "govt": [
        "City Hall", "Capitol", "Police Station 1", "Barangay Hall", 
        "Bicol Central Station", "Fire Station", "LTO Naga", "Hall of Justice",
        "Civic Center", "IPO Naga", "NBI Office", "Comelec Office"
    ],
    "generic": [
        "Abella", "Bagumbayan", "Balatas", "Calauag", "Cararayan", "Carolina", 
        "Concepcion Grande", "Concepcion Pequeña", "Dayangdang", "Del Rosario", 
        "Dinaga", "Igualdad", "Lerma", "Liboton", "Mabolo", "Pacol", "Panicuason", 
        "Peñafrancia", "Sabang", "San Felipe", "San Francisco", "San Isidro", 
        "Santa Cruz", "Tabuco", "Tinago", "Triangulo"
    ]
}

# --- 2. FILLER DATA ---
intros = [
    "Hello admin,", "Good day,", "Ask ko lang,", "Report ko lang,", "Paki-check naman,", 
    "To whom it may concern,", "Admin,", "Mayor,", "Help,", "Urgent:", "Notice:", 
    "Excuse me,", "Hoy,", "Grabe,", "Anuna,", "Pansinin niyo to,", "FYI,"
]

closers = [
    "please action.", "aksyonan agad.", "nakakaabala na.", "delikado to.", 
    "thanks.", "salamat.", "waiting for action.", "kailan ito maaayos?", 
    "any update?", "pls fix.", "asap.", "nakakatakot.", "hassle masyado.", 
    "ang tagal na nito.", "paki-ayos please."
]

# Words used to connect a location to an issue (e.g., "Sa Ateneo -> MAY -> baha")
connectors = ["may", "merong", "please check", "report ko", "yung", "ganap sa", "banda sa"]

prepositions_en = ["near", "in front of", "behind", "at", "inside", "outside", "along", "across"]
prepositions_tl = ["sa may", "sa tapat ng", "sa likod ng", "sa", "sa loob ng", "sa labas ng", "sa kanto ng"]

# --- 3. SEED DATABASE (The Knowledge Base) ---
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
        "dengue misting request", "fogging schedule", "maternal health concern", "infant vaccination missed",
        "hand foot mouth disease alert", "cholera suspicion", "typhoid fever cases", "hepatitis outbreak warning",
        "hiv testing confidentiality", "aids awareness program", "teen pregnancy counseling", 
        "family planning supplies", "contraceptives out of stock", "vasectomy inquiry", "ligation schedule",
        "post-partum depression help", "breastfeeding station unavailable", "nutritional status check",
        "stunting in children survey", "obesity counseling", "diabetes screening free", "hypertension screening",
        "eye checkup free", "hearing test for seniors", "physical therapy assistance", "rehab center referral",
        "ambulance fuel shortage", "ambulance driver missing", "health center dilapidated", "clinic aircon broken",
        "medical equipment defective", "expired medicines reported", "wrong medication given", "doctor negligence",
        "nurse malpractice complaint", "hospital bill dispute", "promissory note hospital", "blood bank empty",
        "plasma donation request", "platelet donor needed", "organ donor inquiry", "medical waste improper disposal",
        "used syringe found", "biohazard bag open", "face mask littering clinic", "gloves scattered hospital"
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
        "dog poop not picked up", "pet owners irresponsible", "piggery too close to houses", 
        "poultry fly infestation", "backyard piggery smell", "illegal slaughtering", "blood from slaughterhouse",
        "feathers scattering road", "animal entrails in river", "fish port slimy", "public faucet algae",
        "communal toilet blocked", "portalet full", "feces on footbridge", "urine smell underpass",
        "vandalism with feces", "diaper hanging on tree", "sanitary pad in toilet bowl", "condoms scattered park",
        "needles found playground", "broken glass in sand", "rusty nails on road", "sharp metal debris",
        "construction dust asthma", "cement mixer spill", "paint thinner smell", "gasoline smell residential",
        "kerosene spill", "rotten meat selling", "double dead meat", "expired canned goods selling",
        "weevil in rice NFA", "moldy bread selling", "dirty ice plant", "water refilling station dirty",
        "no sanitary permit business", "health certificate fake food", "rodent control request"
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
        "monument vandalized", "historical marker missing", "baha sa loob ng bahay", "knee deep flood",
        "waist deep flood", "neck deep flood", "impassable road due to flood", "floodwaters entering shop",
        "mud after flood", "debris after flood", "road washed away", "bridge washed away",
        "retaining wall collapse", "riprap weak", "sandbag request flood", "dredging request river",
        "desilting of canal needed", "floodway blocked", "spillway damaged", "dam gate stuck",
        "irrigation canal dry", "farm to market road sira", "rough road complaint", "dusty road complaint",
        "muddy road complaint", "asphalt overlay peeling", "cement curing too long", "excavation left open",
        "road hazard unlit", "construction materials on road", "scaffolding unsafe", "crane blocking view"
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
        "government internship program", "spes requirements", "summer job application form", "sweldo delay",
        "sahod hindi binigay", "pay slip missing", "wrong computation of salary", "illegal deduction salary",
        "uniform deduction illegal", "cash bond illegal", "training bond dispute", "non-compete clause issue",
        "awol termination", "constructive dismissal", "floating status employee", "redundancy separation",
        "retrenchment notice", "closure of business pay", "bankruptcy claims worker", "nlrc case filing",
        "sena conference schedule", "labor arbiter hearing", "collective bargaining agreement", "union dues dispute",
        "shuttle service complaint", "canteen food work complaint", "restroom at work dirty", "aircon at work broken",
        "ventilation poor at work", "lighting poor at work", "ergonomics bad chair", "heavy lifting injury",
        "repetitive strain injury", "burnout work load", "mental health work stress", "toxic boss report",
        "abusive supervisor", "bullying in office", "gossip destroying reputation", "favoritism in promotion"
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
        "identity theft report", "cyberbullying report", "blackmail report", "extortion attempt",
        "carnapping incident report", "nagnakaw ng motor", "stolen motorcycle report", "motornapping incident",
        "binaril sa harap ng hospital", "sinaksak sa tapat ng school", "holdup sa tapat ng mall",
        "riding in tandem shooting", "motorcycle riding criminal", "agaw cellphone sa jeep",
        "may dalang baril sa ospital", "security guard binaril", "crime scene sa clinic",
        "pickpocket sa palengke", "salisi gang sa mall", "ipit taxi gang", "bukas kotse gang",
        "basag kotse gang", "akyat barko theft", "piracy at sea", "smuggling report",
        "illegal fishing dynamite", "illegal logging report", "kaingin fire report", "arson suspicion",
        "grass fire spreading", "forest fire smoke", "burning building trapped", "fire alarm false",
        "fire drill request", "earthquake drill request", "tsunami alert siren", "flood warning siren"
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
        "guy wire dangerous", "insulator broken", "cross arm broken", "fuse cutout exploded", 
        "electric shock from appliance", "grounding issue house", "loose connection meter",
        "application for new meter", "relocation of post request", "bill delivery late",
        "bill lost in transit", "online payment not reflecting", "overpayment refund",
        "disconnection notice received", "reconnection fee inquiry", "change name account",
        "senior citizen discount utility", "lifeline rate inquiry", "net metering application",
        "solar panel grid tie", "generator noise complaint", "generator smoke complaint",
        "water rationing schedule", "water truck request", "deep well permit inquiry"
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
        "leachate contamination", "methane gas smell", "flies from dumpsite", "birds from dumpsite", 
        "dump truck overloading", "falling trash from truck", "garbage truck obstructing traffic", 
        "garbage truck accident", "recycling center hours", "junk shop buying price", "plastic ban exemption", 
        "bring your own bag policy", "reusable container sanitation", "food waste composting", 
        "vermicasting worms request", "bokashi composting help", "community garden compost", 
        "zero waste seminar", "upcycling workshop", "waste to energy inquiry", "biogas plant smell", 
        "sludge disposal septic", "grease trap cleaning waste", "used oil disposal", 
        "tires disposal where", "furniture disposal help", "appliance disposal help"
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
        "jeepney strike stranded", "transport strike update", "libre sakay schedule", "puj phaseout concern", 
        "jeepney route modification", "tricycle fare matrix", "senior discount transport", "student discount fare", 
        "pwd discount transport", "overcharging taxi airport", "uv express overloading", "colorum van reporting", 
        "bus trip cancellation", "early bus departure", "late bus arrival", "lost baggage bus", 
        "rude bus conductor", "unsafe driving bus", "sleepy driver bus", "distracted driver bus", 
        "car breakdown traffic", "truck breakdown blocking", "accident investigation", "hit and run report", 
        "sideswipe incident", "rear end collision", "head on collision", "multiple vehicle collision", 
        "motorcycle spilling oil", "cargo falling from truck", "loose gravel on road", "animals crossing road"
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
        "drug rehabilitation referral", "balay silangan status", "community service inquiry", "volunteer program join", 
        "red cross blood drive", "disaster preparedness seminar", "first aid training request", "livelihood training tesda", 
        "urban gardening seeds", "fingerlings dispersal", "livestock dispersal", "veterinary mission", 
        "rabies vaccination pet", "spay and neuter free", "legal aid free", "public attorney office", 
        "consumer complaint dti", "price watch report", "overpricing complaint", "hoarding complaint", 
        "profiteering complaint", "senior citizen abuse", "pwd discrimination", "solo parent discrimination", 
        "vawc restraining order", "child custody help", "child support demand", "annulment process help"
    ]
}

# --- 4. SMART CODE-SWITCHING ENGINE ---
vocab_map = {
    # Tagalog to English
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
    "sobrang": "very", "tambak": "piled up", "marumi": "dirty",
    "gripo": "faucet", "paligid": "surroundings", "nakatambak": "piled",
    "nagkalat": "scattered", "puno": "full", "lalim": "deep", "nakatagilid": "leaning",
    "bitak-bitak": "cracked", "pader": "wall", "bubong": "roof", "naghahanap": "looking for",
    "binibigay": "given", "kailan": "when", "umaaligid": "lurking",
    "simula": "since", "kanina": "earlier", "hina": "weak", "putol": "cut",
    "nawalan": "lost", "sumabog": "exploded",
    "kapitbahay": "neighbor", "bumabara": "clogging", "hinahakot": "collected",
    "nabubulok": "biodegradable", "nangongotong": "extorting", "natatanggap": "received",
    "paano": "how", "kumuha": "get", "binigay": "given", "nagsusunog": "burning",
    "baha": "flood", "bumabaha": "flooding", "lubog": "submerged",
    
    # English to Tagalog
    "report": "sumbong", "complaint": "reklamo", "requesting": "hiling",
    "need": "kailangan", "help": "tulong", "urgent": "madalian",
    "check": "suriin", "fix": "ayusin", "update": "balita", "concern": "problema", 
    "inquiry": "tanong", "assistance": "tulong", "dangerous": "delikado", 
    "smelly": "mabaho", "dirty": "madumi", "broken": "sira", "traffic": "trapik", 
    "delay": "antala", "salary": "sahod", "water": "tubig", "lights": "ilaw",
    "road": "kalsada", "bridge": "tulay", "trash": "basura", "cases": "kaso", 
    "outbreak": "pagkalat", "schedule": "iskedyul", "medication": "gamot",
    "infestation": "peste", "vendors": "tindero", "cleaning": "paglinis",
    "construction": "konstruksyon", "renovation": "pinaayos", 
    "hiring": "tumatanggap", "violation": "paglabag", "incident": "insidente",
    "leak": "tulo", "interruption": "kawalan", "collection": "koleksyon",
    "segregation": "paghihiwalay", "congestion": "sikip", "confusion": "kalituhan",
    "application": "aplikasyon", "pension": "pensyon", "flood": "baha"
}

def apply_code_switch(text, mode):
    """
    Translates keywords based on the mode (english/tagalog) using regex
    to preserve punctuation (e.g. 'tubig,' stays 'water,').
    """
    if mode == "taglish": return text
    
    words = text.split()
    new_words = []
    
    for word in words:
        match = re.match(r"([^\w\s]*)([\w'-]+)([^\w\s]*)", word)
        if match:
            prefix, core_word, suffix = match.groups()
            clean_core = core_word.lower()
            
            if clean_core in vocab_map:
                replacement = vocab_map[clean_core]
                if core_word[0].isupper():
                    replacement = replacement.capitalize()
                new_words.append(f"{prefix}{replacement}{suffix}")
            else:
                new_words.append(word)
        else:
            new_words.append(word)
            
    return " ".join(new_words)

# --- 5. AUGMENTATION ---
# QWERTY adjacency keys for realistic "Fat Finger" typos
adj_keys = {
    'a': 'qsxz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfc', 'e': 'wsdfr',
    'f': 'dcvgt', 'g': 'fbhuy', 'h': 'gvjki', 'i': 'ujko', 'j': 'hnmki',
    'k': 'jmlo', 'l': 'kpo', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awzdx', 't': 'rfgy',
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu', 'z': 'asx'
}

def augment_text(text):
    """
    Applies realistic noise to the text:
    1. 3% chance of a "fat finger" typo (hitting adjacent key).
    2. 10% chance of text-speak (shortening words).
    """
    words = text.split()
    new_sentence = []

    for word in words:
        clean_word = word.lower().translate(str.maketrans('', '', '.,!?'))
        if random.random() < 0.03 and len(word) > 4: 
            char_idx = random.randint(1, len(word)-2)
            char = word[char_idx].lower()
            if char in adj_keys:
                replacement_char = random.choice(adj_keys[char])
                word_list = list(word)
                word_list[char_idx] = replacement_char
                new_sentence.append("".join(word_list))
            else:
                word_list = list(word)
                del word_list[char_idx]
                new_sentence.append("".join(word_list))
        elif random.random() < 0.10:
            if clean_word == "please": new_sentence.append("pls")
            elif clean_word == "sana": new_sentence.append("sna")
            elif clean_word == "kayo": new_sentence.append("kau")
            elif clean_word == "dito": new_sentence.append("dto")
            elif clean_word == "dahil": new_sentence.append("kc")
            elif clean_word == "kasi": new_sentence.append("kc")
            elif clean_word == "bakit": new_sentence.append("bkit")
            elif clean_word == "wala": new_sentence.append("wla")
            else: new_sentence.append(word)
        else:
            new_sentence.append(word)
    return " ".join(new_sentence)

# --- 6. CORE LOGIC ---
def get_confusing_location(category):
    """
    Returns a location that might logically contradict the category 
    (e.g., a Traffic complaint at a Hospital) to prevent model overfitting.
    """
    if category == "traffic": loc_type = random.choice(["medical", "education", "religious", "commercial"])
    elif category == "health": loc_type = random.choice(["education", "commercial", "govt"])
    elif category == "sanitation": loc_type = random.choice(["medical", "religious", "govt"])
    elif category == "public_safety": loc_type = random.choice(["religious", "education", "generic"])
    else: loc_type = random.choice(list(landmark_db.keys()))
    return random.choice(landmark_db[loc_type])

def generate_text_for_category(category):
    """
    Generates the final text string.
    Uses 5 distinct structure templates to ensure variety.
    """
    base_issue = random.choice(seeds[category])
    
    # Context Injection (50% Specific Landmark, 50% Generic)
    if random.random() < 0.5: 
        raw_landmark = get_confusing_location(category)
    else: 
        raw_landmark = random.choice(landmark_db["generic"]) 
    
    # Language Mode Selection
    rand_val = random.random()
    if rand_val < 0.7: mode = "taglish"
    elif rand_val < 0.9: mode = "english"
    else: mode = "tagalog"

    processed_issue = apply_code_switch(base_issue, mode)
    
    # Preposition Logic
    if mode == "english":
        prep = random.choice(prepositions_en)
        loc_phrase = f"{prep} {raw_landmark}"
    else:
        prep = random.choice(prepositions_tl)
        loc_phrase = f"{prep} {raw_landmark}"

    # --- THE 5 SENTENCE STRUCTURES ---
    # 0 = Standard Formal: [Intro] + [Issue] + [Location] + [Closer]
    # 1 = Location Front-Loaded: [Location] + [Linker] + [Issue]
    # 2 = Conversational/Rant: [Issue] + [Location] + [Reaction]
    # 3 = Inquiry/Question: [Intro] + [Location] + [Issue]?
    # 4 = Minimalist/Panic: [Issue] + [Location]!!! (or just "dito")

    structure_type = random.choices([0, 1, 2, 3, 4], weights=[35, 20, 20, 10, 15], k=1)[0]
    
    text = ""
    
    if structure_type == 0:
        # Structure 1: Standard Formal
        intro = random.choice(intros) if random.random() < 0.6 else ""
        closer = random.choice(closers) if random.random() < 0.6 else ""
        text = f"{intro} {processed_issue} {loc_phrase} {closer}"
        
    elif structure_type == 1:
        # Structure 2: Location Front-Loaded
        # "Sa may Ateneo, may baha."
        conn = random.choice(connectors)
        text = f"{loc_phrase}, {conn} {processed_issue}."

    elif structure_type == 2:
        # Structure 3: Conversational/Rant
        # "Walang tubig sa Pacol, nakakainis!"
        reaction = random.choice(["nakakainis.", "grabe.", "hays.", "ano na?", "plss lang."])
        text = f"{processed_issue} {loc_phrase}, {reaction}"
        
    elif structure_type == 3:
        # Structure 4: Inquiry/Question
        # "Ask ko lang sa may UNC, may pasok ba?"
        intro = random.choice(["Ask ko lang", "Tanong lang", "May update ba", "Hello po"])
        text = f"{intro} {loc_phrase}, {processed_issue}?"

    elif structure_type == 4:
        # Structure 5: Minimalist/Panic
        # Either "SUNOG SA MAY PALENGKE!!!" or "Walang tubig dito."
        if random.random() < 0.5:
            text = f"{processed_issue} {loc_phrase}".upper() + "!!!"
        else:
            text = f"{processed_issue} dito."

    # Final cleanup and noise injection
    final_text = augment_text(text).strip()
    final_text = re.sub(' +', ' ', final_text) # Remove double spaces

    return final_text

def generate_random_timestamp(start, end):
    """Generates a random timestamp between start and end dates."""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def main():
    data = []
    print(f"Generating {TOTAL_ROWS} Real-World Weighted Timestamped Rows...")
    print(f"Time Range: {START_DATE} to {END_DATE}")
    
    categories = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())

    for _ in range(TOTAL_ROWS):
        # 1. Pick a category based on probability weights (Unbalanced)
        chosen_cat = random.choices(categories, weights=weights, k=1)[0]
        
        # 2. Generate text
        text = generate_text_for_category(chosen_cat)
        
        # 3. Generate Random Timestamp
        timestamp = generate_random_timestamp(START_DATE, END_DATE)
        
        data.append([timestamp, text, chosen_cat])

    # 4. Sort chronologically (Simulates a real log file)
    print("Sorting data chronologically...")
    data.sort(key=lambda x: x[0])

    # 5. Save
    print("Saving to CSV...")
    with open(OUTPUT_FILENAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "text", "category"])
        
        for row in data:
            # Format timestamp string here
            ts_str = row[0].strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([ts_str, row[1], row[2]])
            
    print(f"SUCCESS! Generated {len(data)} rows in {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()