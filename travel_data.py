"""
Static travel data — no network calls needed.
Used by ML models and UI pages throughout the app.
"""

import pandas as pd
import numpy as np

# ── Destination Master Data ────────────────────────────────────────────────────
DESTINATIONS = [
    # name, country, region, avg_cost_per_day, best_months, temp_avg,
    # beach, mountains, culture, adventure, nightlife, family, luxury,
    # solo, budget_friendly, safety_score, language, currency, visa_ease
    ("Bali", "Indonesia", "Asia", 55, "Apr-Oct", 28, 1,0,1,1,1,1,0,1,1, 7.5, "Indonesian", "IDR", 8),
    ("Paris", "France", "Europe", 180, "Apr-Jun", 15, 0,0,1,0,1,0,1,1,0, 8.0, "French", "EUR", 9),
    ("Tokyo", "Japan", "Asia", 120, "Mar-May", 16, 0,0,1,1,1,1,1,1,0, 9.5, "Japanese", "JPY", 7),
    ("New York", "USA", "Americas", 200, "Sep-Nov", 13, 0,0,1,0,1,1,1,1,0, 7.8, "English", "USD", 9),
    ("Bangkok", "Thailand", "Asia", 45, "Nov-Feb", 30, 0,0,1,1,1,1,0,1,1, 7.2, "Thai", "THB", 9),
    ("Rome", "Italy", "Europe", 150, "Apr-Jun", 18, 0,0,1,0,1,1,1,1,0, 7.5, "Italian", "EUR", 9),
    ("Sydney", "Australia", "Oceania", 160, "Sep-Nov", 22, 1,0,1,1,1,1,1,1,0, 9.0, "English", "AUD", 8),
    ("Dubai", "UAE", "Middle East", 200, "Nov-Mar", 25, 1,0,1,0,1,1,1,0,0, 9.2, "Arabic", "AED", 8),
    ("Santorini", "Greece", "Europe", 170, "Jun-Sep", 24, 1,0,1,0,1,0,1,1,0, 8.8, "Greek", "EUR", 9),
    ("Machu Picchu", "Peru", "Americas", 80, "May-Sep", 15, 0,1,1,1,0,1,0,1,1, 7.0, "Spanish", "PEN", 8),
    ("Maldives", "Maldives", "Asia", 400, "Nov-Apr", 29, 1,0,0,1,0,0,1,0,0, 9.0, "Dhivehi", "MVR", 8),
    ("Cape Town", "South Africa", "Africa", 90, "Nov-Mar", 21, 1,1,1,1,1,1,0,1,1, 6.5, "English", "ZAR", 8),
    ("Istanbul", "Turkey", "Europe/Asia", 70, "Apr-Jun", 17, 0,0,1,0,1,1,0,1,1, 7.0, "Turkish", "TRY", 9),
    ("Kyoto", "Japan", "Asia", 130, "Mar-May", 16, 0,0,1,0,0,1,1,1,0, 9.5, "Japanese", "JPY", 7),
    ("Barcelona", "Spain", "Europe", 145, "May-Sep", 22, 1,0,1,0,1,1,0,1,0, 7.8, "Spanish", "EUR", 9),
    ("Phuket", "Thailand", "Asia", 60, "Nov-Apr", 29, 1,0,1,1,1,1,0,1,1, 7.5, "Thai", "THB", 9),
    ("Prague", "Czech Republic", "Europe", 80, "May-Sep", 14, 0,0,1,0,1,1,0,1,1, 9.0, "Czech", "CZK", 9),
    ("Queenstown", "New Zealand", "Oceania", 140, "Dec-Feb", 16, 0,1,1,1,0,0,0,1,0, 9.2, "English", "NZD", 9),
    ("Marrakech", "Morocco", "Africa", 60, "Mar-May", 24, 0,1,1,1,0,1,0,1,1, 7.0, "Arabic", "MAD", 8),
    ("Singapore", "Singapore", "Asia", 150, "Feb-Apr", 30, 0,0,1,0,1,1,1,1,0, 9.5, "English", "SGD", 9),
    ("Amalfi Coast", "Italy", "Europe", 200, "May-Sep", 23, 1,0,1,0,0,0,1,1,0, 8.5, "Italian", "EUR", 9),
    ("Lisbon", "Portugal", "Europe", 100, "Apr-Jun", 18, 1,0,1,0,1,1,0,1,1, 8.8, "Portuguese", "EUR", 9),
    ("Petra", "Jordan", "Middle East", 75, "Mar-May", 22, 0,0,1,1,0,1,0,1,1, 8.5, "Arabic", "JOD", 8),
    ("Havana", "Cuba", "Americas", 65, "Nov-Apr", 26, 1,0,1,0,1,1,0,1,1, 7.8, "Spanish", "CUP", 6),
    ("Reykjavik", "Iceland", "Europe", 200, "Jun-Aug", 8, 0,0,1,1,0,0,0,1,0, 9.8, "Icelandic", "ISK", 9),
    ("Goa", "India", "Asia", 35, "Nov-Feb", 28, 1,0,1,1,1,1,0,1,1, 7.0, "Hindi", "INR", 9),
    ("Zanzibar", "Tanzania", "Africa", 80, "Jun-Oct", 27, 1,0,1,1,0,0,0,1,0, 7.2, "Swahili", "TZS", 7),
    ("Cusco", "Peru", "Americas", 60, "May-Sep", 12, 0,1,1,1,0,1,0,1,1, 7.5, "Spanish", "PEN", 8),
    ("Dubrovnik", "Croatia", "Europe", 130, "Jun-Sep", 22, 1,0,1,0,1,0,0,1,0, 9.0, "Croatian", "EUR", 9),
    ("Chiang Mai", "Thailand", "Asia", 40, "Nov-Feb", 25, 0,1,1,1,0,1,0,1,1, 8.5, "Thai", "THB", 9),
    ("Delhi", "India", "Asia", 40, "Oct-Mar", 25, 0,0,1,1,1,1,0,1,1, 7.5, "Hindi", "INR", 9),
    ("Mumbai", "India", "Asia", 50, "Nov-Feb", 30, 1,0,1,1,1,1,1,1,0, 7.0, "Hindi", "INR", 9),
    ("Jaipur", "India", "Asia", 35, "Oct-Mar", 28, 0,0,1,0,0,1,0,1,1, 8.0, "Hindi", "INR", 9),
    ("Manali", "India", "Asia", 30, "Mar-Jun", 15, 0,1,1,1,0,1,0,1,1, 8.5, "Hindi", "INR", 9),
    ("Rishikesh", "India", "Asia", 25, "Sep-Apr", 20, 0,1,1,1,0,1,0,1,1, 8.8, "Hindi", "INR", 9),
    ("Varanasi", "India", "Asia", 20, "Oct-Mar", 27, 0,0,1,0,0,1,0,1,1, 8.0, "Hindi", "INR", 9),
    ("Udaipur", "India", "Asia", 35, "Oct-Mar", 26, 0,0,1,0,0,1,1,1,0, 8.5, "Hindi", "INR", 9),
    ("Ladakh", "India", "Asia", 45, "May-Sep", 10, 0,1,1,1,0,0,0,1,0, 9.0, "Hindi", "INR", 8),
]

COLUMNS = [
    "destination","country","region","cost_per_day","best_months","avg_temp",
    "beach","mountains","culture","adventure","nightlife","family","luxury",
    "solo","budget_friendly","safety_score","language","currency","visa_ease"
]

def get_destinations_df() -> pd.DataFrame:
    df = pd.DataFrame(DESTINATIONS, columns=COLUMNS)
    return df

# ── Cost breakdown templates (% of daily budget) ──────────────────────────────
COST_BREAKDOWN = {
    "budget":     {"Accommodation":30,"Food":25,"Transport":20,"Activities":15,"Shopping":5,"Misc":5},
    "mid-range":  {"Accommodation":35,"Food":22,"Transport":18,"Activities":18,"Shopping":5,"Misc":2},
    "luxury":     {"Accommodation":40,"Food":20,"Transport":15,"Activities":20,"Shopping":4,"Misc":1},
}

# ── Month labels ───────────────────────────────────────────────────────────────
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# ── Weather templates ─────────────────────────────────────────────────────────
def get_weather_pattern(dest_name: str):
    """Return synthetic monthly temp & rain for a destination."""
    np.random.seed(sum(ord(c) for c in dest_name))  # reproducible per dest
    df = get_destinations_df()
    row = df[df["destination"] == dest_name]
    base_temp = float(row["avg_temp"].iloc[0]) if len(row) else 20

    temps, rain, crowd = [], [], []
    for m in range(12):
        variation = 8 * np.sin((m - 3) * np.pi / 6)
        temps.append(round(base_temp + variation + np.random.uniform(-2, 2), 1))
        rain.append(max(0, round(50 + 60 * np.sin((m - 6) * np.pi / 6) + np.random.uniform(-20, 20))))
        crowd.append(max(10, min(100, round(60 + 35 * np.sin((m - 6) * np.pi / 6) + np.random.uniform(-15, 15)))))

    return pd.DataFrame({"Month": MONTHS, "Temp_C": temps, "Rain_mm": rain, "Crowd_Index": crowd})

# ── Sample itinerary activities ───────────────────────────────────────────────
ACTIVITIES_DB = {
    "Bali":         ["Visit Tanah Lot Temple","Ubud Monkey Forest","Rice Terrace Trek","Cooking Class","Surf Lesson","Spa Day","Seminyak Beach"],
    "Paris":        ["Eiffel Tower","Louvre Museum","Seine River Cruise","Montmartre Walk","Wine Tasting","Versailles Day Trip","Musée d'Orsay"],
    "Tokyo":        ["Shibuya Crossing","Senso-ji Temple","Tsukiji Fish Market","TeamLab Borderless","Mount Fuji Day Trip","Akihabara Tech Walk","Harajuku"],
    "Bangkok":      ["Grand Palace","Chao Phraya River","Floating Market","Muay Thai Show","Street Food Tour","Chatuchak Weekend Market","Wat Arun"],
    "Rome":         ["Colosseum","Vatican Museums","Trevi Fountain","Roman Forum","Trastevere Stroll","Cooking Class","Borghese Gallery"],
    "Barcelona":    ["Sagrada Familia","Park Güell","Gothic Quarter Walk","La Boqueria Market","Flamenco Show","Barceloneta Beach","MNAC Museum"],
    "Dubai":        ["Burj Khalifa","Dubai Mall","Desert Safari","Gold Souk","Dubai Frame","Jumeirah Beach","Marina Dhow Cruise"],
    "Santorini":    ["Oia Sunset","Caldera Hike","Wine Tour","Akrotiri Ruins","Red Beach","Boat Trip","Fira to Oia Trek"],
    "default":      ["City Walking Tour","Local Food Tour","Museum Visit","Day Trip","Sunset Viewpoint","Shopping District","Cultural Performance"],
    "Delhi": ["Red Fort","India Gate","Lotus Temple","Chandni Chowk Food Tour","Qutub Minar"],
    "Mumbai": ["Marine Drive","Gateway of India","Juhu Beach","Local Street Food Tour","Elephanta Caves"],
    "Jaipur": ["Amber Fort","Hawa Mahal","City Palace","Local Bazaar Shopping","Desert Safari"],
    "Manali": ["Solang Valley","Rohtang Pass","River Rafting","Mall Road Walk","Snow Activities"],
    "Rishikesh": ["River Rafting","Laxman Jhula","Yoga Session","Ganga Aarti","Camping"],
    "Varanasi": ["Ganga Aarti","Boat Ride","Kashi Vishwanath Temple","Old City Walk","Street Food Tour"],
    "Udaipur": ["City Palace","Lake Pichola Boat Ride","Saheliyon Ki Bari","Sunset View","Local Market"],
    "Ladakh": ["Pangong Lake","Magnetic Hill","Nubra Valley","Bike Ride","Monastery Visit"],
}

def get_activities(dest: str, n: int = 5) -> list:
    pool = ACTIVITIES_DB.get(dest, ACTIVITIES_DB["default"])
    np.random.seed(sum(ord(c) for c in dest) + n)
    return list(np.random.choice(pool, size=min(n, len(pool)), replace=False))

# ── Popular travel tips ────────────────────────────────────────────────────────
TRAVEL_TIPS = {
    "Asia": ["Book accommodation in advance during peak season","Use local transport apps like Grab","Street food is safe and delicious","Dress modestly at religious sites","Learn a few local phrases"],
    "Europe": ["Get a rail pass for multi-city trips","Book museums in advance","Shoulder season (Apr-May, Sep-Oct) for fewer crowds","Validate train tickets before boarding","Free museum days often on first Sunday"],
    "Americas": ["Yellow fever vaccination may be required","Book Machu Picchu permits months ahead","US dollars widely accepted in South America","Travel insurance is essential","Altitude sickness — acclimatize slowly"],
    "Africa": ["Safari bookings fill up fast — book 6+ months early","Check visa requirements carefully","Travel vaccinations required for many countries","Malaria prophylaxis for some regions","Local guides greatly enhance experience"],
    "Middle East": ["Dress conservatively","Ramadan affects opening hours","Friday is the weekend in many countries","Haggling is expected in souks","Alcohol restrictions vary by country"],
    "Oceania": ["Book domestic flights early","Respect indigenous culture and sacred sites","Sun protection is essential","Wildlife is unique — do not disturb","Hire a car for flexibility"],
}
# ── Coordinates for Map (NEW ADDITION) ─────────────────────────

COORDINATES = {
    "Bali": (-8.3405, 115.0920),
    "Paris": (48.8566, 2.3522),
    "Tokyo": (35.6762, 139.6503),
    "New York": (40.7128, -74.0060),
    "Bangkok": (13.7563, 100.5018),
    "Rome": (41.9028, 12.4964),
    "Sydney": (-33.8688, 151.2093),
    "Dubai": (25.2048, 55.2708),
    "Santorini": (36.3932, 25.4615),
    "Maldives": (3.2028, 73.2207),
    "Cape Town": (-33.9249, 18.4241),
    "Istanbul": (41.0082, 28.9784),
    "Barcelona": (41.3851, 2.1734),
    "Singapore": (1.3521, 103.8198),

    # 🇮🇳 INDIA (important upgrade)
    "Goa": (15.2993, 74.1240),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Jaipur": (26.9124, 75.7873),
    "Manali": (32.2432, 77.1892)
}

def get_coordinates(destination):
    return COORDINATES.get(destination, (20.5937, 78.9629))  # default India
