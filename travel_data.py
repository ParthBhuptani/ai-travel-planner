"""
Static travel data — no network calls needed.
Used by ML models and UI pages throughout the app.
"""

import pandas as pd
import numpy as np

# ── Destination Master Data ───────────────────────────────────────────────
DESTINATIONS = [
    ("Bali","Indonesia","Asia",55,"Apr-Oct",28,1,0,1,1,1,1,0,1,1,7.5,"Indonesian","IDR",8),
    ("Paris","France","Europe",180,"Apr-Jun",15,0,0,1,0,1,0,1,1,0,8.0,"French","EUR",9),
    ("Tokyo","Japan","Asia",120,"Mar-May",16,0,0,1,1,1,1,1,1,0,9.5,"Japanese","JPY",7),
    ("New York","USA","Americas",200,"Sep-Nov",13,0,0,1,0,1,1,1,1,0,7.8,"English","USD",9),
    ("Bangkok","Thailand","Asia",45,"Nov-Feb",30,0,0,1,1,1,1,0,1,1,7.2,"Thai","THB",9),
    ("Rome","Italy","Europe",150,"Apr-Jun",18,0,0,1,0,1,1,1,1,0,7.5,"Italian","EUR",9),
    ("Dubai","UAE","Middle East",200,"Nov-Mar",25,1,0,1,0,1,1,1,0,0,9.2,"Arabic","AED",8),

    # 🇮🇳 INDIA CORE
    ("Delhi","India","Asia",40,"Oct-Mar",25,0,0,1,1,1,1,0,1,1,7.5,"Hindi","INR",9),
    ("Mumbai","India","Asia",50,"Nov-Feb",30,1,0,1,1,1,1,1,1,0,7.0,"Hindi","INR",9),
    ("Jaipur","India","Asia",35,"Oct-Mar",28,0,0,1,0,0,1,0,1,1,8.0,"Hindi","INR",9),
    ("Manali","India","Asia",30,"Mar-Jun",15,0,1,1,1,0,1,0,1,1,8.5,"Hindi","INR",9),
    ("Rishikesh","India","Asia",25,"Sep-Apr",20,0,1,1,1,0,1,0,1,1,8.8,"Hindi","INR",9),
    ("Varanasi","India","Asia",20,"Oct-Mar",27,0,0,1,0,0,1,0,1,1,8.0,"Hindi","INR",9),
    ("Udaipur","India","Asia",35,"Oct-Mar",26,0,0,1,0,0,1,1,1,0,8.5,"Hindi","INR",9),
    ("Ladakh","India","Asia",45,"May-Sep",10,0,1,1,1,0,0,0,1,0,9.0,"Hindi","INR",8),

    # 🇮🇳 SOUTH INDIA
    ("Kerala","India","Asia",40,"Sep-Mar",27,1,0,1,0,0,1,1,1,1,8.5,"Malayalam","INR",9),
    ("Munnar","India","Asia",30,"Sep-May",22,0,1,1,0,0,1,0,1,1,8.8,"Malayalam","INR",9),
    ("Ooty","India","Asia",35,"Oct-Jun",18,0,1,1,0,0,1,0,1,1,8.5,"Tamil","INR",9),
    ("Coorg","India","Asia",35,"Oct-Mar",20,0,1,1,1,0,1,0,1,1,8.7,"Kannada","INR",9),
    ("Hampi","India","Asia",30,"Oct-Feb",25,0,0,1,1,0,1,0,1,1,8.5,"Kannada","INR",9),
    ("Pondicherry","India","Asia",40,"Oct-Mar",28,1,0,1,0,0,1,1,1,1,8.2,"Tamil","INR",9),
    ("Andaman","India","Asia",60,"Nov-May",29,1,0,0,1,0,1,1,1,0,9.0,"Hindi","INR",9),
    ("Hyderabad","India","Asia",35,"Oct-Mar",28,0,0,1,0,1,1,0,1,1,8.0,"Telugu","INR",9),
    ("Bangalore","India","Asia",40,"Oct-Feb",24,0,0,1,0,1,1,0,1,1,8.5,"Kannada","INR",9),
    ("Chennai","India","Asia",45,"Nov-Feb",30,1,0,1,0,1,1,0,1,1,7.8,"Tamil","INR",9),
]

COLUMNS = [
    "destination","country","region","cost_per_day","best_months","avg_temp",
    "beach","mountains","culture","adventure","nightlife","family","luxury",
    "solo","budget_friendly","safety_score","language","currency","visa_ease"
]

def get_destinations_df():
    return pd.DataFrame(DESTINATIONS, columns=COLUMNS)

# ── ACTIVITIES ─────────────────────────────────────────────────────────────
ACTIVITIES_DB = {
    "Delhi": ["Red Fort","India Gate","Lotus Temple","Chandni Chowk","Qutub Minar"],
    "Mumbai": ["Marine Drive","Gateway of India","Juhu Beach","Street Food","Elephanta Caves"],
    "Jaipur": ["Amber Fort","Hawa Mahal","City Palace","Markets","Desert Safari"],
    "Manali": ["Solang Valley","Rohtang Pass","River Rafting","Mall Road","Snow Activities"],
    "Rishikesh": ["Rafting","Yoga","Ganga Aarti","Camping","Laxman Jhula"],
    "Varanasi": ["Ganga Aarti","Boat Ride","Temple Visit","Old City Walk","Street Food"],
    "Udaipur": ["City Palace","Lake Pichola","Boat Ride","Markets","Sunset"],
    "Ladakh": ["Pangong Lake","Nubra Valley","Bike Ride","Monasteries","Magnetic Hill"],

    "Kerala": ["Houseboat","Backwaters","Tea Gardens","Beach","Kathakali"],
    "Munnar": ["Tea Estates","Waterfalls","Viewpoints","Nature Walk","Parks"],
    "Ooty": ["Toy Train","Botanical Garden","Lake","Peak","Tea Factory"],
    "Coorg": ["Coffee Estates","Falls","Trekking","Viewpoints","Wildlife"],
    "Hampi": ["Temples","Ruins","Cycle Tour","River","Sunrise"],
    "Pondicherry": ["French Streets","Beach","Cafe","Auroville","Sunset"],
    "Andaman": ["Scuba","Snorkeling","Beach","Island Tour","Jail Visit"],
    "Hyderabad": ["Charminar","Fort","Biryani","Lake","Film City"],
    "Bangalore": ["Parks","Cafe","Nightlife","Tech Areas","Hills"],
    "Chennai": ["Beach","Temple","Mahabalipuram","Food","Shopping"],

    "default": ["City Tour","Food Tour","Museum","Shopping","Sunset"]
}

def get_activities(dest, n=5):
    pool = ACTIVITIES_DB.get(dest, ACTIVITIES_DB["default"])
    np.random.seed(sum(ord(c) for c in dest))
    return list(np.random.choice(pool, size=min(n, len(pool)), replace=False))

# ── DESCRIPTIONS (NEW 🔥) ─────────────────────────────────────────────────
DESCRIPTIONS = {
    "Delhi": "Capital city with rich history and monuments.",
    "Mumbai": "Financial capital with fast life and Bollywood.",
    "Jaipur": "Royal city with forts and palaces.",
    "Manali": "Hill station with snow and adventure.",
    "Rishikesh": "Yoga capital with rafting and spirituality.",
    "Varanasi": "Spiritual city on Ganga.",
    "Udaipur": "City of lakes and palaces.",
    "Ladakh": "Cold desert with stunning landscapes.",

    "Kerala": "Backwaters, greenery and beaches.",
    "Munnar": "Tea gardens and cool climate.",
    "Ooty": "Hill station with scenic beauty.",
    "Coorg": "Coffee plantations and nature.",
    "Hampi": "Ancient ruins and heritage.",
    "Pondicherry": "French-style coastal town.",
    "Andaman": "Island paradise with beaches.",
    "Hyderabad": "City of pearls and biryani.",
    "Bangalore": "Tech city with great weather.",
    "Chennai": "Cultural capital with beaches."
}

def get_description(dest):
    return DESCRIPTIONS.get(dest, "A beautiful destination.")

# ── COORDINATES (FIXED) ─────────────────────────────────────────────────
COORDINATES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Jaipur": (26.9124, 75.7873),
    "Manali": (32.2396, 77.1887),
    "Rishikesh": (30.0869, 78.2676),
    "Varanasi": (25.3176, 82.9739),
    "Udaipur": (24.5854, 73.7125),
    "Ladakh": (34.1526, 77.5770),
    "Goa": (15.2993, 74.1240),
    "Ahmedabad": (23.0225, 72.5714),

    "Kerala": (10.8505, 76.2711),
    "Munnar": (10.0889, 77.0595),
    "Ooty": (11.4064, 76.6932),
    "Coorg": (12.3375, 75.8069),
    "Hampi": (15.3350, 76.4600),
    "Pondicherry": (11.9416, 79.8083),
    "Andaman": (11.7401, 92.6586),
    "Hyderabad": (17.3850, 78.4867),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
}

def get_coordinates(dest):
    return COORDINATES.get(dest, (20.5937, 78.9629))
