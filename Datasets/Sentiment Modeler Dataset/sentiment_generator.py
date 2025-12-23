import pandas as pd
import random
import numpy as np

# ==========================================
# 1. CONFIGURATION & TUNING KNOBS
# ==========================================
OUTPUT_FILENAME = "peopulse_sentiment_dataset.csv"
NUM_ROWS = 1000            
NOISE_PROBABILITY = 0.30   
BICOL_NUANCE_PROB = 0.20   
INTENSITY_SIGMA = 0.15     

PROB_NEGATIVE = 0.45
PROB_POSITIVE = 0.45
# Remaining 0.10 is Neutral

# ==========================================
# 2. DATA ASSETS (VOCABULARY & TEMPLATES)
# ==========================================

# Mixed Barangays + Specific Landmarks found in Ground Truth
LOCATIONS = [
    "Triangulo", "Calauag", "Concepcion Pequeña", "Concepcion Grande", 
    "Balatas", "San Felipe", "Pacol", "Carolina", "Panicuason", 
    "Bagumbayan Sur", "Lerma", "Tinago", "Dayangdang", "Mabolo",
    "Sabang", "Tabuco", "Dinaga", "San Francisco", "Cararayan",
    "Plaza Rizal", "Plaza Quezon", "Centro", "Magsaysay", 
    "Panganiban Drive", "Diversion Road", "SM Naga", "Cathedral"
]

# Expanded Services including specific Utilities & Local Terms
SERVICES = [
    # General
    "garbage collection", "basura", "truck ng basura",
    "street lights", "ilaw sa poste", "madilim na kalsada",
    "drainage", "kanal", "baha",
    "road repairs", "lubak", "kalsada",
    # Specific Entities (High Intensity Targets)
    "CASURECO", "brownout", "kuryente", # Electricity
    "MNWD", "nawasa", "tubig", "water supply", # Water
    # Local Governance
    "Blue Boys", "traffic enforcer", "trapik",
    "Health Center", "checkup", "gamot", "bakuna",
    "City Hall", "Mayor's Permit", "business permit",
    "Trimobile", "tricycle driver", "pasahe",
    "scholarship", "financial assistance", "ayuda"
]

NEGATIVE_ADJECTIVES = [
    ("mabaho", 1.4), ("mabagal", 1.3), ("sira", 1.5), ("delikado", 1.8),
    ("walang kwenta", 1.9), ("hassle", 1.2), ("disappointing", 1.3),
    ("magulo", 1.1), ("baha", 1.7), ("maingay", 1.0), ("tambak", 1.4),
    ("pahirap", 1.6), ("palpak", 1.5), ("bulok", 1.7), ("useless", 1.8),
    ("bastos", 1.45), ("nangongotong", 1.8), ("kadiri", 1.5)
]

POSITIVE_ADJECTIVES = [
    ("maganda", 1.2), ("mabilis", 1.3), ("maayos", 1.1), 
    ("very helpful", 1.5), ("efficient", 1.4), ("excellent", 1.8),
    ("malinis", 1.2), ("friendly", 1.1), ("organized", 1.2),
    ("smooth", 1.1), ("world-class", 1.9), ("best", 1.5), ("reliable", 1.3),
    ("accommodating", 1.3), ("peaceful", 1.2), ("alerto", 1.5)
]

NEUTRAL_ADJECTIVES = [
    "current", "scheduled", "ongoing", "existing", "proposed", 
    "recent", "upcoming", "regular", "status of", "latest"
]

# --- TEMPLATES DERIVED FROM GROUND TRUTH ---
NEG_TEMPLATES = [
    # High Intensity / Urgent
    "HOY {serv} ANUNA?? {loc} NA NAMAN KAMI!!",
    "WALANG {serv} DITO SA {loc} 3 DAYS NA!!!",
    "{serv} PLEASE NAMAN MAAWA KAYO SA MGA TAO SA {loc}!",
    "GRABE {adj} DITO SA {loc} DELIKADO NA!",
    "WORST {serv} EVER SA {loc}!",
    # Standard Complaints
    "Sobrang {adj} na ng {serv} sa {loc} bakit di inaaksyunan?",
    "Garo wara man kwenta ang {serv} sa {loc}.",
    "Anyare sa {serv} sa {loc}? Ang {adj}.",
    "Paki-check man po ang {serv} sa {loc} {adj} baga.",
    "Late na naman ang {serv} sa {loc}, nakaka-{adj}.",
    "Nakakatakot dumaan sa {loc} pag gabi, {adj} ang {serv}.",
    "Bulok na sistema sa {serv}, ang gulo gulo sa {loc}.",
    "Di man lang nag-reply sa chat ang {serv}, {adj} service.",
    "Parang awa niyo na ayusin niyo na ang {serv} sa {loc}!!",
    "Nakakainis yung {serv} sa {loc}, {adj} masyado."
]

POS_TEMPLATES = [
    # Praise / Gratitude
    "Thank you Mayor Legacion sa mabilis na action sa {serv} sa {loc}!",
    "Mabilis ang process ng {serv} ngayon in fairness.",
    "Super helpful nung staff sa {serv} sa {loc} tnx po.",
    "Best LGU talaga ang Naga!! Proud Nagueño here sa {loc}!",
    "Okay man su service kang {serv} sa {loc}.",
    "Love the new {serv} sa {loc} ang ganda tignan.",
    "Very accommodating si {serv} sa {loc}, {adj}.",
    "Ang galing ng {serv} team alerto agad sa {loc}.",
    "Kudos to the {serv} for managing the {loc} well.",
    "Iyo man, {adj} ang programa sa {serv}.",
    "Thanks sa {serv} allowance laking tulong.",
    "Consistent ang {serv} sa {loc} good job.",
    "Wow ang bilis ng response time ng {serv} hotline!",
    "Solid ang support ng LGU sa {serv}.",
    "Proud to be Nagueño! {adj} ang {serv}."
]

NEU_TEMPLATES = [
    # Inquiries / Passive
    "Good morning po ask ko lang kung open ang {serv} sa {loc}?",
    "Sain po pwede magpa-register para sa {serv}?",
    "May schedule na ba ng {serv} sa {loc}?",
    "Wala bang pasok bukas sa {loc}?",
    "Ask lng po if may {serv} sa {loc}?",
    "Safe ba mag-jogging sa {loc} pag umaga?",
    "Waiting pa din sa {serv} update.",
    "Pwede po ba mag-request ng {serv} sa {loc}?",
    "Marhay na aga, may libreng {serv} po ba?",
    "Sain banda ang pila para sa {serv}?",
    "Ano na balita sa inaayos na {serv} sa {loc}?",
    "May bayad po ba mag-avail ng {serv}?",
    "Kamusta po ang lagay ng {serv} papuntang {loc}?",
    "Anong oras start ng {serv} sa {loc}?"
]

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def inject_bicolano_nuance(text):
    """
    Injects Naga-specific particles and vocabulary swaps based on 
    Ground Truth analysis.
    """
    words = text.split()
    new_words = []
    
    # Vocabulary Swaps (Tagalog -> Bicol/Naga Mix)
    swaps = {
        "saan": "sain",
        "ngayon": "ngunyan",
        "wala": "wara",
        "meron": "igwa",
        "ang": "su", # Context dependent, but adds flavor
        "bago": "ba'go",
        "hindi": "di",
        "kanina": "kaina"
    }
    
    # Particles to insert randomly
    particles = ["man", "baga", "daw", "po", "garo", "uni", "iyo"]

    for i, word in enumerate(words):
        clean_word = word.lower().strip(".,!?")
        
        # 1. Apply Swap if exists
        if clean_word in swaps:
            # Preserve case
            if word[0].isupper():
                word = swaps[clean_word].capitalize()
            else:
                word = swaps[clean_word]
        
        new_words.append(word)
        
        # 2. Random Particle Injection (Don't inject at very end or very start usually)
        if i > 0 and i < len(words) - 1:
            if random.random() < 0.15: # 15% chance after any word
                p = random.choice(particles)
                new_words.append(p)

    return " ".join(new_words)

def inject_noise(text):
    """
    Simulates realistic human typing patterns (Typos, Jejemon).
    """
    shortcuts = {
        "ako": "aq", "siya": "xa", "si": "c", "po": "p", 
        "mo": "m", "ko": "q", "dito": "d2", "niyo": "nyo",
        "bakit": "bkt", "mayor": "mayora", "please": "pls",
        "kalsada": "klsada", "barangay": "brgy", "kayo": "kau",
        "ano": "nu", "ngayon": "ngaun", "thanks": "tnx"
    }

    words = text.split()
    new_words = []

    for word in words:
        clean_word = word.lower().strip(".,!?")
        
        if clean_word in shortcuts and random.random() < 0.30:
            new_words.append(shortcuts[clean_word])
            continue

        new_chars = []
        for c in word:
            # Vowel Elongation
            if c.lower() in "aeiou" and random.random() < 0.05:
                new_chars.append(c * random.randint(2, 4))
                continue
            # Casing Swap
            if c.isalpha() and random.random() < 0.02:
                new_chars.append(c.swapcase())
                continue
            # Dropped Char
            if random.random() < 0.01:
                continue
            new_chars.append(c)
        
        new_words.append("".join(new_chars))

    return " ".join(new_words)


def generate_naga_feedback(num_rows, noise_prob):
    data = []

    for _ in range(num_rows):
        roll = random.random()
        loc = random.choice(LOCATIONS)
        serv = random.choice(SERVICES)
        
        jitter = np.random.normal(loc=0.0, scale=INTENSITY_SIGMA)
        current_intensity = 0.0

        # --- SENTIMENT LOGIC ---
        if roll < PROB_NEGATIVE:
            label = "negative"
            adj, base_score = random.choice(NEGATIVE_ADJECTIVES)
            template = random.choice(NEG_TEMPLATES)
            text_raw = template.format(adj=adj, serv=serv, loc=loc)
            
            current_intensity = base_score + jitter
            
            # --- UPDATED INTENSITY LOGIC (Based on Ground Truth) ---
            
            # 1. Critical Utilities Boost (CASURECO/MNWD/Water/Brownout = High Anger)
            critical_keywords = ["CASURECO", "brownout", "MNWD", "tubig", "water", "sunog"]
            if any(k in text_raw for k in critical_keywords):
                current_intensity += 0.35 # Significant boost
            
            # 2. Urgent Words Boost
            urgent_keywords = ["Mayor", "Emergency", "Attention", "Please", "delikado"]
            if any(k in text_raw for k in urgent_keywords):
                current_intensity += 0.15

            # 3. Shout Logic
            if current_intensity > 1.6:
                text_raw = text_raw.upper()
                current_intensity += 0.2
                
        elif roll < (PROB_NEGATIVE + PROB_POSITIVE):
            label = "positive"
            adj, base_score = random.choice(POSITIVE_ADJECTIVES)
            template = random.choice(POS_TEMPLATES)
            text_raw = template.format(adj=adj, serv=serv, loc=loc)
            
            current_intensity = base_score + jitter
            
            if any(x in text_raw for x in ["Mayor", "Salamat", "Thank", "Proud"]):
                current_intensity += 0.1
            
        else:
            label = "neutral"
            adj = random.choice(NEUTRAL_ADJECTIVES)
            template = random.choice(NEU_TEMPLATES)
            text_raw = template.format(adj=adj, serv=serv, loc=loc)
            current_intensity = abs(np.random.normal(0.25, 0.1)) # Slight bump for inquiries

        # --- LINGUISTIC INJECTION LAYERS ---
        
        # Layer 1: Bicolano Nuance (Apply before noise)
        if random.random() < BICOL_NUANCE_PROB:
            text_raw = inject_bicolano_nuance(text_raw)

        # Layer 2: Noise/Typos
        if random.random() < noise_prob:
            final_text = inject_noise(text_raw)
        else:
            final_text = text_raw
        
        # --- CLAMPING ---
        clamped_intensity = np.clip(current_intensity, 0.0, 2.0)
        final_intensity = round(clamped_intensity, 2)
        
        data.append([final_text, label, final_intensity])

    return pd.DataFrame(data, columns=["text", "label", "intensity"])


# ==========================================
# 4. MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    print(f"--- Peopulse 'Nagueño' Synthetic Data Generator ---")
    print(f"Generating {NUM_ROWS} rows...")
    
    # Generate Data
    df = generate_naga_feedback(NUM_ROWS, NOISE_PROBABILITY)
    
    # Save to CSV
    try:
        df.to_csv(OUTPUT_FILENAME, index=False)
        print(f"SUCCESS: Data saved to '{OUTPUT_FILENAME}'")
        print("-" * 30)
    except Exception as e:
        print(f"ERROR: Could not save file. {e}")