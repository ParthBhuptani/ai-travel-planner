import streamlit as st
import pickle
import pandas as pd
import math
import pydeck as pdk
from travel_data import get_destinations_df, get_activities, get_coordinates

# ===== CONFIG =====
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="wide")

# ===== CACHE =====
@st.cache_resource
def load_model():
    return pickle.load(open("travel_model.pkl", "rb"))

@st.cache_data
def load_data():
    return get_destinations_df()

model = load_model()
df = load_data()

# ===== DISTANCE FUNCTION =====
def get_distance_time(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    time = distance / 60

    return int(distance), round(time, 1)

# ===== HEADER =====
st.markdown("<h1 style='text-align:center;'>🌍 AI Travel Planner</h1>", unsafe_allow_html=True)

# ===== REGION FILTER =====
region = st.selectbox("🌍 Choose Region", ["All", "India", "International"])

if region == "India":
    df_filtered = df[df["country"] == "India"]
elif region == "International":
    df_filtered = df[df["country"] != "India"]
else:
    df_filtered = df

destinations = df_filtered["destination"].tolist()

# ===== INPUT =====
start_city = st.text_input("📍 Starting City")
stops = st.multiselect("🛑 Stops", destinations)
end_city = st.selectbox("🏁 Final Destination", destinations)

col1, col2 = st.columns(2)
with col1:
    days = st.number_input("📅 Days", min_value=1)
with col2:
    budget = st.number_input("💰 Budget", min_value=1000)

# ===== BUTTON =====
if st.button("🚀 Generate Travel Plan"):

    # ===== ROUTE =====
    route = []
    if start_city:
        route.append(start_city)
    route.extend(stops)
    route.append(end_city)

    city_data = []

    for city in route:
        if city in df["destination"].values:
            data = df[df["destination"] == city].iloc[0]
            acts = get_activities(city, 5)

            city_data.append({
                "name": city,
                "data": data,
                "activities": acts
            })

    tab1, tab2, tab3 = st.tabs(["Overview", "Activities", "Itinerary"])

    # ===== TAB 1 =====
    with tab1:

        col1, col2 = st.columns([1, 1])

        # ===== LEFT SIDE =====
        with col1:
            st.markdown("### 🧭 Route Details")

            for i in range(len(route)-1):
                lat1, lon1 = get_coordinates(route[i])
                lat2, lon2 = get_coordinates(route[i+1])

                dist, time = get_distance_time(lat1, lon1, lat2, lon2)
                st.markdown(f"""
                    <div style="
                    padding:10px;
                    margin-bottom:8px;
                    border-radius:8px;
                    background-color:#1e293b;">
                    <b>📍 {route[i]} → {route[i+1]}</b><br>
                    Distance: {dist} km<br>
                    Time: ~{time} hrs
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("### 💰 Budget Distribution")

            budget_data = []

            for idx, city in enumerate(city_data):
                city_days = days // len(city_data) + (1 if idx < (days % len(city_data)) else 0)
                city_budget = int((city_days / days) * budget)

                budget_data.append({
                    "City": city["name"],
                    "Days": city_days,
                    "Budget (₹)": city_budget
                })

            df_budget = pd.DataFrame(budget_data)

            st.dataframe(df_budget, use_container_width=True)

        # ===== RIGHT SIDE (MAP) =====
        with col2:

            coords = []
            for city in route:
                lat, lon = get_coordinates(city)
                coords.append([lon, lat])

            layer = pdk.Layer(
                "PathLayer",
                data=[{"path": coords}],
                get_path="path",
                get_color=[255, 0, 0],
                width_min_pixels=3
            )

            # ✅ FIXED FOCUS (NO RESET)
            if "focus_city" not in st.session_state:
                st.session_state.focus_city = route[0]

            selected = st.selectbox(
                "🔍 Focus Location",
                route,
                index=route.index(st.session_state.focus_city)
            )

            st.session_state.focus_city = selected

            lat, lon = get_coordinates(st.session_state.focus_city)

            view_state = pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=7
            )

            st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    # ===== TAB 2 =====
    with tab2:
        for city in city_data:
            st.markdown(f"### {city['name']}")
            for act in city["activities"]:
                st.write(f"• {act}")

    # ===== TAB 3 =====
    with tab3:
        st.markdown("### 📅 Itinerary")

        days_per_city = days // len(city_data)
        extra_days = days % len(city_data)

        day_count = 1

        for idx, city in enumerate(city_data):

            city_days = days_per_city + (1 if idx < extra_days else 0)

            st.markdown(f"### {city['name']} ({city_days} days)")

            for i in range(city_days):

                if i < len(city["activities"]):
                    text = city["activities"][i]
                else:
                    text = "Explore local places"

                st.write(f"Day {day_count}: {text}")
                day_count += 1

            if idx < len(city_data) - 1:
                st.write("🚗 Travel to next destination")
                day_count += 1

# ===== FOOTER =====
st.markdown("---")
st.markdown("<center>🚀 Built by Parth</center>", unsafe_allow_html=True)
