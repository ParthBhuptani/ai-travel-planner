import streamlit as st
import pickle
import random
from travel_data import get_destinations_df, get_activities

# ===== CONFIG =====
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ===== CACHE =====
@st.cache_resource
def load_model():
    return pickle.load(open("travel_model.pkl", "rb"))

@st.cache_data
def load_data():
    return get_destinations_df()

model = load_model()
df = load_data()
destinations = df["destination"].tolist()

# ===== CUSTOM CSS =====
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #0f172a, #1e293b);
}
.card {
    padding:20px;
    border-radius:12px;
    background: linear-gradient(135deg,#1f3b4d,#2563eb);
    color:white;
    margin-bottom:15px;
}
.box {
    padding:10px;
    margin:6px 0;
    border-radius:8px;
    background-color:#1e293b;
}
.itinerary {
    padding:12px;
    margin:8px 0;
    border-radius:8px;
    background-color:#0f172a;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("""
<h1 style='text-align:center;'>🌍 AI Travel Planner</h1>
<p style='text-align:center;'>Plan smart trips with AI recommendations</p>
""", unsafe_allow_html=True)

st.markdown("### 🌍 Discover smart travel planning with AI")
st.markdown("---")

# ===== INPUT =====
st.markdown("### 🧾 Enter Trip Details")

col1, col2 = st.columns(2)

with col1:
    place = st.selectbox("🌍 Select Destination", destinations)

with col2:
    season = st.selectbox("🌤 Season", ["Summer", "Winter", "Monsoon"])

budget = st.number_input("💰 Budget (₹)", min_value=1000)
days = st.number_input("📅 Days", min_value=1)

season_map = {"Summer": 0, "Winter": 1, "Monsoon": 2}
season_value = season_map[season]

st.markdown("---")

# ===== BUTTON =====
if st.button("🚀 Generate Travel Plan"):

    with st.spinner("Generating your travel plan..."):
        prediction = model.predict([[budget, days, season_value]])

    data = df[df["destination"] == place].iloc[0]

    # ===== SMART TRAVEL STYLE =====
    score = {
        "beach": data["beach"],
        "mountains": data["mountains"],
        "culture": data["culture"],
        "adventure": data["adventure"],
        "luxury": data["luxury"]
    }

    best_type = max(score, key=score.get)

    if best_type == "beach":
        category = "🏖️ Beach & Relaxation"
    elif best_type == "mountains":
        category = "🏔️ Adventure & Nature"
    elif best_type == "culture":
        category = "🏛️ Cultural Exploration"
    elif best_type == "adventure":
        category = "🧗 Adventure Travel"
    elif best_type == "luxury":
        category = "💎 Luxury Travel"
    else:
        category = "🌍 General Travel"

    # ===== COST CALCULATION =====
    est_total = data['cost_per_day'] * days

    # ===== RESULT CARD =====
    st.markdown(f"""
    <div class="card">
    <h3>🌍 {place}, {data['country']}</h3>
    <p><b>🎯 Travel Style:</b> {category}</p>
    <p>💰 Avg Cost/Day: ${data['cost_per_day']}</p>
    <p>📊 Estimated Trip Cost: ${est_total}</p>
    <p>📅 Best Months: {data['best_months']}</p>
    <p>🛡️ Safety: {data['safety_score']}/10</p>
    </div>
    """, unsafe_allow_html=True)

    # ===== ACTIVITIES =====
    st.markdown("### ✨ Suggested Activities")

    activities = get_activities(place, 7)

    for act in activities:
        st.markdown(f'<div class="box">• {act}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ===== DYNAMIC BUDGET =====
    st.markdown("### 💰 Budget Breakdown")

    stay = int(budget * random.uniform(0.35, 0.45))
    food_cost = int(budget * random.uniform(0.25, 0.35))
    travel_cost = budget - (stay + food_cost)

    colA, colB, colC = st.columns(3)
    colA.metric("Stay", f"₹{stay}")
    colB.metric("Food", f"₹{food_cost}")
    colC.metric("Travel", f"₹{travel_cost}")

    st.markdown("---")

    # ===== ITINERARY =====
    st.markdown("### 📅 Suggested Itinerary")

    extra_ideas = [
        "Explore local markets",
        "Try famous local food",
        "Relax at scenic spots",
        "Visit hidden gems",
        "Enjoy cultural shows"
    ]

    for day in range(1, days + 1):

        if day <= len(activities):
            text = activities[day-1]
        else:
            text = extra_ideas[(day - len(activities) - 1) % len(extra_ideas)]

        st.markdown(f"""
        <div class="itinerary">
        <b>Day {day}</b>: {text}
        </div>
        """, unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("---")
st.markdown("<center>🚀 Built by Parth | AI Travel Planner</center>", unsafe_allow_html=True)