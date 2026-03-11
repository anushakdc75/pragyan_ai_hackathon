import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import requests
import shap
import folium
from streamlit_folium import st_folium
from prophet import Prophet

st.set_page_config(page_title="Smart AQI Platform", layout="wide")

# ---------------- ULTRA UI ---------------- #

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
font-family: 'Segoe UI', sans-serif;
}

.hero{
background: linear-gradient(135deg,#4CAF50,#2e7d32);
padding:40px;
border-radius:25px;
text-align:center;
font-size:50px;
font-weight:700;
box-shadow:0px 20px 50px rgba(0,0,0,0.4);
}

.glass{
background: rgba(255,255,255,0.08);
padding:20px;
border-radius:15px;
backdrop-filter: blur(12px);
box-shadow:0px 10px 30px rgba(0,0,0,0.4);
text-align:center;
font-size:20px;
}

.scale{
display:flex;
margin-top:25px;
border-radius:10px;
overflow:hidden;
}

.scale div{
flex:1;
padding:10px;
text-align:center;
color:white;
font-size:13px;
}

.good{background:#4CAF50}
.mod{background:#cddc39}
.poor{background:#ff9800}
.unhealthy{background:#f44336}
.severe{background:#9c27b0}
.hazard{background:#880e4f}

section[data-testid="stSidebar"]{
background:#0b0d12;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

model = joblib.load("aqi_model.pkl")
encoder = joblib.load("city_encoder.pkl")
df = pd.read_csv("city_day.csv")

API_KEY = "f6e06198b71124066ce034ab38f13f8b3a219b85"

# ---------------- FUNCTIONS ---------------- #

def get_live_pollution(city):

    city = city.lower()

    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

    r = requests.get(url)
    data = r.json()

    if data["status"] != "ok":
        return None

    iaqi = data["data"]["iaqi"]

    def safe(key):
        return iaqi[key]["v"] if key in iaqi else 0

    return {
        "pm25": safe("pm25"),
        "pm10": safe("pm10"),
        "no2": safe("no2"),
        "co": safe("co"),
        "o3": safe("o3"),
        "aqi": data["data"]["aqi"]
    }

def aqi_category(aqi):

    if aqi<=50:
        return "Good 🟢"
    elif aqi<=100:
        return "Moderate 🟡"
    elif aqi<=200:
        return "Poor 🟠"
    elif aqi<=300:
        return "Unhealthy 🔴"
    else:
        return "Hazardous ⚫"

# ---------------- TITLE ---------------- #

st.title("🌍 Smart Air Quality Intelligence Platform")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Live AQI",
        "Pollution Dashboard",
        "City Comparison",
        "Future AQI Forecast",
        "Explainable AI",
        "Pollution Map"
    ]
)

# ---------------- LIVE AQI ---------------- #

if menu == "Live AQI":

    city = st.selectbox("Select City", df["City"].unique())

    if st.button("Fetch Live AQI"):

        pollution = get_live_pollution(city)

        if pollution is None:
            st.error("API failed")
        else:

            city_encoded = encoder.transform([city])[0]

            data = [[
                city_encoded,
                pollution["pm25"],
                pollution["pm10"],
                0,
                pollution["no2"],
                0,
                0,
                pollution["co"],
                0,
                pollution["o3"],
                0,
                0,
                0,
                1,1,1
            ]]

            prediction = model.predict(data)[0]

            category = aqi_category(prediction)

            st.markdown(
            f"""
            <div class="hero">
            AQI {round(prediction,0)} <br>
            {category}
            </div>
            """,
            unsafe_allow_html=True
            )

            st.markdown("""
            <div class="scale">
            <div class="good">Good<br>0-50</div>
            <div class="mod">Moderate<br>51-100</div>
            <div class="poor">Poor<br>101-150</div>
            <div class="unhealthy">Unhealthy<br>151-200</div>
            <div class="severe">Severe<br>201-300</div>
            <div class="hazard">Hazardous<br>300+</div>
            </div>
            """, unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction,
                title={'text': "AQI Gauge"},
                gauge={'axis': {'range':[0,500]}}
            ))

            st.plotly_chart(fig,use_container_width=True)

            col1,col2,col3 = st.columns(3)

            col1.markdown(f"<div class='glass'>PM2.5<br>{pollution['pm25']}</div>",unsafe_allow_html=True)
            col2.markdown(f"<div class='glass'>PM10<br>{pollution['pm10']}</div>",unsafe_allow_html=True)
            col3.markdown(f"<div class='glass'>NO2<br>{pollution['no2']}</div>",unsafe_allow_html=True)

# ---------------- DASHBOARD ---------------- #

elif menu == "Pollution Dashboard":

    city = st.selectbox("City", df["City"].unique())

    city_df = df[df["City"]==city]

    col1,col2 = st.columns(2)

    fig1 = px.line(city_df,x="Date",y="AQI")

    fig2 = px.scatter(city_df,x="PM2.5",y="AQI")

    col1.plotly_chart(fig1,use_container_width=True)
    col2.plotly_chart(fig2,use_container_width=True)

# ---------------- CITY COMPARISON ---------------- #

elif menu == "City Comparison":

    cities = st.multiselect(
        "Select Cities",
        df["City"].unique(),
        default=df["City"].unique()[:3]
    )

    compare_df = df[df["City"].isin(cities)]

    fig = px.line(compare_df,x="Date",y="AQI",color="City")

    st.plotly_chart(fig,use_container_width=True)

# ---------------- FORECAST ---------------- #

elif menu == "Future AQI Forecast":

    city = st.selectbox("City", df["City"].unique())

    city_df = df[df["City"]==city]

    forecast_df = city_df[["Date","AQI"]]

    forecast_df.columns=["ds","y"]

    prophet_model = Prophet()

    prophet_model.fit(forecast_df)

    future = prophet_model.make_future_dataframe(periods=30)

    forecast = prophet_model.predict(future)

    fig = px.line(forecast,x="ds",y="yhat")

    st.plotly_chart(fig)

# ---------------- EXPLAINABLE AI ---------------- #

elif menu == "Explainable AI":

    sample = df.sample(100)

    sample["City"] = encoder.transform(sample["City"])

    sample["Date"] = pd.to_datetime(sample["Date"])
    sample["month"] = sample["Date"].dt.month
    sample["day"] = sample["Date"].dt.day
    sample["day_of_week"] = sample["Date"].dt.dayofweek

    features = [
        'City','PM2.5','PM10','NO','NO2','NOx','NH3',
        'CO','SO2','O3','Benzene','Toluene','Xylene',
        'month','day','day_of_week'
    ]

    X = sample[features]

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X)

    shap_df = pd.DataFrame(
        abs(shap_values).mean(axis=0),
        index=features,
        columns=["importance"]
    ).sort_values("importance")

    fig = px.bar(shap_df,x="importance",y=shap_df.index,orientation="h")

    st.plotly_chart(fig,use_container_width=True)

# ---------------- MAP ---------------- #

elif menu == "Pollution Map":

    st.header("India AQI Heat Map")

    m = folium.Map(location=[20.59,78.96],zoom_start=5,tiles="CartoDB dark_matter")

    coords = {
    "Delhi":[28.61,77.20],
    "Mumbai":[19.07,72.87],
    "Bangalore":[12.97,77.59],
    "Chennai":[13.08,80.27],
    "Kolkata":[22.57,88.36],
    "Hyderabad":[17.38,78.48],
    "Ahmedabad":[23.02,72.57],
    "Pune":[18.52,73.85]
    }

    for city in coords:

        city_df = df[df["City"]==city]

        if len(city_df)==0:
            continue

        avg_aqi = city_df["AQI"].mean()

        lat,lon = coords[city]

        if avg_aqi<=50:
            color="green"
        elif avg_aqi<=100:
            color="yellow"
        elif avg_aqi<=200:
            color="orange"
        elif avg_aqi<=300:
            color="red"
        else:
            color="purple"

        folium.CircleMarker(
            location=[lat,lon],
            radius=10+avg_aqi/40,
            popup=f"{city}<br>AQI {round(avg_aqi,1)}",
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    st_folium(m,width=1000,height=600)