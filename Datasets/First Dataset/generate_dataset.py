import csv
import random

# --- CONFIGURATION ---
TARGET_COUNT_PER_CATEGORY = 200
OUTPUT_FILENAME = "populse_dataset.csv"

# --- 1. CONTEXTUAL DATA (Naga City) ---
locations = [
    "Abella", "Bagumbayan", "Balatas", "Calauag", "Cararayan", "Carolina", 
    "Concepcion Grande", "Concepcion Pequeña", "Dayangdang", "Del Rosario", 
    "Dinaga", "Igualdad", "Lerma", "Liboton", "Mabolo", "Pacol", "Panicuason", 
    "Peñafrancia", "Sabang", "San Felipe", "San Francisco", "San Isidro", 
    "Santa Cruz", "Tabuco", "Tinago", "Triangulo", 
    # Landmarks
    "Magsaysay Avenue", "Centro", "Plaza Quince", "Panganiban Drive", 
    "SM Naga area", "UNC gate", "Metropolitan Cathedral", "Ateneo Avenue", 
    "Diversion Road", "LCC Mall", "Naga City People's Mall", "Plaza Rizal", 
    "Bicol Central Station", "Jesse Robredo Coliseum", "Ecology Park"
]

# --- 2. EXTENSIVE SEED DATABASE (Grammatically structured phrases) ---
# Each list contains unique ways to describe the problem for that category.

seeds = {
    "health": [
        "tumataas ang cases ng dengue", "maraming bata ang nilalagnat", 
        "walang doctor sa health center", "ubos na ang gamot sa center", 
        "need namin ng schedule for anti-rabies", "masungit ang nurse sa clinic", 
        "flu outbreak sa area namin", "requesting ambulance assistance", 
        "daming lamok, need fumigation", "walang available na covid vaccine", 
        "high blood pressure monitoring request", "stray dogs chasing people", 
        "malnourished children feeding program", "tuberculosis medication out of stock",
        "medical certificate request for indigent", "schedule ng tuli operation",
        "diarrhea outbreak due to dirty water", "need oxygen tank assistance"
    ],
    "sanitation": [
        "sobrang baho ng kanal", "tambak na basura sa kalsada", 
        "may patay na daga sa daan", "marumi ang tubig na lumalabas sa gripo", 
        "ipis infestation sa public market", "amoy imbornal ang paligid", 
        "dumi ng aso sa sidewalk", "clogged drainage causing smell", 
        "mabaho ang poultry sa residential area", "unsanitary street food vendors", 
        "public toilet walang tubig at madumi", "estero needs cleaning", 
        "basura nakatambak sa harap ng school", "nagkalat na used face masks", 
        "puno na ang septic tank", "pest control request for barangay hall"
    ],
    "infrastructure": [
        "ang lalim ng lubak sa daan", "sira ang tulay, delikado", 
        "nakatagilid na ang poste", "unfinished road works causing traffic", 
        "bitak-bitak na ang pader", "busted ang street lights, madilim", 
        "walang sidewalk na madaanan", "falling debris from construction", 
        "road widening project delay", "sira ang bubong ng waiting shed", 
        "basketball court needs renovation", "slippery pathway due to moss", 
        "cctv camera not working", "drainage cover is missing", 
        "collapsed riprap sa ilog", "defective solar lights", 
        "barangay hall renovation request"
    ],
    "employment": [
        "delayed ang sweldo ng workers", "unfair labor practice sa trabaho", 
        "looking for summer job for students", "naghahanap ng trabaho", 
        "discrimination sa hiring process", "walang benefits na binibigay", 
        "contractualization issue", "kailan ang next job fair", 
        "inquiry for DOLE TUPAD program", "unpaid overtime pay", 
        "illegal dismissal complaint", "hiring ba ng security guard", 
        "openings for construction workers", "tesda training schedule inquiry", 
        "livelihood program for mothers", "cash for work payout delay", 
        "employer not paying SSS contribution"
    ],
    "public_safety": [
        "may nag-aaway na lasing", "may magnanakaw na umaaligid", 
        "suspicious drug related activity", "sobrang dilim ng eskinita", 
        "akyat bahay incident report", "riot ng mga kabataan kagabi", 
        "snatching incident sa kanto", "suspicious person taking photos", 
        "sobrang ingay ng videoke", "curfew violation ng mga minor", 
        "inom sa kalsada hanggang madaling araw", "drag racing ng motor sa gabi", 
        "vandalism sa pader ng school", "gang war threat", 
        "requesting police visibility", "tanod sleeping on duty", 
        "bato-bato sa sasakyan incidents"
    ],
    "utilities": [
        "walang tubig simula kanina", "brownout nanaman dito", 
        "sobrang hina ng signal", "may putol na kable sa daan", 
        "fluctuating ang kuryente", "nawalan ng internet connection", 
        "water pipe leak sa kalsada", "sumabog ang transformer", 
        "shocking electricity bill amount", "illegal jumper connection report", 
        "dirty water supply form faucet", "unannounced water interruption", 
        "dead spot area for globe/smart", "meter reading error complaint", 
        "sparking wires sa poste", "low water pressure tuwing umaga", 
        "street light flickering on and off"
    ],
    "waste_management": [
        "hindi dumaan ang garbage truck", "nagsusunog ng plastic ang kapitbahay", 
        "pagtapon ng basura sa ilog", "illegal dumping site sa vacant lot", 
        "walang segregation policy", "kalat ang basura sa park", 
        "kailan ang schedule ng hakot", "basura bumabara sa drainage", 
        "bulky waste pickup request", "recycling inquiry", 
        "walang garbage collector personnel", "di hinahakot ang nabubulok", 
        "basurahan sa plaza puno na", "penalty for littering inquiry", 
        "composting facility foul odor"
    ],
    "traffic": [
        "grabe ang traffic ngayon", "illegal parking sa kalsada", 
        "counter-flow na tricycle", "sira ang traffic light", 
        "road obstruction by vendors", "no entry violation reports", 
        "tricycle overcharging fare", "congested intersection always", 
        "jeepney cutting trip violation", "colorum vehicles operating", 
        "faded pedestrian lane markings", "loading/unloading violation", 
        "truck ban inquiry time", "traffic enforcer nangongotong", 
        "double parking sa main road", "traffic rerouting confusion", 
        "road rage incident report"
    ],
    "social_services": [
        "wala pa kaming natatanggap na ayuda", "status of scholarship application", 
        "senior citizen pension delay", "paano kumuha ng pwd id", 
        "kulang ang binigay na relief goods", "burial assistance request", 
        "4ps beneficiary inquiry", "solo parent benefits inquiry", 
        "medical assistance for indigent", "birthday cash gift for senior", 
        "feeding program request for kids", "vawc desk assistance needed", 
        "child abuse report", "lost id replacement process", 
        "financial aid for poor students", "calamity loan inquiry", 
        "social pension payout schedule"
    ]
}

# --- 3. PERSONA TEMPLATE ENGINE (The Diversity Core) ---

def generate_row(category):
    # 1. Pick a seed phrase (The Core Issue)
    issue = random.choice(seeds[category])
    
    # 2. Pick a location
    loc = random.choice(locations)
    
    # 3. Choose a Persona/Style
    style = random.choice(["formal", "netizen", "sms", "concerned"])
    
    text = ""
    
    if style == "formal":
        # Polite, complete sentences. Good grammar.
        templates = [
            f"I would like to report that {issue} in {loc}.",
            f"Good day. We are requesting assistance because {issue} at {loc}.",
            f"Formal complaint: {issue} located in {loc}.",
            f"Please be informed that {issue} in the vicinity of {loc}.",
            f"To the City Government: {issue} here in {loc}. Please investigate.",
            f"Reporting a concern regarding {issue} at {loc}.",
        ]
        text = random.choice(templates)

    elif style == "netizen":
        # Emotional, Taglish, Ranty, "Conio" mix.
        templates = [
            f"Grabe naman, {issue} dito sa {loc}! Ano na??",
            f"Huy pansinin niyo naman to. {issue} sa {loc}. Nakaka-stress!",
            f"Shoutout sa LGU, {issue} sa {loc}. Please actionan agad.",
            f"Jusko, {issue} nanaman sa {loc}. Ilang araw na to.",
            f"Anyone from city hall? {issue} here in {loc}. So hassle.",
            f"Pwede ba mag-reklamo? {issue} kasi sa {loc}. Thanks.",
            f"Parang wala namang action. {issue} pa rin sa {loc}.",
        ]
        text = random.choice(templates)

    elif style == "sms":
        # Abbreviated, direct, lowercase, minimal punctuation.
        templates = [
            f"Report ko lng {issue} d2 s {loc}.",
            f"Help. {issue} sa {loc}. Pls fix.",
            f"Gud pm. {issue} sa {loc}. Tnx.",
            f"Urgent: {issue} d2 sa {loc}.",
            f"Update po sa {issue} sa {loc}? Wala pa action.",
            f"Fyi {issue} sa {loc}.",
            f"Concern lang re: {issue} sa {loc}.",
        ]
        text = random.choice(templates)
        # Apply SMS slang cleaning
        text = text.replace("ang", "ng").replace("sa", "s").replace("dito", "d2")

    elif style == "concerned":
        # Narrative, neighborly tone, explanatory.
        templates = [
            f"Ask ko lang po kung may action na, {issue} kasi dito sa {loc}.",
            f"Concerned lang po kami sa mga bata, {issue} dito sa {loc}.",
            f"Kami po ay taga {loc}, report ko lang na {issue}.",
            f"Sir/Ma'am, pa-check naman po ng {loc}, {issue} po kasi.",
            f"Magtatanong lang po regarding {issue} sa {loc}?",
            f"Kailan po kaya maayos ang {loc}? {issue} po kasi.",
        ]
        text = random.choice(templates)

    # 4. Final Polish: Random Typo/Casing Injection for Realism
    # 5% chance to be ALL CAPS (Angry)
    if random.random() < 0.05:
        text = text.upper()
    
    # 5% chance to be all lowercase (Lazy)
    elif random.random() < 0.05:
        text = text.lower()

    return [text, category]

def main():
    data = []
    print("Generating POLISHED & EXPANDED dataset...")
    
    # Generate balanced data
    for category in seeds.keys():
        for _ in range(TARGET_COUNT_PER_CATEGORY):
            data.append(generate_row(category))
            
    # Shuffle to simulate real intake
    random.shuffle(data)
    
    with open(OUTPUT_FILENAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["text", "category"])
        writer.writerows(data)
        
    print(f"DONE! Generated {len(data)} rows in {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()