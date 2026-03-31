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

# ===== HERO SECTION =====
st.markdown("""
<h1 style='text-align:center;'>🌍 AI Travel Planner</h1>
<p style='text-align:center; font-size:18px;'>Plan smart multi-city trips with AI ✈️</p>
""", unsafe_allow_html=True)

st.markdown("---")

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
st.markdown("### 🧾 Enter Trip Details")

start_city = st.text_input("📍 Starting City")
stops = st.multiselect("🛑 Stops", destinations)
end_city = st.selectbox("🏁 Final Destination", destinations)

col1, col2 = st.columns(2)
with col1:
    days = st.number_input("📅 Days", min_value=1)
with col2:
    budget = st.number_input("💰 Budget", min_value=1000)

st.markdown("---")

# ===== BUTTON =====
if st.button("🚀 Generate Travel Plan"):

    # ✅ EMPTY CHECK
    if not start_city or not end_city:
        st.warning("Please enter start and end city")
        st.stop()

    route = []
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

    # ===== TRIP SUMMARY =====
    total_distance = 0
    for i in range(len(route)-1):
        lat1, lon1 = get_coordinates(route[i])
        lat2, lon2 = get_coordinates(route[i+1])
        dist, _ = get_distance_time(lat1, lon1, lat2, lon2)
        total_distance += dist

    st.markdown("### 📊 Trip Summary")
    colA, colB, colC = st.columns(3)
    colA.metric("Total Cities", len(city_data))  # ✅ updated label
    colB.metric("Total Distance", f"{total_distance} km")
    colC.metric("Budget", f"₹{budget}")

    tab1, tab2, tab3 = st.tabs(["Overview", "Activities", "Itinerary"])

    # ===== TAB 1 =====
    with tab1:

        col1, col2 = st.columns([1, 1])

        # ===== LEFT =====
        with col1:
            st.markdown("### 🧭 Route Details")

            for i in range(len(route)-1):
                lat1, lon1 = get_coordinates(route[i])
                lat2, lon2 = get_coordinates(route[i+1])

                dist, time = get_distance_time(lat1, lon1, lat2, lon2)

                st.markdown(f"""
                <div style="padding:12px;margin-bottom:10px;border-radius:10px;background-color:#1e293b;">
                <b>📍 {i+1}. {route[i]} → {i+2}. {route[i+1]}</b>
                <br>🚗 {dist} km &nbsp;&nbsp; ⏱ {time} hrs
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

            st.dataframe(pd.DataFrame(budget_data), use_container_width=True)

        # ===== RIGHT (MAP IMPROVED) =====
        with col2:

            st.markdown("### 🗺️ Travel Map")

            coords = []
            for city in route:
                lat, lon = get_coordinates(city)
                coords.append([lon, lat])

            avg_lat = sum([c[1] for c in coords]) / len(coords)
            avg_lon = sum([c[0] for c in coords]) / len(coords)

            # ROUTE LINE
            line_layer = pdk.Layer(
                "PathLayer",
                data=[{"path": coords}],
                get_path="path",
                get_color=[255, 80, 80],
                width_min_pixels=3
            )

            # ✅ COLORED POINTS (NEW)
            scatter_data = []
            for idx, coord in enumerate(coords):
                if idx == 0:
                    color = [0, 255, 0]   # start
                elif idx == len(coords)-1:
                    color = [255, 0, 0]   # end
                else:
                    color = [0, 200, 255] # stops

                scatter_data.append({
                    "position": coord,
                    "color": color
                })

            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=scatter_data,
                get_position="position",
                get_color="color",
                get_radius=15000
            )

            view_state = pdk.ViewState(
                latitude=avg_lat,
                longitude=avg_lon,
                zoom=4.5
            )

            st.pydeck_chart(pdk.Deck(
                layers=[line_layer, scatter_layer],
                initial_view_state=view_state
            ))

    # ===== TAB 2 =====
    with tab2:
        st.markdown("### ✨ Suggested Activities")

        for city in city_data:
            st.markdown(f"#### 📍 {city['name']}")
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

            # ✅ bigger heading
            st.markdown(f"## 📍 {city['name']} ({city_days} days)")

            for i in range(city_days):

                if i < len(city["activities"]):
                    text = city["activities"][i]
                else:
                    text = "Explore local places"

                st.markdown(f"**Day {day_count}:** {text}")
                day_count += 1

            if idx < len(city_data) - 1:
                st.markdown("🚗 Travel to next destination")

# ===== FOOTER =====
st.markdown("---")
st.markdown("<center>🚀 Built by Parth</center>", unsafe_allow_html=True)
